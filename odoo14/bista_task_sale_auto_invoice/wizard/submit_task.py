# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class MessageWizard(models.TransientModel):
    _name = 'submit.task.message'
    _description = "Apply ALL"

    def action_ok(self):
        """ close wizard"""
        return True
