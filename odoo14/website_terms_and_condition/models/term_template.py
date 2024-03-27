# -*- coding: utf-8 -*-

from odoo import fields, models, api


class PosTermTemplate(models.Model):
    _name = 'pos.term.template'
    _description = 'POS Term Condition Template'

    name = fields.Char(string="Name")
    term = fields.Html(string="Term and Condition")
    product_ids = fields.Many2many('product.product', string="Products")