# -*- coding: utf-8 -*-

from odoo import api, models, fields,_


class ProductProduct(models.Model):
    _inherit = 'product.product'

    rental_subscription_prod_id = fields.Many2one('product.product', string="Rental Subscription Product")