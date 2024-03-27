# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    advance_amount = fields.Float(string="Advance Amount", required=False,
                                  copy=False)
    is_advance_amount = fields.Boolean(string="Is Advance Amount")
    advance_amount_pay = fields.Float(string="Advance Amount Pay",
                                      compute="_advance_amount_pay",
                                      store=True,
                                      required=False)
    down_payment_total = fields.Monetary(string="Down Payment",
                                         compute="_compute_down_payment",
                                         store=True)
    invoiced_amount = fields.Float(string='Invoiced Amount',
                                   compute='_compute_invoice_amount')
    amount_due = fields.Float(string='Amount Due',
                              compute='_compute_amount_due')
    paid_amount = fields.Float(string='Paid Amount',
                               compute='_compute_amount_paid')

    def _compute_invoice_amount(self):
        for record in self:
            invoice_id = self.env['account.move'].search(
                ['&', ('invoice_origin', '=', record.name),('state', '=', 'posted'),
                 ('payment_state', 'not in', ['reversed', 'invoicing_legacy'])])
            total = 0

            if invoice_id:
                for invoice in invoice_id:
                    total += invoice.amount_total
                    record.invoiced_amount = total
            else:
                record.invoiced_amount = total

    @api.depends('paid_amount', 'invoiced_amount', 'amount_due')
    def _compute_amount_due(self):
        for record in self:
            invoice_ids = self.env['account.move'].search(
                ['&', ('invoice_origin', '=', record.name), ('state', '=', 'posted'),
                 ('payment_state', 'not in', ['reversed', 'invoicing_legacy'])])
            amount_due = 0

            if invoice_ids:
                for inv in invoice_ids:
                    amount_due += inv.amount_residual
                total_paid = record.down_payment_total + record.paid_amount
                if record.amount_due == 0 and record.amount_total != total_paid:
                    amount_due = amount_due + record.down_payment_total
                if record.amount_total == total_paid:
                    amount_due = 0
                record.amount_due = amount_due
            else:
                record.amount_due = amount_due

    @api.onchange('invoiced_amount', 'amount_due')
    def _compute_amount_paid(self):
        self.paid_amount = float(self.invoiced_amount) - float(
            self.amount_due)

    @api.depends('order_line.product_id', 'order_line.qty_invoiced',
                 'invoice_ids.amount_residual')
    def _compute_down_payment(self):
        """
            Calculate down payment amount and total due amount in sale order
        """
        for obj in self:
            down_payment_lines = obj.order_line.filtered(
                lambda l: l.is_downpayment)
            obj.down_payment_total = sum(down_payment_lines.mapped(
                'price_unit'))

    def has_to_be_paid(self, include_draft=False):
        transaction = self.get_portal_last_transaction()
        require_payment = self.require_payment
        if not self.is_advance_amount and self.state == 'sent':
            require_payment = False
        return (self.state == 'sent' or self.state == 'sale' or (self.state == 'draft' and include_draft)) and not self.is_expired and require_payment and transaction.state != 'done' and self.amount_total

    @api.depends('payment_term_id', 'amount_total')
    def _advance_amount_pay(self):
        for obj in self:
            payment_line_ids = \
                obj.payment_term_id.line_ids.filtered(
                    lambda l: l.value == 'percent' and l.days == 0)
            value_amount = payment_line_ids and payment_line_ids[
                0].value_amount or 0.00
            obj.advance_amount_pay = (obj.amount_total * value_amount) / 100

    @api.onchange('payment_term_id')
    def onchange_method(self):
        payment_line_ids = \
            self.payment_term_id.line_ids.filtered(
                lambda l: l.value == 'percent' and l.days == 0)
        is_advance_amount = False
        if payment_line_ids:
            is_advance_amount = True
        self.is_advance_amount = is_advance_amount


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _invoice_sale_orders(self):
        if self.env['ir.config_parameter'].sudo().get_param('sale.automatic_invoice'):
            for trans in self.filtered(lambda t: t.sale_order_ids):
                trans = trans.with_company(trans.acquirer_id.company_id)\
                    .with_context(company_id=trans.acquirer_id.company_id.id)
                confirmed_orders = trans.sale_order_ids.filtered(lambda so: so.state in ('sale', 'done'))
                if confirmed_orders and not confirmed_orders.is_advance_amount:
                    confirmed_orders._force_lines_to_invoice_policy_order()
                    invoices = confirmed_orders._create_invoices()
                    trans.invoice_ids = [(6, 0, invoices.ids)]


    def create_downpayment_invoice(self, amount, so):
        context = {'active_model': 'sale.order', 'active_ids': [so.id], 'active_id': so.id,
                   'default_sale_order_id': so.id}
        adv_inv = self.env['sale.advance.payment.inv'].sudo().with_context(
            context).create({'advance_payment_method': 'fixed',
                             'fixed_amount': amount})
        adv_inv.with_context(default_is_downpayment_inv=True).sudo().create_invoices()
        invoice = so.sudo().invoice_ids.filtered(lambda l: l.state == 'draft'
                                                           and l.move_type == 'out_invoice')
        self.sudo().write({'invoice_ids': [(6, 0, invoice.ids)]})

    def render_sale_button(self, order, submit_txt=None, render_values=None):
        values = {
            'partner_id': order.partner_id.id,
            'type': self.type,
        }
        if render_values:
            values.update(render_values)
        # Not very elegant to do that here but no choice regarding the design.
        self._log_payment_transaction_sent()
        amount_total = order.amount_total
        if order.is_advance_amount:
            amount_total = self.amount
        return self.acquirer_id.with_context(
            submit_class='btn btn-primary',
            submit_txt=submit_txt or _('Pay Now')).sudo().render(
            self.reference,
            amount_total,
            order.pricelist_id.currency_id.id,
            values=values,
        )

    @api.model_create_multi
    def create(self, vals_list):
        res = super(PaymentTransaction, self).create(vals_list)
        if sum(res.sale_order_ids.mapped('advance_amount')) > 0:
            res.amount = sum(res.sale_order_ids.mapped('advance_amount'))
        return res

    def _check_amount_and_confirm_order(self):
        self.ensure_one()
        for order in self.sale_order_ids.filtered(
                lambda so: so.state in ('draft', 'sent')):
            cmp_advance_payment = order.currency_id.compare_amounts(
                self.amount, order.advance_amount_pay) == 0
            if order.currency_id.compare_amounts(
                    self.amount, order.amount_total) == 0 or \
                    cmp_advance_payment:
                order.with_context(send_email=True).action_confirm()
                if order.is_advance_amount and cmp_advance_payment:
                    self.create_downpayment_invoice(self.amount, order)
            else:
                _logger.warning(
                    '<%s> transaction AMOUNT MISMATCH for order %s (ID %s): expected %r, got %r',
                    self.acquirer_id.provider,order.name, order.id,
                    order.amount_total, self.amount,
                )
                order.message_post(
                    subject=_("Amount Mismatch (%s)",
                              self.acquirer_id.provider),
                    body=_("The order was not confirmed despite response from the acquirer (%s): order total is %r but acquirer replied with %r.") % (
                        self.acquirer_id.provider,
                        order.amount_total,
                        self.amount,
                    )
                )
