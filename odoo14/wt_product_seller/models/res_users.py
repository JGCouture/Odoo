# -*- coding: utf-8 -*-

from odoo import models, fields, _


class ResUsers(models.Model):
    _inherit = "res.users"

    is_seller = fields.Boolean('Is seller ?')
    seller_employee_id = fields.Many2one('hr.employee', string="Seller Employee")