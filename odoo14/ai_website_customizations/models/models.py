# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        res = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        if self.order_line:
            req_order_lines = self.order_line.filtered(lambda l:l.is_required_prod_line)
            if req_order_lines:
                for req_line in req_order_lines:
                    req_line.price_unit = req_line.special_price
        return res

    def get_recurring_total(self):
        total = 0
        if self.order_line:
            lines = self.order_line.filtered(lambda l: l.is_subscription_product == True or l.product_id.recurring_invoice)
            if lines:
                total = sum(lines.mapped('price_subtotal'))
        return total

class RequiredProdConfig(models.Model):
    _name = 'required.prod.config'
    _description = "Required Product Configuration"
    _rec_name = 'product_template_id'

    product_template_id = fields.Many2one('product.template', stirng="Product Template")
    required_product_ids = fields.One2many('sale.required.product', 'required_config_id', string="Required Product")
    variant_ids = fields.Many2many('product.product','rel_required_config_variant', string="Variant")

    @api.constrains('variant_ids')
    def _check_product_variant(self):
        for rec in self:
            variants = rec.variant_ids.ids
            config_ids = self.search([('product_template_id', '=', rec.product_template_id.id), ('id','!=', rec.id)])
            if config_ids:
                for each in config_ids:
                    if each.variant_ids:
                        for each_var in each.variant_ids:
                            if each_var.id in variants:
                                raise Warning('You have already added product '+ each_var.display_name + ' in other required product configuration.')

class SaleRequiredProduct(models.Model):
    _name = 'sale.required.product'
    _description = "Sale Required Products"
    _rec_name = 'product_id'

    required_config_id = fields.Many2one('required.prod.config', string="Required Product", required=True)
    product_id = fields.Many2one('product.product', string="Product")
    special_price = fields.Float(string="Special Price")
    required_qty = fields.Float(string="Required Qty")
    update_with_main_qty = fields.Boolean(string="Update QTY")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def create_required_prod_config(self):
        required_config_ids = self.env['required.prod.config'].sudo().search([('product_template_id', '=', self.id)])
        return {
            'name': 'Required Product Configuration',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'required.prod.config',
            'context': {'default_product_template_id': self.id},
            'domain' : [('id','in',required_config_ids.ids)],
            'type': 'ir.actions.act_window',
        }


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_subscription_product = fields.Boolean(copy=False)
    product_line_id = fields.Integer()
    is_required_prod_line = fields.Boolean()
    required_src_sale_line_id = fields.Integer()
    special_price = fields.Float(string="Special Price")
    auto_update_qty = fields.Boolean()
    required_qty = fields.Float()

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        if self.is_required_prod_line:
            self.price_unit = self.special_price
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        if res.product_id.subscription_product_id:
            product_id = res.product_id.subscription_product_id[0]
            sale_line_id = self.create({
                'product_id': product_id.id,
                'product_uom_qty': res.product_uom_qty,
                'order_id': res.order_id.id,
                'product_uom': product_id.uom_id.id,
                'price_unit': product_id.lst_price,
                'discount': 0,
                'is_subscription_product': True,
                'product_line_id': self.id,
            })
            sale_line_id.product_uom_change()

        # required product line
        required_config_ids = self.env['required.prod.config'].sudo().search([('product_template_id', '=', res.product_id.product_tmpl_id.id)])
        if required_config_ids:
            for req in required_config_ids:
                if req.variant_ids:
                    if res.product_id.id in req.variant_ids.ids and req.required_product_ids:
                        for each in req.required_product_ids:
                            order_line = False
                            if res.order_id.order_line:
                                order_line = res.order_id.order_line.filtered(lambda l:l.product_id == each.product_id and l.required_src_sale_line_id == res.id)
                            if not order_line:
                                if each.required_qty:
                                    required_sale_line_id = self.create({
                                        'product_id': each.product_id.id,
                                        'product_uom_qty': each.required_qty,
                                        'order_id': res.order_id.id,
                                        'product_uom': each.product_id.uom_id.id,
                                        'price_unit': each.special_price,
                                        'is_required_prod_line': True,
                                        'auto_update_qty': each.update_with_main_qty,
                                        'required_qty': each.required_qty,
                                        'special_price': each.special_price,
                                        'required_src_sale_line_id': res.id,
                                    })
                                    required_sale_line_id.product_uom_change()
        return res
    
    def write(self, vals):
        if vals.get('product_uom_qty') and vals.get('product_uom_qty') >= 1:
            required_prod_config_ids = self.env['required.prod.config'].search([('product_template_id','=', self.product_id.product_tmpl_id.id)])
            if required_prod_config_ids:
                prod_lst = []
                for rc in required_prod_config_ids:
                    if rc.required_product_ids:
                        for rcp in rc.required_product_ids:
                            prod_lst.append(rcp.product_id.id)
                if prod_lst:
                    rp_existing_line_ids = self.search([('required_src_sale_line_id', '=', self.id),('order_id','=', self.order_id.id),('is_required_prod_line','=', True),('auto_update_qty','=', True),('product_id','in', prod_lst)])
                    if rp_existing_line_ids:
                        for rp_line in rp_existing_line_ids:
                            rp_line.product_uom_qty = vals.get('product_uom_qty') * rp_line.required_qty
        if vals.get('product_uom_qty') and vals.get('product_uom_qty') > 1:
            if self.product_id.subscription_product_id and len(self.product_id.subscription_product_id) > 1:
                if vals.get('product_uom_qty') > 1:
                    product_id = self.product_id.subscription_product_id[1]
                    existing_line_id = self.search([('order_id','=', self.order_id.id),('is_subscription_product','=', True),('product_line_id','=', self.id),('product_id','=', product_id.id) ])
                    if existing_line_id:
                        existing_line_id.product_uom_qty = vals.get('product_uom_qty') - 1
                    else:
                        sale_line_id = self.create({
                            'product_id': product_id.id,
                            'product_uom_qty': vals.get('product_uom_qty') - 1,
                            'order_id': self.order_id.id,
                            'product_uom': product_id.uom_id.id,
                            'price_unit': product_id.lst_price,
                            'discount': 0,
                            'is_subscription_product': True,
                            'product_line_id': self.id,
                        })
                        sale_line_id.product_uom_change()
            if self.product_id.subscription_product_id and len(self.product_id.subscription_product_id) == 1:
                product_id = self.product_id.subscription_product_id[0]
                existing_line_id = self.search(
                    [('order_id', '=', self.order_id.id), ('is_subscription_product', '=', True),
                     ('product_id', '=', product_id.id)])
                if existing_line_id:
                    existing_line_id.product_uom_qty = vals.get('product_uom_qty')

        elif vals.get('product_uom_qty') and vals.get('product_uom_qty') == 1:
            if self.product_id.subscription_product_id and len(self.product_id.subscription_product_id) > 1:
                product_id1 = self.product_id.subscription_product_id[0]
                product_id2 = self.product_id.subscription_product_id[1]
                existing_line_id2 = self.search(
                    [('order_id', '=', self.order_id.id), ('is_subscription_product', '=', True),
                     ('product_line_id', '=', self.id), ('product_id', '=', product_id2.id)])
                existing_line_id1 = self.search(
                    [('order_id', '=', self.order_id.id), ('is_subscription_product', '=', True),
                     ('product_line_id', '=', self.id), ('product_id', '=', product_id1.id)])
                if existing_line_id2:
                    existing_line_id2.unlink()
                if existing_line_id1:
                    existing_line_id1.product_uom_qty = vals.get('product_uom_qty')
            if self.product_id.subscription_product_id and len(self.product_id.subscription_product_id) == 1:
                product_id = self.product_id.subscription_product_id[0]
                existing_line_id = self.search(
                    [('order_id', '=', self.order_id.id), ('is_subscription_product', '=', True),
                     ('product_id', '=', product_id.id)])
                if existing_line_id:
                    existing_line_id.product_uom_qty = vals.get('product_uom_qty')
        return super(SaleOrderLine, self).write(vals)

    def unlink(self):
        for line in self:
            if line.order_id and line.product_id.subscription_product_id:
                if len(line.product_id.subscription_product_id.ids) == 1:
                    product_ids = line.order_id.order_line.filtered(lambda l:l.product_id.id == line.product_id.subscription_product_id[0].id)
                    product_ids.unlink()
                if len(line.product_id.subscription_product_id.ids) > 1:
                    product_ids = line.order_id.order_line.filtered(
                        lambda l: l.product_id.id in line.product_id.subscription_product_id.ids)
                    product_ids.unlink()
            required_prod_lines = self.search([('order_id','=',line.order_id.id),('is_required_prod_line', '=', True), ('required_src_sale_line_id','=', line.id)])
            if required_prod_lines:
                required_prod_lines.unlink()
            return super(SaleOrderLine, self).unlink()

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        self.ensure_one()
        if self.is_subscription_product:
            res['is_subscription_product'] = True
        return res


class ProductProduct(models.Model):
    _inherit = "product.product"

    subscription_product_id = fields.Many2many("product.product","relation_subscription_product_table","product_id","subscription_id", string="Subscription Product")

    def write(self, vals):
        if 'lst_price' in vals:
            old_price = self.lst_price
        res = super(ProductProduct, self).write(vals)
        if 'lst_price' in vals:
            subscription_product_ids = self.search([('subscription_product_id','in',self.ids)])
            if subscription_product_ids:
                for prod in subscription_product_ids:
                    message = "Subscription Product " + self.name + " price change " + str('%.2f'% old_price) + ' -> ' + str('%.2f'% vals.get('lst_price'))
                    prod.message_post(body=message)
        return res


class Website(models.Model):
    _inherit = "website"

    restrict_login = fields.Boolean(string="Restrict Login")


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_subscription_product = fields.Boolean(copy=False)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_recurring_total(self):
        total = 0
        if self.invoice_line_ids:
            lines = self.invoice_line_ids.filtered(lambda l: l.is_subscription_product == True or (l.product_id and l.product_id.recurring_invoice))
            if lines:
                total = sum(lines.mapped('price_subtotal'))
        return total