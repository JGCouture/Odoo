# -*- coding: utf-8 -*-

from odoo import api, models, fields,_
from datetime import  date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        self.date_cancel = date.today()
        return res