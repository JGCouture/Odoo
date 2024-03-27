# -*- coding: utf-8 -*-
import requests
import json
import logging
import datetime
from odoo import api, fields, models, _
from odoo import api, fields, models, tools, _, SUPERUSER_ID

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @tools.ormcache()
    def _get_default_category_id(self):
        # Deletion forbidden (at least through unlink)
        return super(ProductTemplate, self)._get_default_category_id()

    def _read_group_categ_id(self, categories, domain, order):
        return super(ProductTemplate, self)._read_group_categ_id(categories, domain, order)

    # type = fields.Selection([
    #     ('consu', 'Consumable'),
    #     ('service', 'Service')], string='Product Type', default='consu', required=True,
    #     help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
    #          'A consumable product is a product for which stock is not managed.\n'
    #          'A service is a non-material product you provide.', tracking=True)
    sale_ok = fields.Boolean('Can be Sold', default=True, tracking=True)
    purchase_ok = fields.Boolean('Can be Purchased', default=True, tracking=True)
    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True, default=_get_default_category_id, group_expand='_read_group_categ_id',
        required=True, help="Select category for the current product", tracking=True)
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, tracking=True)

