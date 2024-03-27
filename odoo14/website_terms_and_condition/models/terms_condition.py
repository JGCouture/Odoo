# -*- coding: utf-8 -*-

from odoo import models, fields, _


class Website(models.Model):
    _inherit = 'website'

    terms_and_conditions = fields.Html(string='Description')
