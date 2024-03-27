# -*- coding: utf-8 -*-
import requests
import json
import logging
import datetime
from odoo import api, fields, models, _
import gspread
from odoo.modules.module import get_module_resource
import time
_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    def _set_product_lst_price(self):
        super(ProductProduct, self)._set_product_lst_price()

    @api.depends('list_price', 'price_extra')
    @api.depends_context('uom')
    def _compute_product_lst_price(self):
        super(ProductProduct, self)._compute_product_lst_price()

    standard_price = fields.Float(
        'Cost', company_dependent=True,
        digits='Product Price',
        groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the next unit that will leave the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""", tracking=True)
    barcode = fields.Char(
        'Barcode', copy=False,
        help="International Article Number used for product identification.", tracking=True)
    lst_price = fields.Float(
        'Public Price', compute='_compute_product_lst_price',
        digits='Product Price', inverse='_set_product_lst_price',
        help="The sale price is managed from the product template. Click on the 'Configure Variants' button to set the extra attribute prices.", tracking=True)