# -*- coding: utf-8 -*-


from odoo import models, fields, api


class IrisIntegration(models.Model):
	_name = 'iris.integration.history'
	_rec_name = 'order_id'
	_description = 'Iris Integration'

	order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order", required=False)
	user_id = fields.Many2one(comodel_name="res.users", string="User")
	partner_id = fields.Many2one(comodel_name="res.partner",
									string="Customer", required=False, )
	note = fields.Text(string="Note", required=False, )
	response = fields.Text(string="Response", required=False)


