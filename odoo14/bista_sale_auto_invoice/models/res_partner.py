# -*- encoding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2020 (http://www.bistasolutions.com)
#
##############################################################################

from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    auto_create_invoice = fields.Boolean("Auto Create Customer Invoice", help='Select Checkbox to Create Auto Invoice for this Customer')
    auto_validate_invoice = fields.Boolean("Auto Validate Customer Invoice", help='Select Checkbox to Auto Validate Invoice for this Customer')
    auto_send_mail_invoice = fields.Boolean("Auto Send Mail Customer Invoice", help='Select Checkbox to Auto Send Invoice Mail for this Customer')
