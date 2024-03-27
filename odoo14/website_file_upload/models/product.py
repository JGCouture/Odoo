#  -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    required_doc_ids = fields.One2many('sale.required.doc', 'product_id', string="Required Documents")


class SaleRequiredDoc(models.Model):
    _name = 'sale.required.doc'
    _description = "Sale Required Documents"

    name = fields.Char(string="Document Name", required=True)
    product_id = fields.Many2one('product.product', string="Product")
