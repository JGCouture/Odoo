# -*- coding: utf-8 -*-

from odoo import api, models, fields,_


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_order_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
        return base_url

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.x_studio_many2one_field_8mpil and self.x_studio_many2one_field_8mpil.work_email:
            template = self.env.ref('zbs_agent_confirmation_email.email_template_agent_sale_order_confirmation')
            template.send_mail(self.id, force_send=True)
        if self.x_studio_many2one_field_8mpil.parent_id and self.x_studio_many2one_field_8mpil.parent_id.work_email:
            try:
                template = self.env.ref('zbs_agent_confirmation_email.email_template_agent_manager_order_confirmation')
                template.send_mail(self.id, force_send=True)
            except:
                pass
        return res


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def get_order_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
        return base_url