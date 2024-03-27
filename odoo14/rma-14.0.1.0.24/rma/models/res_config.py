# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class RmaConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_quote_cancellation = fields.Boolean(
        string="Allow cancellation of order quote.", help="Customer can cancel quotation order.")
    process_do_state = fields.Selection([
        ('all', 'All'),
        ('done', 'Only Done'),
    ], string="Process state")
    rma_term_condition = fields.Html(string="Term And Conditions")
    days_for_rma = fields.Integer(string="Return Policy",
                                  help="Number of days upto which customer can request for RMA after delivery done.")
    rma_day_apply_on = fields.Selection(
        [("so_date", "Order Date"), ("do_date", "Delivery Date")], string="Apply On")
    module_repair = fields.Boolean(
        "Allow repair of product in RMA.", help='Allows to manage all product repairs.\n')
    repair_location_id = fields.Many2one(
        'stock.location', 'Repair Location')
    show_rma_stage = fields.Boolean(string="Show RMA stage to customer.")

    def set_values(self):
        super(RmaConfigSettings, self).set_values()
        ir_default = self.env['ir.default'].sudo()
        ir_default.set('res.config.settings', 'allow_quote_cancellation', self.allow_quote_cancellation)
        ir_default.set('res.config.settings', 'process_do_state', self.process_do_state)
        ir_default.set('res.config.settings', 'show_rma_stage', self.show_rma_stage)
        return True

    @api.model
    def get_values(self):
        res = super(RmaConfigSettings, self).get_values()
        ir_default = self.env['ir.default'].sudo()
        allow_quote_cancellation = ir_default.get('res.config.settings', 'allow_quote_cancellation')
        process_do_state = ir_default.get('res.config.settings', 'process_do_state')
        show_rma_stage = ir_default.get('res.config.settings', 'show_rma_stage')
        res.update({
            'allow_quote_cancellation': allow_quote_cancellation,
            'process_do_state': process_do_state,
            "show_rma_stage": show_rma_stage,
        })
        return res
