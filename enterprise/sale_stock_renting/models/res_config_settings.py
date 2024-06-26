# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Padding Time

    padding_time = fields.Float(string="Padding", related='company_id.padding_time', readonly=False,
                                help="Amount of time (in hours) during which a product is considered unavailable prior to renting (preparation time).")

    @api.onchange('padding_time')
    def _onchange_padding_time(self):
        self.env['ir.property']._set_default("preparation_time", "product.template", self.padding_time)
