# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	iris_api_id = fields.Char(related='company_id.iris_api_id', string='IRIS API ID', readonly=False)
	iris_api_key = fields.Char(related='company_id.iris_api_key',
							   string='IRIS API KEY', readonly=False)


class ResCompany(models.Model):
	_inherit = 'res.company'

	iris_api_id = fields.Char(
		string='IRIS API ID')
	iris_api_key = fields.Char(string='IRIS API KEY')
