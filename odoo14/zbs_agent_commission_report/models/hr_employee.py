# -*- coding: utf-8 -*-

from odoo import api, models, fields,_
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    commission_per = fields.Float(string="Commission Percentage(%)")
    is_a_agent = fields.Boolean(string="Is a Agent?")

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    commission_per = fields.Float(string="Commission Percentage(%)")