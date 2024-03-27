# -*- encoding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2019 (http://www.bistasolutions.com)
#
##############################################################################

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    auto_create_invoice = fields.Boolean(
        "Auto Create Customer Invoice", related='company_id.auto_create_invoice', readonly=False, help='Allow to create customer invoice automatically while delivery order validated')
    auto_validate_invoice = fields.Boolean(
        "Auto Validate Customer Invoice", related='company_id.auto_validate_invoice', readonly=False, help='Validate Customer Invoice Automatically')
    auto_send_mail_invoice = fields.Boolean(
        "Auto Send Mail Customer Invoice", related='company_id.auto_send_mail_invoice', readonly=False, help='Auto Send Invoice Mail to Customer')

    @api.onchange('auto_create_invoice')
    def onchange_auto_create_invoice(self):
        if not self.auto_create_invoice and (self.auto_validate_invoice or self.auto_send_mail_invoice):
            self.auto_validate_invoice = False
            self.auto_send_mail_invoice = False

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        Ir_config_param = self.env['ir.config_parameter'].sudo()
        res.update(auto_create_invoice=Ir_config_param.get_param('auto_create_invoice'),
                   auto_validate_invoice=Ir_config_param.get_param('auto_validate_invoice'),
                   auto_send_mail_invoice=Ir_config_param.get_param('auto_send_mail_invoice'))
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('auto_create_invoice', self.auto_create_invoice)
        params.set_param('auto_validate_invoice', self.auto_validate_invoice)
        params.set_param('auto_send_mail_invoice', self.auto_send_mail_invoice)
