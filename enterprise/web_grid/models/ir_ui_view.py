# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('grid', "Grid")])

    @api.model
    def _postprocess_access_rights(self, model, node):
        """ Override prost processing to add specific action access check for
        grid view. """
        super(View, self)._postprocess_access_rights(model, node)

        if node.tag == 'grid':
            # testing ACL as real user
            Model = self.env[model].sudo(False)
            is_base_model = self.env.context.get('base_model_name', model) == model
            for action, operation in (('create', 'create'), ('delete', 'unlink'), ('edit', 'write')):
                if (not node.get(action) and
                        not Model.check_access_rights(operation, raise_exception=False) or
                        not self._context.get(action, True) and is_base_model):
                    node.set(action, 'false')
