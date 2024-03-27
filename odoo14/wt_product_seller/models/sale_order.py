# -*- coding: utf-8 -*-

from odoo import models, fields, _, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_seller = fields.Boolean('Is seller?')
    seller_partner_id = fields.Many2one('res.partner', 'Partner')
    date_order = fields.Datetime(string='Order Date', required=True, readonly=False, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of cnfirmed orders.")


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.seller_partner_id:
            self.partner_id = self.seller_partner_id.id
        return super(SaleOrder, self).onchange_partner_id()