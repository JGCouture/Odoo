# -*- coding: utf-8 -*-

from odoo import api, models, fields,_
from odoo.exceptions import ValidationError


class RentalProcessingLine(models.TransientModel):
    _inherit = 'rental.order.wizard.line'

    def _apply(self):
        res = super(RentalProcessingLine, self)._apply()
        for wizard_line in self:
            if wizard_line.status == 'return' and wizard_line.qty_returned and wizard_line.product_id.rental_subscription_prod_id:
                order_id = self.env['sale.order'].browse(self._context.get('default_order_id'))
                lst = []
                for each in order_id.order_line:
                    order_line = each.order_id.order_line.filtered(lambda l:l.product_id == wizard_line.product_id.rental_subscription_prod_id and l.subscription_id)
                    if order_line and len(order_line) > 1:
                        if order_line not in lst:
                            lst.append(order_line)
                    if order_line and len(order_line) == 1:
                        for line in order_line:
                            if line.subscription_id and not each.subscription_id.close_reason_id:
                                line.subscription_id.close_reason_id = self.env.ref('zbs_close_subscription.rental_order_returned').id
                                line.subscription_id.sudo().set_close()
                if lst:
                    msg = "Please manually close the subscription for the product : " + lst[0][0].product_id.name
                    each.order_id.message_post(body=msg)
        return res