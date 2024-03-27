# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    referal_code = fields.Char(string="Referral", tracking=True)
    find_ref = fields.Selection([
        ('agent', 'Agent'),
        ('referral', 'Referral'),
        ('online_ad', 'Online Ads')
    ], string="How did you find us?", tracking=True)
    online_add = fields.Selection([
        ('wechat', 'WeChat'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('other', 'Other')
    ], string="Find By",tracking=True)
    other_add = fields.Char(string="Online Add Other", tracking=True)
    online_form_count = fields.Integer(string="Ordering Form", compute="get_online_form_count")

    def get_online_form_count(self):
        self.online_form_count = 0
        online_ordering_id = self.env['online.order'].search([('sale_order_id', '=', self.id)])
        if online_ordering_id:
            self.online_form_count = len(online_ordering_id)

    def action_view_online_form(self):
        online_ordering_id = self.env['online.order'].search([('sale_order_id', '=', self.id)])
        return {
            'name': 'Online Ordering Form',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'online.order',
            'domain': [('id', 'in', online_ordering_id.ids)],
        }

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if vals.get('state') and vals.get('state') in ['sent','sale','done']:
            online_form_id = self.env['online.order'].sudo().search([('sale_order_id','=', self.id),('active','=',False)])
            if online_form_id:
                online_form_id.active = True
        return res

    def check_term_condition_required(self):
        template_lst = []
        if self.order_line:
            for each in self.order_line:
                template_ids = self.env['pos.term.template'].sudo().search([('product_ids','in', each.product_id.id)])
                for tmpl in template_ids:
                    if tmpl not in template_lst:
                        template_lst.append(tmpl)
        if template_lst:
            return template_lst
        else:
            return False

    def get_term_template(self):
        template_lst = []
        if self.order_line:
            for each in self.order_line:
                template_ids = self.env['pos.term.template'].sudo().search([('product_ids','in', each.product_id.id)])
                for tmpl in template_ids:
                    if tmpl not in template_lst:
                        template_lst.append(tmpl)
        if template_lst:
            return template_lst
        else:
            return False


    def get_product_links(self):
        links = {}
        if self.order_line:
            order_lines =  self.order_line.filtered(lambda l:l.product_id.hyper_link_ids)
            if order_lines:
                for each in order_lines:
                    for link in each.product_id.hyper_link_ids:
                        links[link.name] = link.url
        if links:
            return links
        else:
            return False

    def get_so_user_activity(self):
        activity_ids = self.env['mail.activity'].sudo().search([('res_model', '=', 'sale.order'), ('res_id', '=', self.id),('summary', '!=', False)], order="date_deadline")
        data_lst = []
        for activity in activity_ids:
            data_lst.append({
                'name': activity.summary,
                'date': activity.date_deadline.strftime('%m/%d/%Y'),
            })
        return data_lst