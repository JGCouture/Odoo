# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

import logging
import hashlib
import hmac
import werkzeug
from odoo.tools.float_utils import float_repr
from odoo import http,_
from odoo.http import request
from odoo.addons.payment.controllers.portal import WebsitePayment,PaymentProcessing
from odoo.osv import expression
from unicodedata import normalize

_logger = logging.getLogger(__name__)


class WebsitePaymentCC(WebsitePayment):
    @staticmethod
    def _get_acquirers_compatible_with_current_user(acquirers):
        # s2s mode will always generate a token, which we don't want for public users
        valid_flows = ['form'] if request.env.user._is_public() else ['form', 's2s']
        return [acq for acq in acquirers if acq.payment_flow in valid_flows] + [acq for acq in acquirers if acq.provider == "cardconnect" and request.env.user._is_public()]
        # res = super(WebsitePaymentCC, self)._get_acquirers_compatible_with_current_user(acquirers)

    @http.route()
    def payment_token(self, pm_id, reference, amount, currency_id, partner_id=False, return_url=None, **kwargs):
        token = request.env['payment.token'].sudo().browse(int(pm_id))
        order_id = kwargs.get('order_id')
        invoice_id = kwargs.get('invoice_id')
        if not token:
            return request.redirect('/website_payment/pay?error_msg=%s' % _('Cannot setup the payment.'))
        values = {
            'acquirer_id': token.acquirer_id.id,
            'reference': reference,
            'amount': float(amount),
            'currency_id': int(currency_id),
            'partner_id': int(partner_id),
            'payment_token_id': int(pm_id),
            'type': 'server2server',
            'return_url': return_url,
        }
        if order_id:
            values['sale_order_ids'] = [(6, 0, [int(order_id)])]

            acquirer = token.acquirer_id
            partner = request.env['res.partner'].sudo().browse(int(partner_id))
            order_id = request.env['sale.order'].sudo().browse(int(order_id))
            if acquirer and acquirer.provider == 'cardconnect':
                acquirer_fees = acquirer.cardconnect_compute_fees(float(amount), int(currency_id), partner.country_id.id)
                if acquirer_fees:
                    values.update({'amount': acquirer_fees + values.get('amount', 0)})
                    for order in order_id:
                        fees_line = order.order_line.filtered(lambda line: line.is_cardconnect_fees_line)
                        fees_product = request.env.ref('payment_cardconnect_cr.product_cardconnect_fees_line')
                        if fees_line:
                            fees_line.write({'price_unit': acquirer_fees})
                        else:
                            val = {
                                'name': fees_product.sudo().name,
                                'product_id': fees_product.sudo().id,
                                'product_uom_qty': 1,
                                'price_unit': acquirer_fees,
                                'is_cardconnect_fees_line': True,
                            }
                            order.write({'order_line': [(0, 0, val)]})

        if invoice_id:
            values['invoice_ids'] = [(6, 0, [int(invoice_id)])]

            acquirer = token.acquirer_id
            partner = request.env['res.partner'].sudo().browse(int(partner_id))
            invoice_id = request.env['account.move'].sudo().browse(int(invoice_id))
            if acquirer and acquirer.provider == 'cardconnect':
                acquirer_fees = acquirer.cardconnect_compute_fees(float(amount), int(currency_id), partner.country_id.id)
                if acquirer_fees:
                    values.update({'amount': acquirer_fees + values.get('amount', 0)})
                    for invoice in invoice_id:
                        fees_line = invoice.invoice_line_ids.filtered(lambda line: line.is_cardconnect_fees_line)
                        fees_product = request.env.ref('payment_cardconnect_cr.product_cardconnect_fees_line')
                        if fees_line:
                            fees_line.write({'price_unit': acquirer_fees})
                        else:
                            val = {
                                'name': fees_product.sudo().name,
                                'product_id': fees_product.sudo().id,
                                'quantity': 1,
                                'price_unit': acquirer_fees,
                                'is_cardconnect_fees_line': True,
                                'account_id': fees_product.sudo().property_account_income_id.id,
                            }
                            invoice.write({'invoice_line_ids': [(0, 0, val)]})

        tx = request.env['payment.transaction'].sudo().with_context(lang=None).create(values)
        PaymentProcessing.add_payment_transaction(tx)

        try:
            tx.s2s_do_transaction()
            secret = request.env['ir.config_parameter'].sudo().get_param('database.secret')
            token_str = '%s%s%s' % (tx.id, tx.reference, float_repr(tx.amount, precision_digits=tx.currency_id.decimal_places))
            token = hmac.new(secret.encode('utf-8'), token_str.encode('utf-8'), hashlib.sha256).hexdigest()
            tx.return_url = return_url or '/website_payment/confirm?tx_id=%d&access_token=%s' % (tx.id, token)
        except Exception as e:
            _logger.exception(e)
        return request.redirect('/payment/process')

    @http.route()
    def pay(self, reference='', order_id=None, amount=False, currency_id=None, acquirer_id=None, partner_id=False, access_token=None, **kw):
        env = request.env
        user = env.user.sudo()
        reference = normalize('NFKD', reference).encode('ascii', 'ignore').decode('utf-8')
        if partner_id and not access_token:
            raise werkzeug.exceptions.NotFound
        if partner_id and access_token:
            token_ok = request.env['payment.link.wizard'].check_token(access_token, int(partner_id), float(amount), int(currency_id))
            if not token_ok:
                raise werkzeug.exceptions.NotFound

        invoice_id = kw.get('invoice_id')

        # Default values
        values = {
            'amount': 0.0,
            'currency': user.company_id.currency_id,
        }

        # Check sale order
        if order_id:
            try:
                order_id = int(order_id)
                if partner_id:
                    # `sudo` needed if the user is not connected.
                    # A public user woudn't be able to read the sale order.
                    # With `partner_id`, an access_token should be validated, preventing a data breach.
                    order = env['sale.order'].sudo().browse(order_id)
                else:
                    order = env['sale.order'].browse(order_id)
                values.update({
                    'currency': order.currency_id,
                    'amount': order.amount_total,
                    'order_id': order_id
                })
            except:
                order_id = None

        if invoice_id:
            try:
                values['invoice_id'] = int(invoice_id)
            except ValueError:
                invoice_id = None

        # Check currency
        if currency_id:
            try:
                currency_id = int(currency_id)
                values['currency'] = env['res.currency'].browse(currency_id)
            except:
                pass

        # Check amount
        if amount:
            try:
                amount = float(amount)
                values['amount'] = amount
            except:
                pass

        # Check reference
        reference_values = order_id and {'sale_order_ids': [(4, order_id)]} or {}
        values['reference'] = env['payment.transaction']._compute_reference(values=reference_values, prefix=reference)

        # Check acquirer
        acquirers = None
        if order_id and order:
            cid = order.company_id.id
        elif kw.get('company_id'):
            try:
                cid = int(kw.get('company_id'))
            except:
                cid = user.company_id.id
        else:
            cid = user.company_id.id

        # Check partner
        if not user._is_public():
            # NOTE: this means that if the partner was set in the GET param, it gets overwritten here
            # This is something we want, since security rules are based on the partner - assuming the
            # access_token checked out at the start, this should have no impact on the payment itself
            # existing besides making reconciliation possibly more difficult (if the payment partner is
            # not the same as the invoice partner, for example)
            partner_id = user.partner_id.id
        elif partner_id:
            partner_id = int(partner_id)

        values.update({
            'partner_id': partner_id,
            'bootstrap_formatting': True,
            'error_msg': kw.get('error_msg')
        })

        acquirer_domain = ['&', ('state', 'in', ['enabled', 'test']), ('company_id', '=', cid)]
        if partner_id:
            partner = request.env['res.partner'].browse([partner_id])
            acquirer_domain = expression.AND([
                acquirer_domain,
                ['|', ('country_ids', '=', False), ('country_ids', 'in', [partner.sudo().country_id.id])]
            ])
        if acquirer_id:
            acquirers = env['payment.acquirer'].browse(int(acquirer_id))
        if order_id:
            acquirers = env['payment.acquirer'].search(acquirer_domain)
        if not acquirers:
            acquirers = env['payment.acquirer'].search(acquirer_domain)

        values['acquirers'] = self._get_acquirers_compatible_with_current_user(acquirers)
        if partner_id:
            values['pms'] = request.env['payment.token'].search([
                ('acquirer_id', 'in', acquirers.ids),
                ('partner_id', 'child_of', partner.commercial_partner_id.id)
            ])
        else:
            values['pms'] = []

        if values['acquirers']:
            valid_flows = ['form'] if request.env.user._is_public() else ['form', 's2s']
            custom_acquirers = acquirers.filtered(lambda x: x.provider == "cardconnect" or x.payment_flow in valid_flows)
            cc_partner_id = request.env['res.partner'].sudo()
            if values.get("partner_id"):
                cc_partner_id = request.env['res.partner'].sudo().browse(values['partner_id'])
            values['acq_extra_fees'] = custom_acquirers.get_acquirer_extra_fees(values['amount'], values['currency'], cc_partner_id.country_id.id)
        return request.render('payment.pay', values)

class CarcconnectController(http.Controller):

    @http.route(['/payment/cardconnect/s2s/create_json_3ds'], type='json', auth='public', csrf=False)
    def cardconnect_s2s_create_json_3ds(self, verify_validity=False, **kwargs):
        if not kwargs.get('partner_id'):
            kwargs = dict(kwargs, partner_id=request.env.user.partner_id.id)
        token = False
        error = None
        try:
            token = request.env['payment.acquirer'].browse(int(kwargs.get('acquirer_id'))).s2s_process(kwargs)
        except Exception as e:
            error = str(e)
        if not token:
            res = {
                'result': False,
                'error': error,
            }
            return res
        res = {
            'result': True,
            'id': token.id,
            'short_name': token.short_name,
            '3d_secure': False,
            'verified': True,
        }
        return res
