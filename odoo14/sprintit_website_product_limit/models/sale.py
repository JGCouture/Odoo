# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import models, _
        
class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        product = self.env['product.product'].browse(product_id)
        order_line = self._cart_find_product_line(product_id, line_id, **kwargs)[:1]
        warning = ' '
        exist_qty = 0
        exist_lines = order_line.order_id.order_line.filtered(lambda l:l.product_id.product_tmpl_id == product.product_tmpl_id and product.attribute_value_id.id in l.product_id.product_template_attribute_value_ids.ids and l.id != order_line.id)
        if exist_lines:
            exist_qty = sum(exist_lines.mapped('product_uom_qty'))
            # set_qty += sum(exist_lines.mapped('product_uom_qty'))
        if product.apply_order_limit and product.attribute_value_id:
            if set_qty > 0 and product.order_limit and (set_qty + exist_qty) > product.order_limit:
                # if set_qty > product.order_limit:
                msg = "You have already added " + str(
                    product.order_limit) + ' quantity for product ' + product.name + " With attribute " + product.attribute_value_id.name
                msg += "." + "\nMaximum purchase limit of product " + product.name + " with attribute " + product.attribute_value_id.name + " is " + str(
                    product.order_limit)
                msg += "\n" + " and you are trying to purchase " + str(set_qty) + " quantity."
                msg += "\n" + "Please select other variant combination or select higher package to purchase more quantity."
                warning = (_(msg))
                set_qty = product.order_limit - exist_qty
                order_line.write({'product_uom_qty': product.order_limit})
            if add_qty and (float(add_qty) + order_line.product_uom_qty) > product.order_limit:
                set_qty = product.order_limit
        if product.apply_order_limit and not product.attribute_value_id:
            if set_qty > 0 and product.order_limit:
                if set_qty > product.order_limit:
                    warning = _('You have already added maximum purchasable quantity %s for products %s. please select another product or higher package to purchase more quantity.') % (product.order_limit, product.name)
                    set_qty = product.order_limit
                    order_line.write({'product_uom_qty': product.order_limit})
            if add_qty and (float(add_qty) + order_line.product_uom_qty) > product.order_limit:
                set_qty = product.order_limit
        res = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        res['warning'] = warning
        return res
