# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    special_diacount_applicable = fields.Boolean(string="Special Diacount Applicable")
    

class ProductProduct(models.Model):
    _inherit = 'product.product'

    website_term = fields.Html(string="Term & Conditions")
    hyper_link_ids = fields.One2many('product.hyper.link', 'product_id', string="Links")


class ProductHyperLink(models.Model):
    _name = 'product.hyper.link'
    _description = "Product Links"

    name = fields.Char(string="Name")
    url = fields.Char(string="Url")
    product_id = fields.Many2one('product.product', string="Product")