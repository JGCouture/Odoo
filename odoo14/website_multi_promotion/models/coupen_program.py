# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CouponProgram(models.Model):
    _inherit = 'coupon.program'

    allow_cumulative = fields.Boolean(string="Allow Cumulative")
    discount_most_expensive = fields.Boolean(string="Apply discount on most expensive product")
    code_in_chines = fields.Char(string="Promotion code in chines")
    limit_per_customer = fields.Integer(string="Limit Per Customer")
    other_program_ids = fields.Many2many('coupon.program', 'related_coupon_program', 'main_program_id','related_program_id', string="Related Program")

    def _check_promo_code(self, order, coupon_code):
        promotion_program = False
        if coupon_code:
            promotion_program = self.env['coupon.program'].search([('promo_code', '=', coupon_code)], limit=1)
            if not promotion_program:
                promotion_program = self.env['coupon.program'].search([('code_in_chines', '=', coupon_code)], limit=1)
        message = {}

        #check code limit
        if order and coupon_code and promotion_program and promotion_program.limit_per_customer:
            partner_lst = [order.partner_id.id]
            if order.partner_id.phone:
                partner_ids = self.env['res.partner'].search([('phone','=',order.partner_id.phone)])
                if partner_ids:
                    for related_partner in partner_ids:
                        partner_lst.append(related_partner.id)
            final_partner_ids = self.env['res.partner'].browse(partner_lst)
            order_lst = []
            for each in final_partner_ids:
                promo_code_lst = []
                if promotion_program.promo_code:
                    promo_code_lst.append(promotion_program.promo_code)
                if promotion_program.code_in_chines:
                    promo_code_lst.append(promotion_program.code_in_chines)
                if promotion_program.other_program_ids:
                    for related_program in promotion_program.other_program_ids:
                        if related_program.promo_code:
                            promo_code_lst.append(related_program.promo_code)
                        if related_program.code_in_chines:
                            promo_code_lst.append(related_program.code_in_chines)
                search_domain = [('order_id.state', 'in', ['sale', 'done']), ('order_id.partner_id', '=', each.id), ('order_id.id', '!=', order.id),'|',('promo_code','in',promo_code_lst),('promo_code_chines','=',promo_code_lst)]
                sale_line_ids = self.env['sale.order.line'].search(search_domain)
                if sale_line_ids:
                    for sale_line in sale_line_ids:
                        if sale_line.order_id.id not in order_lst:
                            order_lst.append(sale_line.order_id.id)
            if order_lst and len(order_lst) >= promotion_program.limit_per_customer:
                return {'error': _('The promo code is already used')}

        if self.maximum_use_number != 0 and self.order_count >= self.maximum_use_number:
            message = {'error': _('Promo code %s has been expired.') % (coupon_code)}
        elif not self._filter_on_mimimum_amount(order):
            message = {'error': _(
                'A minimum of %(amount)s %(currency)s should be purchased to get the reward',
                amount=self.rule_minimum_amount,
                currency=self.currency_id.name
            )}
        elif self.promo_code and self.promo_code == order.promo_code:
            message = {'error': _('The promo code is already applied on this order')}
        elif self.promo_code and order.order_line and order.order_line.filtered(lambda l:l.promo_code==coupon_code or l.promo_code_chines==coupon_code):
            message = {'error': _('The promo code is already applied on this order')}
        elif self in order.no_code_promo_program_ids:
            message = {'error': _('The promotional offer is already applied on this order')}
        elif not self.active:
            message = {'error': _('Promo code is invalid')}
        elif self.rule_date_from and self.rule_date_from > fields.Datetime.now() or self.rule_date_to and fields.Datetime.now() > self.rule_date_to:
            message = {'error': _('Promo code is expired')}
        elif order.promo_code and promotion_program and not promotion_program.allow_cumulative:
            message = {'error': _('Promotionals codes are not cumulative.')}
        # elif order.promo_code and self.promo_code_usage == 'code_needed':
        #     message = {'error': _('Promotionals codes are not cumulative.')}
        elif self._is_global_discount_program() and order._is_global_discount_already_applied():
            message = {'error': _('Global discounts are not cumulative.')}
        elif self.promo_applicability == 'on_current_order' and self.reward_type == 'product' and not order._is_reward_in_order_lines(self):
            message = {'error': _('The reward products should be in the sales order lines to apply the discount.')}
        elif not self._is_valid_partner(order.partner_id):
            message = {'error': _("The customer doesn't have access to this reward.")}
        elif not self._filter_programs_on_products(order):
            message = {'error': _("You don't have the required product quantities on your sales order. If the reward is same product quantity, please make sure that all the products are recorded on the sales order (Example: You need to have 3 T-shirts on your sales order if the promotion is 'Buy 2, Get 1 Free'.")}
        elif self.promo_applicability == 'on_current_order' and not self.env.context.get('applicable_coupon'):
            applicable_programs = order._get_applicable_programs()
            if self not in applicable_programs:
                message = {'error': _('At least one of the required conditions is not met to get the reward!')}
        return message

