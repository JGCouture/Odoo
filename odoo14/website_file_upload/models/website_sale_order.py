#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################

from odoo import SUPERUSER_ID
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    attachment_count = fields.Integer(
        compute='_get_attachment_count', string="Number of Attachments")

    def _get_attachment_count(self):
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'sale.order'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attach_data = dict((res['res_id'], res['res_id_count'])
                           for res in read_group_res)

        for record in self:
            record.attachment_count = attach_data.get(record.id, 0)

    def attachment_tree_view_action(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {
            'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(
            ['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        return action

    def get_required_doc(self):
        doc_lst = []
        so_id = self
        if so_id.order_line:
            so_lines = so_id.order_line.filtered(lambda l: l.product_id and l.product_id.required_doc_ids)
            if so_lines:
                for each in so_lines:
                    for doc in each.product_id.required_doc_ids:
                        if doc.name not in doc_lst:
                            doc_lst.append(doc.name)
        if doc_lst:
            return len(doc_lst)
        else:
            return 0

    def get_required_doc_list(self):
        doc_lst = []
        so_id = self
        if so_id.order_line:
            so_lines = so_id.order_line.filtered(lambda l: l.product_id and l.product_id.required_doc_ids)
            if so_lines:
                for each in so_lines:
                    for doc in each.product_id.required_doc_ids:
                        if doc.name not in doc_lst:
                            doc_lst.append(doc.name)
        if doc_lst:
            str = 'Please Upload Documents'
            for doc_l in doc_lst:
                str += "\n" + doc_l
            return str
        else:
            return ''


class IrAttachement(models.Model):
    _inherit = 'ir.attachment'

    is_web_attachment = fields.Boolean(string="Website Attachment?")