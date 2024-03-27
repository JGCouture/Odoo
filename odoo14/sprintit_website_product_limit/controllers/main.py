# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.models import ir_http

import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import ValidationError
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.osv import expression
_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        prod_id = request.env['product.product'].sudo().browse(int(product_id))
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(kw.get('no_variant_attribute_values'))
        if prod_id and prod_id.apply_order_limit and sale_order and prod_id.attribute_value_id:
            if sale_order.order_line:
                order_lines = sale_order.order_line.filtered(lambda l:l.product_id.product_tmpl_id == prod_id.product_tmpl_id and prod_id.attribute_value_id.id in l.product_id.product_template_attribute_value_ids.ids)
                # if order_lines:
                #     msg = 'You have already added maximum qty ' + str((prod_id.order_limit)) + '. of product ' + prod_id.name + ' with ' +  prod_id.attribute_value_id.name + ' Please select another variant or upgrade package to buy more quantity.'
                #     raise ValidationError(msg)
                # quatity check.
                if order_lines:
                    total_order_qty = sum(order_lines.mapped('product_uom_qty'))
                    if (total_order_qty + float(add_qty)) > prod_id.order_limit:
                        msg = "You have already added " + str(total_order_qty) + ' quantity for product' + prod_id.name + " With attribute " +  prod_id.attribute_value_id.name
                        msg += "." + "\nMaximum purchase limit of product " + prod_id.name +" with attribute " + prod_id.attribute_value_id.name + " is " + str(prod_id.order_limit)
                        msg += "\n" + "You are trying to purchase " + str(total_order_qty + float(add_qty)) + " quantity."
                        msg += "\n" + "Please select other variant combination or select higher package to purchase more quantity."
                        raise ValidationError(msg)

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )

        if kw.get('express'):
            return request.redirect("/shop/checkout?express=1")

        return request.redirect("/shop/cart")


class WebsiteSaleVariantController(WebsiteSaleVariantController):
    
    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        res = super(WebsiteSaleVariantController, self).get_combination_info_website(product_template_id, product_id, combination, add_qty, **kw)
        product_obj = request.env['product.template'].browse(product_template_id)
        product_id_obj = request.env['product.product'].browse(product_id)
        website = ir_http.get_request_website()
        product_cart_qty = 0
        if website:
            cart = website.sale_get_order()
            product_cart_qty = sum(cart.order_line.filtered(lambda p: p.product_id.id == product_id_obj.id).mapped('product_uom_qty')) if cart else 0
        res.update({'apply_order_limit': product_id_obj.apply_order_limit, 'order_limit': product_id_obj.order_limit, 'display_message' : False, 'product_cart_qty': product_cart_qty})
        return res