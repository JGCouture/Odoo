#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################

import base64

import json
from odoo import SUPERUSER_ID
from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(['/update/order/info/'], type='json', auth="public", methods=['POST'] , website=True)
    def update_order_info_common(self, sale_id, find_us_pay,order_type_pay, agent_select_pay, ref_pay_pay, online_add_pay, text_other_add_pay):
        so_id = request.env['sale.order'].sudo().browse(int(sale_id))
        if so_id:
            if order_type_pay:
                so_id.sale_order_type = order_type_pay

            if agent_select_pay:
                so_id.x_studio_many2one_field_8mpil = int(agent_select_pay)

            if find_us_pay and find_us_pay == 'referral' and ref_pay_pay:
                so_id.find_ref = find_us_pay
                so_id.referal_code = ref_pay_pay

            elif find_us_pay and find_us_pay == 'online_ad' and online_add_pay and online_add_pay != 'other':
                so_id.find_ref = find_us_pay
                so_id.online_add = online_add_pay

            elif find_us_pay and find_us_pay == 'online_ad' and online_add_pay and online_add_pay == 'other':
                so_id.find_ref = find_us_pay
                so_id.online_add = online_add_pay
                so_id.other_add = text_other_add_pay

    @http.route(['/check/required/document/'], type='json', auth="public", methods=['POST'] , website=True)
    def get_required_document(self, sale_id):
        so_id = request.env['sale.order'].sudo().browse(int(sale_id))
        doc_lst = []
        if so_id.order_line:
            so_lines = so_id.order_line.filtered(lambda l:l.product_id and l.product_id.required_doc_ids)
            if so_lines:
                for each in so_lines:
                    for doc in each.product_id.required_doc_ids:
                        if doc.name not in doc_lst:
                            doc_lst.append(doc.name)
        attachment_ids = request.env['ir.attachment'].sudo().search([('is_web_attachment','=', True),('res_model', '=', 'sale.order'), ('res_id', '=', int(sale_id))])
        if doc_lst:
            attachment = 0
            if attachment_ids:
                attachment = len(attachment_ids)
            if attachment < len(doc_lst):
                str = "Please upload following documents!\n"
                str += ',\n'.join(doc_lst)
                return str
        else:
            return False


    @http.route('/shop/payment/file_upload', type='http', auth="public", methods=['POST'], website=True)
    def shop_file_upload(self, **post):
        if post.get('Upload-File'):
            data = {
                'attachments': []
            }
            orphan_attachment_ids = []
            for field_name, field_value in post.items():
                if hasattr(field_value, 'filename'):
                    field_name = field_name.rsplit('[', 1)[0]
                    field_value.field_name = field_name
                    data['attachments'].append(field_value)

            order = request.website.sale_get_order()
            if order:
                for file in data['attachments']:

                    custom_field = None
                    attachment_value = {
                        'name': file.field_name if custom_field else file.filename,
                        'datas': base64.encodestring(file.read()),
                        'store_fname': file.filename,
                        'res_model': 'sale.order',
                        'res_id': order.id,
                        'is_web_attachment': True
                    }
                    attachment_id = request.env['ir.attachment'].sudo().create(attachment_value)
                    orphan_attachment_ids.append(attachment_id.id)
                    if orphan_attachment_ids:
                        values = {
                            'body': _('<p>Attached files : </p>'),
                            'model': 'sale.order',
                            'message_type': 'comment',
                            'no_auto_thread': False,
                            'res_id': order.id,
                            'attachment_ids': [(6, 0, orphan_attachment_ids)],
                        }
                        mail_id = request.env['mail.message'].sudo().create(values)
            else:
                return request.redirect("/shop")
            return request.redirect("/shop/payment?success=1")
        return request.redirect("/shop/payment?success=0")

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        res = super(WebsiteSale, self).payment(**post)
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        order = request.website.sale_get_order()
        attachment_objs = request.env['ir.attachment'].sudo().search([('res_model', '=', 'sale.order'), ('res_id', '=', order.id)])
        if attachment_objs:
            res.qcontext['attachment_objs'] = attachment_objs
        if post.get('success'):
            res.qcontext['upload_success'] = str(post.get('success'))
        return res

    @http.route('/shop/payment/remove_upload', type='json', auth="public", website=True)
    def remove_file_upload(self, attachment_id, **post):
        if attachment_id:
            attachment_obj = request.env['ir.attachment'].sudo().browse(attachment_id)
            order = request.website.sale_get_order()
            if attachment_obj:
                attachment_obj.sudo().unlink()
                values = {
                    'body': _('<p>Attached removed.</p>'),
                    'model': 'sale.order',
                    'message_type': 'comment',
                    'no_auto_thread': False,
                    'res_id': order.id,
                }
                mail_id = request.env['mail.message'].sudo().create(values)
        return True
