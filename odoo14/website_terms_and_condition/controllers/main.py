# -*- coding: utf-8 -*-

from odoo import http
import logging
import base64
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import Forbidden, NotFound
_logger = logging.getLogger(__name__)
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.exceptions import ValidationError
from odoo.http import request, Response, JsonRequest
import json


class WebsiteSale(WebsiteSale):

    @http.route(['/check/term/'], type='json', auth="public", methods=['POST'] , website=True)
    def check_pos_term_condition(self, order):
        order_id = request.env['sale.order'].sudo().browse(int(order))
        res = False
        if order_id:
            res = order_id.check_term_condition_required()
        return res

    @http.route(['/get/signup/states/'], type='json', auth="public", methods=['POST'] , website=True)
    def get_country_states(self, country_id):
        state_dict = {}
        state_ids = request.env['res.country.state'].sudo().search([('country_id','=',int(country_id))])
        if state_ids:
            for each in state_ids:
                state_dict[each.id] = each.name
        return state_dict

    def _get_mandatory_billing_fields(self):
        # deprecated for _get_mandatory_fields_billing which handle zip/state required
        return ["name", "email", "street", "country_id", 'city', 'x_studio_owner_name', 'mobile']

    def _get_mandatory_shipping_fields(self):
        return ["name", "street", "country_id", 'city', 'x_studio_owner_name', 'mobile']

    def format_phone_number(self, phone):
        return phone[:3] + '-' + phone[3:6] + '-' + phone[6:10]

    def _checkout_form_save(self, mode, checkout, all_values):
        Partner = request.env['res.partner']
        if all_values.get('mobile'):
            checkout['mobile'] = all_values['mobile']
        if all_values.get('phone'):
            checkout['phone'] = all_values.get('phone')

        if mode[0] == 'new':
            if all_values.get('online_add'):
                checkout['online_add'] = all_values.get('online_add')
            if all_values.get('x_studio_lead_id'):
                checkout['x_studio_lead_id'] = all_values['x_studio_lead_id']
            if all_values.get('x_studio_owner_name'):
                checkout['x_studio_owner_name'] = all_values['x_studio_owner_name']
            if all_values.get('find_ref'):
                checkout['find_ref'] = all_values['find_ref']
            if all_values.get('x_studio_agent'):
                checkout['x_studio_agent'] = all_values['x_studio_agent']
            partner_id = Partner.sudo().with_context(tracking_disable=True).create(checkout).id
        elif mode[0] == 'edit':
            partner_id = int(all_values.get('partner_id', 0))
            if partner_id:
                exist_partner_id = request.env['res.partner'].sudo().browse(partner_id)
                if exist_partner_id:
                    if not exist_partner_id.sudo().x_studio_agent and all_values.get('x_studio_agent'):
                        checkout['x_studio_agent'] = all_values['x_studio_agent']
                    if all_values.get('x_studio_lead_id'):
                        checkout['x_studio_lead_id'] = all_values['x_studio_lead_id']
                    if all_values.get('x_studio_owner_name'):
                        checkout['x_studio_owner_name'] = all_values['x_studio_owner_name']
                order = request.website.sale_get_order()
                shippings = Partner.sudo().search([("id", "child_of", order.partner_id.commercial_partner_id.ids)])
                if partner_id not in shippings.mapped('id') and partner_id != order.partner_id.id:
                    return Forbidden()
                Partner.browse(partner_id).sudo().write(checkout)
        return partner_id

    @http.route(['/shop/payment'], type='http', auth="public", website=True, sitemap=False)
    def payment(self, **post):
        res = super(WebsiteSale, self).payment(**post)
        if res and res.qcontext['website_sale_order']:
            for so_line in res.qcontext['website_sale_order'].order_line:
                if res.qcontext['website_sale_order'].order_line:
                    special_lines = res.qcontext['website_sale_order'].order_line.filtered(lambda l:l.product_id.special_diacount_applicable)
                    subscription_lines = res.qcontext['website_sale_order'].order_line.filtered(
                        lambda l: l.product_id.recurring_invoice)
                    online_order_id = request.env['online.order'].search(
                        [('active', '=', False), ('sale_order_id', '=', res.qcontext['website_sale_order'].id)])
                    ach_form_id = request.env['ach.form'].sudo().search(
                        [('sale_order_id', '=', res.qcontext['website_sale_order'].id)], limit=1,
                        order="write_date desc")
                    kwickpos_online_order = request.env['online.order.form'].sudo().search(
                        [('sale_order_id', '=', res.qcontext['website_sale_order'].id)], limit=1,
                        order="write_date desc")
                    if special_lines:
                        res.qcontext['special_disc'] = True
                        if online_order_id:
                            res.qcontext['form_fill'] = 'checked'
                            res.qcontext['need_website'] = online_order_id.need_website
                            res.qcontext['menu_other'] = online_order_id.menu_other
                            res.qcontext['website_address'] = online_order_id.website_address
                            res.qcontext['monday'] = online_order_id.monday
                            res.qcontext['tuesday'] = online_order_id.tuesday
                            res.qcontext['wednesday'] = online_order_id.wednesday
                            res.qcontext['thursday'] = online_order_id.thursday
                            res.qcontext['friday'] = online_order_id.friday
                            res.qcontext['saturday'] = online_order_id.saturday
                            res.qcontext['sunday'] = online_order_id.sunday
                            res.qcontext['monday_shift2'] = online_order_id.monday_shift2
                            res.qcontext['tuesday_shift2'] = online_order_id.tuesday_shift2
                            res.qcontext['wednesday_shift2'] = online_order_id.wednesday_shift2
                            res.qcontext['thursday_shift2'] = online_order_id.thursday_shift2
                            res.qcontext['friday_shift2'] = online_order_id.friday_shift2
                            res.qcontext['saturday_shift2'] = online_order_id.saturday_shift2
                            res.qcontext['sunday_shift2'] = online_order_id.sunday_shift2
                            res.qcontext['sale_tax'] = online_order_id.sale_tax
                            res.qcontext['need_chinese'] = online_order_id.need_chinese
                            res.qcontext['email_address'] = online_order_id.email_address
                            res.qcontext['backup_phone_number'] = online_order_id.backup_phone_number
                            res.qcontext['do_delivery'] = online_order_id.do_delivery
                            res.qcontext['plan_choice'] = online_order_id.plan_choice
                            res.qcontext['notification_choice'] = online_order_id.order_notification
                            res.qcontext['min_order_amount'] = online_order_id.min_order_amount
                            res.qcontext['payment_option'] = online_order_id.payment_option
                            res.qcontext['delivery_free'] = online_order_id.delivery_free
                            res.qcontext['delivery_distance'] = online_order_id.delivery_distance
                            res.qcontext['pickup_order_time'] = online_order_id.pickup_order_time
                            res.qcontext['delivery_order_time'] = online_order_id.delivery_order_time
                            res.qcontext['use_google_business'] = online_order_id.use_google_business
                        if kwickpos_online_order:
                            res.qcontext['customer_id'] = kwickpos_online_order.customer_id
                            res.qcontext['pos_system'] = kwickpos_online_order.pos_system
                            res.qcontext['kwickpos_plan_choice'] = kwickpos_online_order.plan_choice
                            res.qcontext['if_cash_discount'] = kwickpos_online_order.if_cash_discount
                            res.qcontext['company_name'] = kwickpos_online_order.company_name
                            res.qcontext['ssn'] = kwickpos_online_order.ssn
                            res.qcontext['tax_id'] = kwickpos_online_order.tax_id
                            res.qcontext['bank'] = kwickpos_online_order.bank
                            res.qcontext['account_number'] = kwickpos_online_order.account_number
                            res.qcontext['routing_number'] = kwickpos_online_order.routing_number
                            res.qcontext[
                                'from_application_signature_date'] = kwickpos_online_order.from_application_signature_date
                            res.qcontext[
                                'personal_guarantee_signature_date'] = kwickpos_online_order.personal_guarantee_signature_date
                            res.qcontext[
                                'print_client_business_legal_name'] = kwickpos_online_order.print_client_business_legal_name
                            res.qcontext[
                                'print_name_of_signer'] = kwickpos_online_order.print_name_of_signer
                            res.qcontext[
                                'client_business_principle_title'] = kwickpos_online_order.client_business_principle_title
                            res.qcontext[
                                'client_business_principle_sign_date'] = kwickpos_online_order.client_business_principle_sign_date
                            res.qcontext['date'] = kwickpos_online_order.date
                    if subscription_lines and not special_lines :
                        res.qcontext['is_subscription'] = True
                        if ach_form_id:
                            res.qcontext['BankBranch'] = ach_form_id.bank_branch
                            res.qcontext['BankName'] = ach_form_id.bank_name
                            res.qcontext['Routing'] = ach_form_id.bank_routing
                            res.qcontext['Account'] = ach_form_id.bank_account

                            res.qcontext['ach_form_fill'] = 'checked'

                    else:
                        if online_order_id:
                            online_order_id.sudo().unlink()

            res.qcontext['partner_id'] = res.qcontext['website_sale_order'].partner_id
            res.qcontext['sale_order_id'] = res.qcontext['website_sale_order'].id
            res.qcontext['need_website'] = 'no'
            res.qcontext['need_chinese'] = 'no'
            res.qcontext['plan_choice'] = 'promo'
            res.qcontext['notification_choice'] = 'email'
            res.qcontext['do_delivery'] = 'yes'
            res.qcontext['payment_option'] = 'in_store'
            res.qcontext['use_google_business'] = 'yes'
        return res

    @http.route(['/online/kwickpos_ordering'], type='http', auth='public')
    def kwickpos_online_customer_order(self, **kwargs):
        partner_id = kwargs.get('partner_id')
        partner = request.env['res.partner'].sudo().search([('id', '=', partner_id)])
        dba = partner.name
        email = partner.email
        restaurant_city = partner.city
        restaurant_state = partner.state_id.name
        restaurant_zipcode = partner.zip
        business_phone_number = partner.phone
        company_address = partner.contact_address_complete
        owner_name = partner.x_studio_owner_name
        cell_phone_number = partner.mobile
        sale_order_id = kwargs.get('sale_order_id')
        from_application_signature_date = kwargs.get('from_application_signature_date')
        personal_guarantee_signature_date = kwargs.get('personal_guarantee_signature_date')
        print_client_business_legal_name = kwargs.get('print_client_business_legal_name')
        print_name_of_signer = kwargs.get('print_name_of_signer')
        client_business_principle_title = kwargs.get('client_business_principle_title')
        client_business_principle_sign_date = kwargs.get('client_business_principle_sign_date')
        date = kwargs.get('date')

        need_chinese = kwargs.get('need_chinese')
        need_chinese_dict = {
            "yes": "1",
            "no": "2",
        }
        need_chinese_transfered = need_chinese_dict.get(need_chinese)
        if_cash_discount = kwargs.get('if_cash_discount')
        plan_choice = kwargs.get('plan_choice')
        payment_option = kwargs.get('payment_option')
        payment_option_dict = {
            "in_store": "3",
            "online": "2",
            "instore_online": "1"
        }
        payment_option_transfered = payment_option_dict.get(payment_option)
        bank = kwargs.get('bank')
        account_number = kwargs.get('account_number')
        routing_number = kwargs.get('routing_number')
        bank_id = request.env['res.bank'].sudo().search([('name', '=', bank)])
        if not bank_id:
            bank_id = request.env['res.bank'].sudo().create({'name': bank})
        partner_account = request.env['res.partner.bank'].sudo().search(
            [
                ('acc_number', '=', account_number), ('aba_routing', '=', routing_number)
            ])
        if partner_account:
            partner.write({'bank_ids': [(4, partner_account[0].id)]})
        company_name = kwargs.get('company_name')
        ssn = kwargs.get('ssn')
        tax_id = kwargs.get('tax_id')
        sale_tax = kwargs.get('sale_tax')

        customer_id = kwargs.get('customer_id')
        need_website = kwargs.get('need_website')
        need_website_dict = {
            "no": "1",
            "no1": "2",
            "no3": "3"
        }
        need_website_transfered = need_website_dict.get(need_website)
        website_address = kwargs.get('website_address')
        pos_system = kwargs.get('pos_system')
        language = kwargs.get('menu_other')
        note = kwargs.get('notes')
        try:
            online_order_form_res = request.env['online.order.form'].sudo().create({
                'partner': int(partner_id),
                'customer_id': customer_id,
                'pos_system': pos_system,
                'need_website': need_website_transfered,
                'website_address': website_address,
                'sales_tax': sale_tax,
                'language': language,
                'plan_choice': plan_choice,
                'need_chinese': need_chinese_transfered,
                'payment_option': payment_option_transfered,
                'if_cash_discount': if_cash_discount,
                'bank': bank,
                'account_number': account_number,
                'routing_number': routing_number,
                'note': note,
                'date': date,
                'company_name': company_name,
                'dba': dba,
                'company_address': company_address,
                'city': restaurant_city,
                'state': restaurant_state,
                'zip_code': restaurant_zipcode,
                'business_phone_number': business_phone_number,
                'email': email,
                'tax_id': tax_id,
                'owner_name': owner_name,
                'cell_phone_number': cell_phone_number,
                'ssn': ssn,
                'personal_guarantee_signature_date': personal_guarantee_signature_date,
                'from_application_signature_date': from_application_signature_date,
                'print_client_business_legal_name': print_client_business_legal_name,
                'print_name_of_signer': print_name_of_signer,
                'client_business_principle_title': client_business_principle_title,
                'client_business_principle_sign_date': client_business_principle_sign_date,
            })
            online_order_form_res.write({'sale_order_id': sale_order_id})
            if kwargs.get('kp_online_order_from_application_signature', False):
                from_application_signature = kwargs.get('kp_online_order_from_application_signature', False)
                from_application_signature_content = from_application_signature.split(';')[1]
                from_application_signature_encoded = from_application_signature_content.split(',')[1]
                online_order_form_res.write(
                    {'from_application_signature': from_application_signature_encoded.encode('utf-8')})
            if kwargs.get('kp_online_order_personal_guarantee_signature', False):
                personal_guarantee_signature = kwargs.get('kp_online_order_personal_guarantee_signature', False)
                personal_guarantee_signature_content = personal_guarantee_signature.split(';')[1]
                personal_guarantee_signature_encoded = personal_guarantee_signature_content.split(',')[1]
                online_order_form_res.write(
                    {'personal_guarantee_signature': personal_guarantee_signature_encoded.encode('utf-8')})
            if kwargs.get('kp_online_order_pricing_confirmation_signature', False):
                pricing_confirmation_signature = kwargs.get('kp_online_order_pricing_confirmation_signature', False)
                pricing_confirmation_signature_content = pricing_confirmation_signature.split(';')[1]
                pricing_confirmation_signature_encoded = pricing_confirmation_signature_content.split(',')[1]
                online_order_form_res.write(
                    {'pricing_confirmation_signature': pricing_confirmation_signature_encoded.encode('utf-8')})
            if kwargs.get('kp_online_order_client_initials', False):
                client_initials = kwargs.get('kp_online_order_client_initials', False)
                client_initials_content = client_initials.split(';')[1]
                client_initials_encoded = client_initials_content.split(',')[1]
                online_order_form_res.write({'client_initials': client_initials_encoded.encode('utf-8')})
            if kwargs.get('kp_online_order_client_business_principle_signature', False):
                client_business_principle_signature = kwargs.get('kp_online_order_client_business_principle_signature',
                                                                 False)
                client_business_principle_signature_content = client_business_principle_signature.split(';')[1]
                client_business_principle_signature_encoded = client_business_principle_signature_content.split(',')[1]
                online_order_form_res.write(
                    {'client_business_principle_signature': client_business_principle_signature_encoded.encode(
                        'utf-8')})
            if kwargs.get('kp_online_order_signature', False):
                signature = kwargs.get('kp_online_order_signature', False)
                signature_content = signature.split(';')[1]
                signature_encoded = signature_content.split(',')[1]
                online_order_form_res.write({'signature': signature_encoded.encode('utf-8')})
            attachment_ids = []
            if kwargs.get('menu', False):
                menu_file = kwargs.get('menu')
                menu_file_ir_values = {
                    'name': "online_order_menu_file",
                    'type': 'binary',
                    'datas': base64.b64encode(menu_file.read()),
                    'is_web_attachment': True
                }
                menu_file_data_id = request.env['ir.attachment'].sudo().create(menu_file_ir_values)
                online_order_form_res.write({'menu': menu_file_data_id.datas})
                attachment_ids.append(menu_file_data_id.id)
            if kwargs.get('owner_id', False):
                owner_id_file = kwargs.get('owner_id')
                owner_id_ir_values = {
                    'name': "online_order_owner_id_file",
                    'type': 'binary',
                    'datas': base64.b64encode(owner_id_file.read()),
                    'is_web_attachment': True
                }
                owner_id_file_data_id = request.env['ir.attachment'].sudo().create(owner_id_ir_values)
                online_order_form_res.write({'owner_id': owner_id_file_data_id.datas})
                attachment_ids.append(owner_id_file_data_id.id)
            if kwargs.get('irs_document', False):
                irs_document_file = kwargs.get('irs_document')
                irs_document_ir_values = {
                    'name': "online_order_irs_document_file",
                    'type': 'binary',
                    'datas': base64.b64encode(irs_document_file.read()),
                    'is_web_attachment': True
                }
                irs_document_file_data_id = request.env['ir.attachment'].sudo().create(irs_document_ir_values)
                online_order_form_res.write({'irs_document': irs_document_file_data_id.datas})
                attachment_ids.append(irs_document_file_data_id.id)
            if kwargs.get('void_check', False):
                void_check_file = kwargs.get('void_check')
                irs_document_ir_values = {
                    'name': "online_order_void_check_file",
                    'type': 'binary',
                    'datas': base64.b64encode(void_check_file.read()),
                    'is_web_attachment': True
                }
                void_check_file_data_id = request.env['ir.attachment'].sudo().create(irs_document_ir_values)
                online_order_form_res.write({'void_check': void_check_file_data_id.datas})
                partner.write({'ach_void_check': void_check_file_data_id.datas})
                attachment_ids.append(void_check_file_data_id.id)
        except Exception as e:
            _logger.info("create online order form goes wrong %s", e)
            headers = {'Content-Type': 'application/json'}
            body = {'results': {'code': 501, 'message': "Something is wrong, please try it later"}}
            return Response(json.dumps(body), headers=headers)
        headers = {'Content-Type': 'application/json'}
        body = {'results': {'code': 201, 'message': "Kwickpos online order is created successfully"}}

        return Response(json.dumps(body), headers=headers)

    @http.route(['/online/ordering'], type='json', auth='public', website=True)
    def online_customer_order(self, **kwargs):
        order_obj = False
        if kwargs.get('sale_order_id'):
            order_obj = request.env['online.order'].search([('active','=',False),('sale_order_id', '=', kwargs.get('sale_order_id'))])
            if order_obj:
                order_obj.write(kwargs)
                vals = {'order_id': order_obj.id}
            else:
                order_obj = request.env['online.order'].create(kwargs)
                if order_obj:
                    vals = {'order_id': order_obj.id}
        return vals

    @http.route(['/website/ach_form'],  auth='public', type='http')
    def website_ach_form(self, **kwargs):
        try:
            data_url = kwargs.get("canvas")

            sale_order_id = kwargs.get("sale_order_id")
            partner_id = kwargs.get("partner_id")
            subscription_start_date = kwargs.get('SubscriptionStartDate')
            bank_branch = kwargs.get('BankBranch')
            partner = request.env['res.partner'].sudo().search([('id', '=', partner_id)])
            if kwargs.get('ach_form_void_check', False):
                void_check_file = kwargs.get('ach_form_void_check')
                irs_document_ir_values = {
                    'name': "ach_form_void_check_file",
                    'type': 'binary',
                    'datas': base64.b64encode(void_check_file.read()),
                    'is_web_attachment': True
                }
                void_check_file_data_id = request.env['ir.attachment'].sudo().create(irs_document_ir_values)
                partner.write({'ach_void_check': void_check_file_data_id.datas})

            dba = partner.name
            owner_phone = partner.mobile
            store_phone = partner.phone
            store_address = partner.street
            store_city = partner.city
            country = partner.country_id.name
            state = partner.state_id.name
            owner_name = partner.x_studio_owner_name
            owner_email = partner.email
            store_zip = partner.zip
            bank_name = kwargs.get("BankName")
            routing = kwargs.get("Routing")
            account = kwargs.get("Account")
            bank_id = request.env['res.bank'].sudo().search([('name', '=', bank_name)])
            if not bank_id:
                bank_id = request.env['res.bank'].sudo().create({'name': bank_name})
            partner_account = request.env['res.partner.bank'].sudo().search(
                [
                    ('acc_number', '=', account), ('aba_routing', '=', routing)
                ])
            if partner_account:
                headers = {'Content-Type': 'application/json'}
                body = {'code': 202, 'message': "You already uploaded before!"}
                partner.write({'bank_ids': [(4, partner_account[0].id)]})
                return Response(json.dumps(body), headers=headers)
            else:
                partner_account = request.env['res.partner.bank'].sudo().create(
                    {'partner_id': partner_id,
                     'acc_number': account,
                     'bank_id': bank_id[0].id,
                     'aba_routing': routing,
                     })
            bank_account_dict = {
                '1': 'PersonalChecking',
                '2': 'PersonalSavings',
                '3': 'BusinessChecking',
                '4': 'BusinessSavings',
                '5': 'Other',
            }
            bank_account_type = bank_account_dict.get(kwargs.get('bank_account_type'))
            # sales_order = request.env['sale.order'].search([('id', '=', sale_order_id)])
            content = data_url.split(';')[1]
            image_encoded = content.split(',')[1]
            res = request.env['ach.form'].sudo().create({
                'sale_order_id': sale_order_id,
                'dba': dba,
                'store_phone': store_phone,
                'store_address': store_address,
                'store_city': store_city,
                'store_zip': store_zip,
                'country': country,
                'state': state,
                'owner_name': owner_name,
                'owner_phone': owner_phone,
                'owner_email': owner_email,
                'subscription_start_date': subscription_start_date,
                'bank_name': bank_name,
                'bank_routing': routing,
                'bank_account': account,
                'bank_branch': bank_branch,
                'bank_account_type': bank_account_type,
                'signature': image_encoded.encode('utf-8')
            })
            pdf = request.env.ref('website_application.action_report_ach').sudo()._render_qweb_pdf(res.ids)[0]
            b64_pdf = base64.b64encode(pdf)
            partner.sudo().write({"ach_form_pdf": b64_pdf})
            headers = {'Content-Type': 'application/json'}
            body = {'code': 201, 'message': "ACH form is created successfully"}
            return Response(json.dumps(body), headers=headers)

        except Exception as e:
            _logger.info("create ach form goes wrong %s", e)
            headers = {'Content-Type': 'application/json'}
            body = {'code': 501, 'message': "ACH form creation failed"}
            return Response(json.dumps(body), headers=headers)

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        Partner = request.env['res.partner'].with_context(show_address=1).sudo()
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        mode = (False, False)
        can_edit_vat = False
        values, errors = {}, {}

        partner_id = int(kw.get('partner_id', -1))

        # IF PUBLIC ORDER
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            mode = ('new', 'billing')
            can_edit_vat = True
        # IF ORDER LINKED TO A PARTNER
        else:
            if partner_id > 0:
                if partner_id == order.partner_id.id:
                    mode = ('edit', 'billing')
                    can_edit_vat = order.partner_id.can_edit_vat()
                else:
                    shippings = Partner.search([('id', 'child_of', order.partner_id.commercial_partner_id.ids)])
                    if order.partner_id.commercial_partner_id.id == partner_id:
                        mode = ('new', 'shipping')
                        partner_id = -1
                    elif partner_id in shippings.mapped('id'):
                        mode = ('edit', 'shipping')
                    else:
                        return Forbidden()
                if mode and partner_id != -1:
                    values = Partner.browse(partner_id)
            elif partner_id == -1:
                mode = ('new', 'shipping')
            else: # no mode - refresh without post?
                return request.redirect('/shop/checkout')
        if mode == ('new', 'billing') or mode == ('edit', 'billing'):
            if kw.get('find_ref'):
                order.find_ref = kw.get('find_ref')
            else:
                order.find_ref = False
            if kw and order and kw.get('x_studio_agent'):
                    order.x_studio_many2one_field_8mpil = int(kw.get('x_studio_agent'))
            else:
                order.x_studio_many2one_field_8mpil = False
            if kw and order and kw.get('find_ref') and kw.get('find_ref') == 'referral' and kw.get('ref'):
                order.referal_code = kw.get('ref')
            else:
                order.referal_code = False
            if kw and order and kw.get('find_ref') and kw.get('find_ref') == 'online_ad' and kw.get('online_add'):
                order.find_ref = kw.get('find_ref')
                order.online_add = kw.get('online_add')
                if kw.get('online_add') == 'other' and kw.get('other_add'):
                    order.other_add = kw.get('other_add')
            else:
                order.online_add = False
                order.other_add = False

            if kw and kw.get('order_type'):
                order.sale_order_type = kw.get('order_type')
        # IF POSTED
        if 'submitted' in kw:
            pre_values = self.values_preprocess(order, mode, kw)
            errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
            post, errors, error_msg = self.values_postprocess(order, mode, pre_values, errors, error_msg)

            if errors:
                errors['error_message'] = error_msg
                values = kw
            else:
                partner_id = self._checkout_form_save(mode, post, kw)
                if mode[1] == 'billing':
                    order.partner_id = partner_id
                    order.with_context(not_self_saleperson=True).onchange_partner_id()
                    # This is the *only* thing that the front end user will see/edit anyway when choosing billing address
                    order.partner_invoice_id = partner_id
                    if not kw.get('use_same'):
                        kw['callback'] = kw.get('callback') or \
                            (not order.only_services and (mode[0] == 'edit' and '/shop/checkout' or '/shop/address'))
                elif mode[1] == 'shipping':
                    order.partner_shipping_id = partner_id

                # TDE FIXME: don't ever do this
                order.message_partner_ids = [(4, partner_id), (3, request.website.partner_id.id)]
                if not errors:
                    return request.redirect(kw.get('callback') or '/shop/confirm_order')

        render_values = {
            'website_sale_order': order,
            'partner_id': partner_id,
            'mode': mode,
            'checkout': values,
            'can_edit_vat': can_edit_vat,
            'error': errors,
            'callback': kw.get('callback'),
            'only_services': order and order.only_services,
        }
        render_values.update(self._get_country_related_render_values(kw, render_values))
        return request.render("website_sale.address", render_values)

    def check_phone_number_validation(self, phone):
        if len(phone) == 10:
            return True
        else:
            return False

    def checkout_form_validate(self, mode, all_form_values, data):
        # mode: tuple ('new|edit', 'billing|shipping')
        # all_form_values: all values before preprocess
        # data: values after preprocess
        error = dict()
        error_message = []

        # Required fields from form
        required_fields = [f for f in (all_form_values.get('field_required') or '').split(',') if f]

        # Required fields from mandatory field function
        country_id = int(data.get('country_id', False))
        required_fields += mode[1] == 'shipping' and self._get_mandatory_fields_shipping(country_id) or self._get_mandatory_fields_billing(country_id)

        # error message for empty required fields
        for field_name in required_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # phone, mobile validation
        if data.get('phone'):
            res = self.check_phone_number_validation(data.get('phone'))
            if not res:
                error["phone"] = 'error'
                error_message.append(_('Business Phone number not valid. please enter phone number in correct format.'))

        if data.get('mobile'):
            res = self.check_phone_number_validation(data.get('mobile'))
            if not res:
                error["mobile"] = 'error'
                error_message.append(_('Cell Phone number not valid. please enter phone number in correct format.'))

        if data.get('zip') and len(data.get('zip')) != 5:
            error["zip"] = 'error'
            error_message.append(_('Zip code length should be 5.'))

        if 'order_type' in data and not data.get('order_type'):
            error["order_type"] = 'error'
            error_message.append(_('Please select order type.'))

        # vat validation
        Partner = request.env['res.partner']
        if data.get("vat") and hasattr(Partner, "check_vat"):
            if country_id:
                data["vat"] = Partner.fix_eu_vat_number(country_id, data.get("vat"))
            partner_dummy = Partner.new(self._get_vat_validation_fields(data))
            try:
                partner_dummy.check_vat()
            except ValidationError as exception:
                error["vat"] = 'error'
                error_message.append(exception.args[0])

        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('item mark " * " is required field'))

        return error, error_message
