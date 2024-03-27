# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.sale.controllers.portal import CustomerPortal as portal
from odoo.http import request


class CustomerPortal(portal):

	@http.route(['/my/orders/<int:order_id>/transaction/'], type='json',
				auth="public", website=True)
	def payment_transaction_token(self, acquirer_id, order_id,
								  save_token=False,
								  access_token=None, **kwargs):
		order = request.env['sale.order'].sudo().browse(order_id)
		advance_payment = 'advance_payment' in kwargs and kwargs.get(
			'advance_payment') or False
		if advance_payment:
			order.write({'advance_amount': advance_payment})
		return super(CustomerPortal, self).payment_transaction_token(
			acquirer_id, order_id, save_token, access_token, **kwargs)

	@http.route('/my/orders/<int:order_id>/transaction/token', type='http',
				auth='public', website=True)
	def payment_token(self, order_id, pm_id=None, **kwargs):
		order = request.env['sale.order'].sudo().browse(order_id)
		advance_payment = 'advance_payment' in kwargs and kwargs.get(
			'advance_payment') or False
		if advance_payment:
			order.write({'advance_amount': advance_payment})
		return super(CustomerPortal, self).payment_token(
			order_id, pm_id=pm_id, **kwargs)
