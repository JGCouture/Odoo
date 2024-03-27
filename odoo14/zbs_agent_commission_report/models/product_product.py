# -*- coding: utf-8 -*-

from odoo import api, models, fields,_


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_promotion_product = fields.Boolean(string="Is Promotion Product?", tracking=True)
    is_package_product = fields.Boolean(string="Is Package Product?", tracking=True)
    not_show_in_agent_report = fields.Boolean(string="Do not show in agent report", tracking=True)
    is_shipping_product = fields.Boolean(string="Is Shipping Product?", tracking=True)
    is_misc_product = fields.Boolean(string="Is Misc Product?", tracking=True)