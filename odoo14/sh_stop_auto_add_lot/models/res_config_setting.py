# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_stop_auto_add_lot = fields.Boolean("Stop Auto add lot/serial ?")


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_stop_auto_add_lot = fields.Boolean(
        "Stop Auto add lot/serial ?",
        related='company_id.sh_stop_auto_add_lot',
        readonly=False
    )