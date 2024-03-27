# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _remove_invalid_reward_lines(self):
        """ Find programs & coupons that are not applicable anymore.
            It will then unlink the related reward order lines.
            It will also unset the order's fields that are storing
            the applied coupons & programs.
            Note: It will also remove a reward line coming from an archive program.
        """
        self.ensure_one()
        order = self

        applied_programs = order._get_applied_programs()
        applicable_programs = self.env['coupon.program']
        if applied_programs:
            applicable_programs = order._get_applicable_programs() + order._get_valid_applied_coupon_program()
            applicable_programs = applicable_programs._keep_only_most_interesting_auto_applied_global_discount_program()
        programs_to_remove = applied_programs - applicable_programs

        reward_product_ids = applicable_programs.discount_line_product_id.ids
        # delete reward line coming from an archived coupon (it will never be updated/removed when recomputing the order)
        invalid_lines = order.order_line.filtered(lambda line: line.is_reward_line and line.product_id.id not in reward_product_ids)

        if programs_to_remove:
            product_ids_to_remove = programs_to_remove.discount_line_product_id.ids

            if product_ids_to_remove:
                # Invalid generated coupon for which we are not eligible anymore ('expired' since it is specific to this SO and we may again met the requirements)
                self.generated_coupon_ids.filtered(lambda coupon: coupon.program_id.discount_line_product_id.id in product_ids_to_remove).write({'state': 'expired'})

            # Reset applied coupons for which we are not eligible anymore ('valid' so it can be use on another )
            coupons_to_remove = order.applied_coupon_ids.filtered(lambda coupon: coupon.program_id in programs_to_remove)
            coupons_to_remove.write({'state': 'new'})

            # Unbind promotion and coupon programs which requirements are not met anymore
            order.no_code_promo_program_ids -= programs_to_remove
            order.code_promo_program_id -= programs_to_remove

            if coupons_to_remove:
                order.applied_coupon_ids -= coupons_to_remove

            # Remove their reward lines
            if product_ids_to_remove:
                invalid_lines |= order.order_line.filtered(lambda line: line.product_id.id in product_ids_to_remove)

        invalid_lines.unlink()

    def _create_reward_line(self, program):
        vals = self._get_reward_line_values(program)
        for each in vals:
            if program.promo_code_usage == 'code_needed':
                each['promo_code'] = program.promo_code
                if program.code_in_chines:
                    each['promo_code_chines'] = program.code_in_chines
        self.write({'order_line': [(0, False, value) for value in vals]})

    def _get_reward_values_discount(self, program):
        if program.discount_type == 'fixed_amount':
            taxes = program.discount_line_product_id.taxes_id
            if self.fiscal_position_id:
                taxes = self.fiscal_position_id.map_tax(taxes)
            return [{
                'name': _("Discount: %s", program.name),
                'product_id': program.discount_line_product_id.id,
                'price_unit': - self._get_reward_values_discount_fixed_amount(program),
                'product_uom_qty': 1.0,
                'product_uom': program.discount_line_product_id.uom_id.id,
                'is_reward_line': True,
                'tax_id': [(4, tax.id, False) for tax in taxes],
            }]
        reward_dict = {}
        lines = self._get_paid_order_lines()
        amount_total = sum(self._get_base_order_lines(program).mapped('price_subtotal'))
        if program.discount_apply_on == 'cheapest_product':
            line = self._get_cheapest_line()
            if line:
                discount_line_amount = min(line.price_reduce * (program.discount_percentage / 100), amount_total)
                if discount_line_amount:
                    taxes = self.fiscal_position_id.map_tax(line.tax_id)

                    reward_dict[line.tax_id] = {
                        'name': _("Discount: %s", program.name),
                        'product_id': program.discount_line_product_id.id,
                        'price_unit': - discount_line_amount if discount_line_amount > 0 else 0,
                        'product_uom_qty': 1.0,
                        'product_uom': program.discount_line_product_id.uom_id.id,
                        'is_reward_line': True,
                        'tax_id': [(4, tax.id, False) for tax in taxes],
                    }
        elif program.discount_apply_on in ['specific_products', 'on_order']:
            if program.discount_apply_on == 'specific_products':
                # We should not exclude reward line that offer this product since we need to offer only the discount on the real paid product (regular product - free product)
                free_product_lines = self.env['coupon.program'].search([('reward_type', '=', 'product'), ('reward_product_id', 'in', program.discount_specific_product_ids.ids)]).mapped('discount_line_product_id')
                lines = lines.filtered(lambda x: x.product_id in (program.discount_specific_product_ids | free_product_lines))
                if program.discount_most_expensive and lines and len(lines) > 1:
                    lines = lines
                    price = 0
                    for sol in lines:
                        if sol.price_unit > price:
                            lines = sol
                        price = sol.price_unit
            # when processing lines we should not discount more than the order remaining total
            currently_discounted_amount = 0
            for line in lines:
                discount_line_amount = min(self._get_reward_values_discount_percentage_per_line(program, line), amount_total - currently_discounted_amount)

                if discount_line_amount:

                    if line.tax_id in reward_dict:
                        reward_dict[line.tax_id]['price_unit'] -= discount_line_amount
                    else:
                        taxes = self.fiscal_position_id.map_tax(line.tax_id)

                        reward_dict[line.tax_id] = {
                            'name': _(
                                "Discount: %(program)s - On product with following taxes: %(taxes)s",
                                program=program.name,
                                taxes=", ".join(taxes.mapped('name')),
                            ),
                            'product_id': program.discount_line_product_id.id,
                            'price_unit': - discount_line_amount if discount_line_amount > 0 else 0,
                            'product_uom_qty': 1.0,
                            'product_uom': program.discount_line_product_id.uom_id.id,
                            'is_reward_line': True,
                            'tax_id': [(4, tax.id, False) for tax in taxes],
                        }
                        currently_discounted_amount += discount_line_amount

        # If there is a max amount for discount, we might have to limit some discount lines or completely remove some lines
        max_amount = program._compute_program_amount('discount_max_amount', self.currency_id)
        if max_amount > 0:
            amount_already_given = 0
            for val in list(reward_dict):
                amount_to_discount = amount_already_given + reward_dict[val]["price_unit"]
                if abs(amount_to_discount) > max_amount:
                    reward_dict[val]["price_unit"] = - (max_amount - abs(amount_already_given))
                    add_name = formatLang(self.env, max_amount, currency_obj=self.currency_id)
                    reward_dict[val]["name"] += "( " + _("limited to ") + add_name + ")"
                amount_already_given += reward_dict[val]["price_unit"]
                if reward_dict[val]["price_unit"] == 0:
                    del reward_dict[val]
        return reward_dict.values()

    def _update_existing_reward_lines(self):
        '''Update values for already applied rewards'''
        def update_line(order, lines, values):
            '''Update the lines and return them if they should be deleted'''
            lines_to_remove = self.env['sale.order.line']
            # Check commit 6bb42904a03 for next if/else
            # Remove reward line if price or qty equal to 0
            if values['product_uom_qty'] and values['price_unit']:
                lines.write(values)
            else:
                if program.reward_type != 'free_shipping':
                    # Can't remove the lines directly as we might be in a recordset loop
                    lines_to_remove += lines
                else:
                    values.update(price_unit=0.0)
                    lines.write(values)
            return lines_to_remove

        self.ensure_one()
        order = self
        applied_programs = order._get_applied_programs_with_rewards_on_current_order()
        program_lst = []
        if applied_programs:
            for each_prog in applied_programs:
                program_lst.append(each_prog)
        if self.order_line:
            program_apply_lines = self.order_line.filtered(lambda l:l.promo_code or l.promo_code_chines)
            if program_apply_lines:
                for each_l in program_apply_lines:
                    program_id = False
                    if each_l.promo_code:
                        program_id = self.env['coupon.program'].search([('promo_code','=',each_l.promo_code),('promo_code_usage','=','code_needed')])
                    if not program_id and each_l.promo_code_chines:
                        program_id = self.env['coupon.program'].search([('code_in_chines', '=', each_l.promo_code_chines), ('promo_code_usage', '=', 'code_needed')])
                    if program_id and program_id[0] not in program_lst:
                        program_lst.append(program_id[0])
        for program in program_lst:
            values = order._get_reward_line_values(program)
            lines = order.order_line.filtered(lambda line: line.product_id == program.discount_line_product_id)
            if program.reward_type == 'discount' and program.discount_type == 'percentage':
                lines_to_remove = lines
                # Values is what discount lines should really be, lines is what we got in the SO at the moment
                # 1. If values & lines match, we should update the line (or delete it if no qty or price?)
                # 2. If the value is not in the lines, we should add it
                # 3. if the lines contains a tax not in value, we should remove it
                for value in values:
                    value_found = False
                    for line in lines:
                        # Case 1.
                        if not len(set(line.tax_id.mapped('id')).symmetric_difference(set([v[1] for v in value['tax_id']]))):
                            value_found = True
                            # Working on Case 3.
                            lines_to_remove -= line
                            lines_to_remove += update_line(order, line, value)
                            continue
                    # Case 2.
                    if not value_found:
                        order.write({'order_line': [(0, False, value)]})
                # Case 3.
                lines_to_remove.unlink()
            else:
                update_line(order, lines, values[0]).unlink()



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    promo_code = fields.Char('Promo Code')
    promo_code_chines = fields.Char('Promo Code Chines')