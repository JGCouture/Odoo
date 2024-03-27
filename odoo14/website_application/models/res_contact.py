# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo import api, fields, models


class ResContact(models.Model):
    _inherit = 'res.partner'

    ach_form_pdf = fields.Binary(string="ACH Form")
