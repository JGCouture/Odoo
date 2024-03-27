# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SignTemplate(models.Model):
    _inherit = 'sign.template'

    company_id = fields.Many2one('res.company', string="Company")


class SignRequest(models.Model):
    _inherit = 'sign.request'

    company_id = fields.Many2one('res.company', string="Company", related="template_id.company_id")