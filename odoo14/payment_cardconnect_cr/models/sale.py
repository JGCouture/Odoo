# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_cardconnect_fees_line = fields.Boolean('Card Connect Fees Line')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_payment_transaction(self, vals):
        # Ensure the currencies are the same.
        currency = self[0].pricelist_id.currency_id
        if any(so.pricelist_id.currency_id != currency for so in self):
            raise ValidationError(_('A transaction can\'t be linked to sales orders having different currencies.'))

        # Ensure the partner are the same.
        partner = self[0].partner_id
        if any(so.partner_id != partner for so in self):
            raise ValidationError(_('A transaction can\'t be linked to sales orders having different partners.'))

        # Try to retrieve the acquirer. However, fallback to the token's acquirer.
        acquirer_id = vals.get('acquirer_id')
        acquirer = False
        payment_token_id = vals.get('payment_token_id')

        if payment_token_id:
            payment_token = self.env['payment.token'].sudo().browse(payment_token_id)
            payment_token.partner_id = partner.id
            # Check payment_token/acquirer matching or take the acquirer from token
            if acquirer_id:
                acquirer = self.env['payment.acquirer'].browse(acquirer_id)
                if payment_token and payment_token.acquirer_id != acquirer:
                    raise ValidationError(_('Invalid token found! Token acquirer %s != %s') % (
                        payment_token.acquirer_id.name, acquirer.name))
                if payment_token and payment_token.partner_id != partner:
                    raise ValidationError(_('Invalid token found! Token partner %s != %s') % (
                        payment_token.partner.name, partner.name))
            else:
                acquirer = payment_token.acquirer_id

        # Check an acquirer is there.
        if not acquirer_id and not acquirer:
            raise ValidationError(_('A payment acquirer is required to create a transaction.'))

        if not acquirer:
            acquirer = self.env['payment.acquirer'].browse(acquirer_id)

        if acquirer and acquirer.provider == 'cardconnect':
            acquirer_fees = acquirer.cardconnect_compute_fees(sum(self.mapped('amount_total')), currency, partner.country_id.id)
            if acquirer_fees:
                for order in self:
                    fees_line = order.order_line.filtered(lambda line: line.is_cardconnect_fees_line)
                    fees_product = self.env.ref('payment_cardconnect_cr.product_cardconnect_fees_line').sudo()
                    if fees_line:
                        fees_line.write({'price_unit': acquirer_fees})
                    else:
                        val = {
                            'name': fees_product.name,
                            'product_id': fees_product.id,
                            'product_uom_qty': 1,
                            'price_unit': acquirer_fees,
                            'is_cardconnect_fees_line': True,
                        }
                        order.write({'order_line': [(0, 0, val)]})
        return super(SaleOrder, self)._create_payment_transaction(vals)
