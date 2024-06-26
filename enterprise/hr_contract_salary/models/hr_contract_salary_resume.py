# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrContractSalaryResumeCategory(models.Model):
    _name = 'hr.contract.salary.resume.category'
    _description = 'Salary Package Resume Category'
    _order = 'sequence'

    name = fields.Char()
    sequence = fields.Integer(default=100)
    periodicity = fields.Selection([
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')])


class HrContractSalaryResume(models.Model):
    _name = 'hr.contract.salary.resume'
    _description = 'Salary Package Resume'

    name = fields.Char()
    value_type = fields.Selection([
        ('fixed', 'Fixed Value'),
        ('contract', 'Contract Value'),
        ('monthly_total', 'Monthly Total'),
        ('sum', 'Sum of Advantages Values')], required=True, default='fixed')
    advantage_ids = fields.Many2many('hr.contract.salary.advantage')
    code = fields.Char()
    fixed_value = fields.Char()
    category_id = fields.Many2one('hr.contract.salary.resume.category', required=True)
    structure_type_id = fields.Many2one('hr.payroll.structure.type', string="Salary Structure Type")
    impacts_monthly_total = fields.Boolean()
    uom = fields.Selection([
        ('days', 'Days'),
        ('percent', 'Percent'),
        ('currency', 'Currency')], string="Advantage Unit of Measure", default='currency')
