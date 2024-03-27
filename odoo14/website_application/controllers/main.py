# -*- coding: utf-8 -*-

import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import Forbidden, NotFound
_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _, SUPERUSER_ID, tools
from odoo.http import request
from odoo import http
import base64
import json
import requests
from odoo.modules.module import get_module_resource
from odoo.http import request, Response, JsonRequest

class WebsiteSale(WebsiteSale):

    @http.route(['/form'], type='http', auth="public", methods=['GET'] , website=True)
    def form(self, **kw):
        render_values = {
        }
        return request.render("website_application.tmp_application", render_values)

    @http.route(['/application'], type='http', auth="public", methods=['GET'], website=True)
    def application(self, **kw):
        attachment_name = 'KwickServiceAgreement.pdf'
        country = request.env['res.country']
        try:
            attachment_id = request.env['ir.attachment'].sudo().search([('name', '=', attachment_name)]).read()[0]['id']
        except:
            render_values = {
                'success': False,
            }
            return request.render("website_application.email_sent", render_values)
        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
            'attachment_id': attachment_id
        }
        return request.render("website_application.tmp_customer_form", render_values)

    @http.route(['/application_rebate'], type='http', auth="public", methods=['GET'], website=True)
    def application_rebate(self, **kw):
        country = request.env['res.country']

        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
        }
        return request.render("website_application.zbs_rebate_form", render_values)

    @http.route(['/application_ach'], type='http', auth="public", methods=['GET'], website=True)
    def application_ach(self, **kw):
        country = request.env['res.country']

        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
        }
        return request.render("website_application.Zbs_SaaS_ACH_Authorization_Form", render_values)

    @http.route(['/application_new_merchant'], type='http', auth="public", methods=['GET'], website=True)
    def application_new_merchant(self, **kw):
        country = request.env['res.country']

        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
        }
        return request.render("website_application.new_merchant_form", render_values)

    @http.route(['/application_questionnaire_reminder'], type='http', auth="public", methods=['GET'], website=True)
    def application_questionnaire_reminder(self, **kw):
        country = request.env['res.country']

        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
        }
        return request.render("website_application.questionnaire_reminder", render_values)

    @http.route(['/application_questionnaire'], type='http', auth="public", methods=['GET'], website=True)
    def application_questionnaire(self, **kw):
        country = request.env['res.country']

        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
        }
        return request.render("website_application.questionnaire", render_values)

    @http.route(['/application_rma_warranty'], type='http', auth="public", methods=['GET'], website=True)
    def application_rma_warranty(self, **kw):
        country = request.env['res.country']

        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
        }
        return request.render("website_application.application_rma_warranty", render_values)

    @http.route(['/application_kwickpos_online_ordering'], type='http', auth="public",
                methods=['GET'], website=True)
    def application_online_ordering(self, **kw):
        country = request.env['res.country']

        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
        }
        return request.render("website_application.application_kwickpos_online_ordering", render_values)

    @http.route(['/application_kwickpos_online_ordering/<int:online_order_id>'], type='http', auth="public", methods=['GET'], website=True, csrf=False)
    def application_online_ordering_online_order_id(self, online_order_id, **kw):
        country = request.env['res.country']

        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
        }
        if online_order_id:
            online_order_from = request.env['online.order.form'].sudo().search([('id', '=', online_order_id)])
        render_values.update({
            'online_order_from':online_order_from})
        return request.render("website_application.application_kwickpos_online_ordering", render_values)

    @http.route(['/application_new_merchant/<int:new_merchant_id>'], type='http', auth="public",
                methods=['GET'], website=True,csrf=False)
    def application_new_merchant_id(self, new_merchant_id, **kw):
        country = request.env['res.country']

        render_values = {
            'country_states': country.get_website_sale_states(),
            'countries': country.get_website_sale_countries(),
        }
        if new_merchant_id:
            new_merchant_from = request.env['merchant.form'].sudo().search([('id', '=', new_merchant_id)])
        render_values.update({
            'new_merchant_from': new_merchant_from})
        return request.render("website_application.new_merchant_form", render_values)

    @http.route(['/application/country_infos/<model("res.country"):country>'], type='json', auth="public", methods=['POST'],
                website=True)
    def application_country_infos(self, country, mode='billing', **kw):
        return dict(
            fields=country.get_address_fields(),
            states=[(st.id, st.name, st.code) for st in country.get_website_sale_states(mode=mode)],
            phone_code=country.phone_code,
            zip_required=country.zip_required,
            state_required=country.state_required,
        )

    @http.route(['/canvas'], type='json', auth="public",
                methods=['POST'],
                website=True)
    def application_canvas(self, mode='billing', **kw):
        print(kw)
        data_url = kw.get("canvas")
        dba = kw.get("dba")
        street = kw.get("street")
        city = kw.get("city")
        state_id = kw.get("state_id")
        store_zip = kw.get("store_zip")
        country_id = kw.get("country_id")
        email = kw.get("email")
        owner_phone = kw.get("owner_phone")

        content = data_url.split(';')[1]
        image_encoded = content.split(',')[1]
        rebate_form_attachment = request.env['ir.attachment'].sudo().create({
            'name': dba + '-' + owner_phone + '-' + 'signature',
            'type': 'binary',
            'datas': image_encoded.encode('utf-8'),
        })

    @http.route(['/application_rma_warranty/submit'], auth="public", type='http', methods=['POST'],
                website=True, csrf=False)
    def rma_submit(self, **kw):
        try:
            dba = kw.get('dba')

            service_type = kw.get('service_type')
            service_type_dict = {
                '1': 'RMA Warranty Request (Approval needed)',
                '2': 'Repair (Non Warranty Repair - Fee Applys)',

            }
            service_type_string = service_type_dict.get(service_type, '1')
            lead_id = kw.get('lead_id')
            contact_name = kw.get('contact_name')
            contact_phone = kw.get('contact_phone')
            restaurant_address = kw.get('restaurant_address')
            restaurant_city = kw.get('restaurant_city')
            restaurant_zipcode = kw.get('restaurant_zipcode')
            country_id = kw.get('country_id')
            state_id = kw.get('state_id')

            model_number = kw.get('model_number')
            email = kw.get('email')
            serial_number = kw.get('serial_number')
            date_of_purchase = kw.get('date_of_purchase')
            detailed_fault_description = kw.get('detailed_fault_description')
            picture_of_faulty_device = kw.get('picture_of_faulty_device')


            rma_form = request.env['rma.form'].sudo().create({'service_type': service_type,
                                                          'dba': dba,
                                                          'email':email,
                                                          'lead_id': lead_id,
                                                          'contact_name': contact_name,
                                                          'contact_phone': contact_phone,
                                                          'restaurant_address': restaurant_address,
                                                          'restaurant_city': restaurant_city,
                                                          'restaurant_zipcode': restaurant_zipcode,
                                                          'country_id': country_id,
                                                          'state_id': state_id,
                                                          'model_number': model_number,
                                                          'serial_number': serial_number,
                                                          'date_of_purchase': date_of_purchase,
                                                          'detailed_fault_description': detailed_fault_description,
                                                              'status': 'new'
                                                          })
            # stock_move_line = request.env['stock.move.line'].sudo().search(['&', ('state', '=', 'done'), '|', ('lot_name', '=', serial_number), ('delivery_lot_name', '=', serial_number)],
            #                                                            order="date desc", limit=1)
            pickings = request.env['stock.picking'].sudo().search([('state', '=', 'done')] , order="date_done desc")
            flag = False
            for picking in pickings:
                if 'OUT' in picking.name:
                    for item in picking.move_ids_without_package:
                        for lot_id in item.lot_ids:
                            if lot_id.name == serial_number:
                                rma_form.write({'sale_order': picking.sale_id.id})
                                flag = True
                                break
                        if flag:
                            break
                    if flag:
                        break

            user = request.env.user
            ctx = request.env.context.copy()
            ctx.update({
                'service_type': service_type_string,
                'dba': dba,
                'email_from': request.env.user.company_id.catchall_email,
                'lead_id': lead_id,
                'contact_name': contact_name,
                'contact_phone': contact_phone,
                'restaurant_address': restaurant_address,
                'restaurant_city': restaurant_city,
                'restaurant_country': country_id,
                'state': state_id,
                'restaurant_zipcode': restaurant_zipcode,
                'model_number': model_number,
                'serial_number': serial_number,
                'date_of_purchase': date_of_purchase,
                'detailed_fault_description': detailed_fault_description,
                'picture_of_faulty_device': picture_of_faulty_device,

            })

            mail_template_id = request.env.ref('website_application.email_template_application_rma_warranty').sudo()
            if kw.get('signature', False):
                rma_signature = kw.get('signature', False)
                rma_content = rma_signature.split(';')[1]
                rma_image_encoded = rma_content.split(',')[1]
                rma_form.write({'signature': rma_image_encoded.encode('utf-8')})

            if kw.get('picture_of_faulty_device'):
                file = kw.get('picture_of_faulty_device')
                ir_values = {
                    'name': "rma_picture",
                    'type': 'binary',
                    'datas': base64.b64encode(file.read()),
                    'res_model': 'res.users',
                    'res_id': user.id,
                    'is_web_attachment': True
                }
                data_id = request.env['ir.attachment'].sudo().create(ir_values)
                rma_form.write({'picture_of_faulty_device': data_id.datas})

                mail_template_id.attachment_ids = [(6, 0, [data_id.id])]

            ctx.update({
                'email_to': 'accounting@zbspos.com',
                'id': rma_form.id
            })
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)

            render_values = {
                'success': True,
            }
            return request.render("website_application.email_sent", render_values)

        except Exception as e:
            # raise ValidationError(e)
            _logger.info("Send RMA email error:  %s ", e)
            render_values = {
                'success': False,

            }
            return request.render("website_application.email_sent", render_values)

    @http.route(['/application/submit'], auth="public", type='http', methods=['POST'],
                website=True)
    def application_submit(self, **kw):
        agent_email = kw.get('AgentEmail')
        agent_name = kw.get('AgentName')
        store_name = kw.get('StoreName')
        store_phone = kw.get('StorePhone')
        store_address = kw.get('StoreAddress')
        store_city = kw.get('StoreCity')
        store_zip = kw.get('StoreZip')
        country = kw.get('country')
        state = kw.get('state')
        owner_name = kw.get('OwnerName')
        owner_phone = kw.get('OwnerPhone')
        owner_email = kw.get('OwnerEmail')
        doordash_username = kw.get('DoordashUsername')
        doordash_password = kw.get('DoordashPassword')
        ubereats_username = kw.get('UberEatsUsername')
        ubereats_password = kw.get('UberEatsPassword')
        ubereats_pin = kw.get('UberEatsPin')
        ubereatstablet_username = kw.get('UberEatsTabletUsername')
        ubereatstablet_password = kw.get('UberEatsTabletPassword')
        grubhub_username = kw.get('GrubhubUsername')
        grubhub_password = kw.get('GrubhubPassword')

        bank_name = kw.get('BankName')
        routing = kw.get('Routing')
        account = kw.get('Account')
        user = request.env.user
        ctx = request.env.context.copy()
        ctx.update({
            'email_to': agent_email,
            'agent_name': agent_name,
            'email_from': request.env.user.company_id.catchall_email,
            'store_name': store_name,
            'store_phone': store_phone,
            'store_address': store_address,
            'store_city': store_city,
            'store_zip': store_zip,
            'store_country': country,
            'store_state': state,
            'owner_name': owner_name,
            'owner_phone': owner_phone,
            'owner_email': owner_email,
            'doordash_username': doordash_username,
            'doordash_password': doordash_password,
            'ubereats_username': ubereats_username,
            'ubereats_password': ubereats_password,
            'ubereats_pin':ubereats_pin,
            'ubereatstablet_username': ubereatstablet_username,
            'ubereatstablet_password': ubereatstablet_password,
            'grubhub_username': grubhub_username,
            'grubhub_password': grubhub_password,
            'bank_name': bank_name,
            'routing': routing,
            'account': account,

        })

        mail_template_id = request.env.ref('website_application.email_sign_payment_contract').sudo()
        try:
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)
            ctx.update({
                'email_to': 'lingy@zbspos.com',
            })
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)
            ctx.update({
                'email_to': 'vickin@zbspos.com',
            })
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)
            ctx.update({
                'email_to': 'account@zbspos.com',
            })
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)
            render_values = {
                'success': True,
            }
            return request.render("website_application.email_sent", render_values)
        except ValueError:
            render_values = {
                'success': False,

            }
            return request.render("website_application.email_sent", render_values)

    @http.route(['/application_rebate/submit'], auth="public", type='http', methods=['POST'],
                website=True)
    def application_rebate_submit(self, **kw):
        sales_email = kw.get('SalesEmail')
        sales_name = kw.get('SalesName')
        store_name = kw.get('StoreName')
        store_phone = kw.get('StorePhone')
        store_address = kw.get('StoreAddress')
        store_city = kw.get('StoreCity')
        store_zip = kw.get('StoreZip')
        country_id = kw.get('country_id')
        state_id = kw.get('state_id')
        owner_name = kw.get('OwnerName')
        owner_phone = kw.get('OwnerPhone')
        owner_email = kw.get('OwnerEmail')
        lead_id = kw.get('LeadId')
        purchase_date = kw.get('PurchaseDate')
        bank_name = kw.get('BankName')
        routing = kw.get('Routing')
        account = kw.get('Account')
        country = request.env["res.country"].search([('id', '=', country_id)]).name
        state = request.env["res.country.state"].search([('id', '=', state_id)]).name
        user = request.env.user
        ctx = request.env.context.copy()
        ctx.update({
            'email_to': sales_email,
            'sales_name': sales_name,
            'sales_email': sales_email,
            'email_from': request.env.user.company_id.catchall_email,
            'store_name': store_name,
            'store_phone': store_phone,
            'store_address': store_address,
            'store_city': store_city,
            'store_zip': store_zip,
            'store_country': country,
            'store_state': state,
            'owner_name': owner_name,
            'owner_phone': owner_phone,
            'owner_email': owner_email,
            'purchase_date': purchase_date,
            'bank_name': bank_name,
            'routing': routing,
            'account': account,

        })

        res = request.env['rebate.bank'].sudo().create({'sales_name': sales_name,
                                                 'sales_email': sales_email,
                                            'store_name': store_name,
                                            'store_phone': store_phone,
                                            'store_address': store_address,
                                            'store_city': store_city,
                                             'store_zip':store_zip,
                                            'country': country,
                                            'state': state,
                                            'owner_name': owner_name,
                                            'owner_phone': owner_phone,
                                            'owner_email': owner_email,
                                            'purchase_date': purchase_date,
                                            'bank_name': bank_name,
                                            'bank_routing': routing,
                                            'bank_account': account
                                                                     })
        pdf = request.env.ref('website_application.action_report_rebate')._render_qweb_pdf(res.ids)[0]
        b64_pdf = base64.b64encode(pdf)
        name = 'rebate_bank'+str(res.id)
        rebate_form_attachment = request.env['ir.attachment'].sudo().create({
            'type': 'binary',
            'datas': b64_pdf,
            'name': name + '.pdf',
            'mimetype': 'application/x-pdf'
        })
        #create iris ticket
        iris_url_user = "https://zbs.iriscrm.com/api/v1/leads/users"
        iris_url_lead = "https://zbs.iriscrm.com/api/v1/leads"
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
        headers.update({'X-API-KEY': IRIS_API_KEY})
        response = requests.get(iris_url_user, headers=headers)
        crm_users_data = json.loads(response.text)
        crm_sales_id = 0
        for crm_user in crm_users_data.get('data'):
            if crm_user.get('email') == sales_email:
                crm_sales_id = int(crm_user.get('id'))

        iris_ticket_data = {
            "type": 379,
            "subject": store_name,
            "priority": 0,
            "assignedUsers": [205, crm_sales_id],
            "assignType": "none",
            "group_id": 0,
            "assignType": "lead",
            "assignTo": lead_id,
        }
        # response_lead = requests.get(iris_url_lead, params={'email': owner_email}, headers=headers)
        # response_lead_json = json.loads(response_lead.text)
        # if len(response_lead_json.get('data')) > 0:
        #     lead_id = 0
        #     for lead in response_lead_json.get('data'):
        #         if lead.get('name').lower() == store_name.lower():
        #             lead_id = lead.get('id')
        #     iris_ticket_data.update({
        #         "assignType": "lead",
        #         "assignTo": lead_id,
        #     })
        iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
        response = requests.post(iris_ticket_url, data=json.dumps(iris_ticket_data), headers=headers)

        mail_template_id = request.env.ref('website_application.email_sign_rebate_form_to_sales').sudo()
        if kw.get('attachment'):
            file = kw.get('attachment')
            ir_values = {
                'name': "Rebate",
                'type': 'binary',
                'datas': base64.b64encode(file.read()),
                'res_model': 'res.users',
                'res_id': user.id,
                'is_web_attachment': True
            }
            data_id = request.env['ir.attachment'].create(ir_values)
        try:
            mail_template_id.attachment_ids = [(6, 0, [data_id.id, rebate_form_attachment.id])]
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)

            render_values = {
                'success': True,
            }
            return request.render("website_application.email_sent", render_values)

        except ValueError:
            render_values = {
                'success': False,

            }
            return request.render("website_application.email_sent", render_values)

    @http.route(['/application_ach_authorization/submit'], auth="public", type='http', methods=['POST'], website=True)
    def application_ach_submit(self, **kw):
        dba = kw.get('DBA')
        store_phone = kw.get('StorePhone')
        store_address = kw.get('StoreAddress')
        store_city = kw.get('StoreCity')
        store_zip = kw.get('StoreZip')
        country_id = kw.get('country_id')
        state_id = kw.get('state_id')
        owner_name = kw.get('OwnerName')
        owner_phone = kw.get('OwnerPhone')
        owner_email = kw.get('OwnerEmail')
        pad_number = kw.get('PadNumber')
        subscription_start_date = kw.get('SubscriptionStartDate')
        monthly_subscription = []
        main_subscription = kw.get('MainSubscription')
        saas_subscription = kw.get('SaasSubscription')
        tablet_subscription = kw.get('TabletSubscription')
        kitchen_display_system_subscription = kw.get('KitchenDisplaySystemSubscription')
        kiosk_saas_subscription = kw.get('KioskSaaSSubscription')
        monthly_gateway = kw.get('MonthlyGateway')
        monthly_support = kw.get('MonthlySupport')
        if main_subscription is not None:
            monthly_subscription.append("Main Subscription $ 29.00")
        if saas_subscription is not None:
            monthly_subscription.append("Saas Subscription - 2nd+ $ 15.00")
        if tablet_subscription is not None:
            monthly_subscription.append("iPad/Tablet Subscription $ 15.00")
        if kitchen_display_system_subscription is not None:
            monthly_subscription.append("Kitchen Display System Subscription $ 15.00")
        if kiosk_saas_subscription is not None:
            monthly_subscription.append("Kiosk SaaS Subscription $ 60.00")
        if monthly_gateway is not None:
            monthly_subscription.append("Monthly Gateway Fee $ 60.00")
        if monthly_support is not None:
            monthly_subscription.append("Monthly Support Fee $ 60.00")

        billing_name = kw.get('BillingName')

        bank_name = kw.get('BankName')
        routing = kw.get('Routing')
        account = kw.get('Account')
        bank_branch = kw.get('BankBranch')
        bank_phone_number = kw.get('BankPhoneNumber')

        bank_account_type = []
        personal_checking = kw.get('PersonalChecking')
        personal_savings = kw.get('PersonalSavings')
        business_checking = kw.get('BusinessChecking')
        business_savings = kw.get('BusinessSavings')
        other = kw.get('other')
        if personal_checking is not None:
            bank_account_type.append("PersonalChecking")
        if personal_savings is not None:
            bank_account_type.append("PersonalSavings")
        if business_checking is not None:
            bank_account_type.append("BusinessChecking")
        if business_savings is not None:
            bank_account_type.append("BusinessSavings")
        if other is not None:
            bank_account_type.append("other")
        date = kw.get('Date')
        data_url = kw.get('hidden_canvas')

        user = request.env.user
        ctx = request.env.context.copy()
        country = request.env["res.country"].search([('id', '=', country_id)]).name
        state = request.env["res.country.state"].search([('id', '=', state_id)]).name
        ctx.update({
            'DBA': dba,
            'email_from': request.env.user.company_id.catchall_email,
            'store_phone': store_phone,
            'store_address': store_address,
            'store_city': store_city,
            'store_zip': store_zip,
            'store_country': country,
            'store_state': state,
            'owner_name': owner_name,
            'owner_phone': owner_phone,
            'owner_email': owner_email,
            'pad_number': pad_number,
            'monthly_subscription': ",".join(monthly_subscription),
            'subscription_start_date': subscription_start_date,
            'billing_name': billing_name,
            'bank_name': bank_name,
            'bank_routing': routing,
            'bank_account': account,
            'bank_branch': bank_branch,
            'bank_phone_number': bank_phone_number,
            'bank_account_type': ",".join(bank_account_type),
            'date': date,
        })

        partner_id = request.env['res.partner'].sudo().search(
            [('phone', '=', owner_phone),
             ('email', '=', owner_email)])
        if not partner_id:
            partner_id = request.env['res.partner'].sudo().create({
                    'name': dba,
                    'street': store_address,
                    'city': store_city,
                    'state_id': int(state_id),
                    'zip': store_zip,
                    'country_id': int(country_id),
                    'phone': owner_phone,
                    'email': owner_email,
                })
        bank_id = request.env['res.bank'].sudo().search([('name', '=', bank_name)])
        if not bank_id:
            bank_id = request.env['res.bank'].sudo().create({'name': bank_name})
        partner_account = request.env['res.partner.bank'].sudo().search(
            [
             ('acc_number', '=', account),
             ])
        if not partner_account:
            partner_account = request.env['res.partner.bank'].sudo().create(
                {'partner_id': partner_id.id,
                 'acc_number': account,
                 'bank_id': bank_id[0].id,
                 'aba_routing': routing,
                 })
        attachment_id = request.env['ir.attachment'].sudo().search([('name', '=', dba + '-' + owner_phone + '-' + 'signature')]).read()
        res = request.env['ach.form'].sudo().create({
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
                                                 'pad_number': pad_number,
                                                 'monthly_subscription': ",".join(monthly_subscription),
                                                 'subscription_start_date': subscription_start_date,
                                                 'billing_name': billing_name,
            'bank_name': bank_name,
            'bank_routing': routing,
            'bank_account': account,
            'bank_branch': bank_branch,
            'bank_phone_number': bank_phone_number,
            'bank_account_type': ",".join(bank_account_type),
            'date': date,
            'signature': attachment_id[0].get('datas')
                                                 })
        pdf = request.env.ref('website_application.action_report_ach')._render_qweb_pdf(res.ids)[0]
        b64_pdf = base64.b64encode(pdf)
        ach_form_pdf = request.env['ir.attachment'].sudo().create({
            'name': dba + '-' + owner_phone + '-' + 'ach_form_pdf',
            'type': 'binary',
            'datas': b64_pdf,
            'name': dba + '-' + owner_phone + '-' + 'ach_form_pdf' + '.pdf',
            'mimetype': 'application/x-pdf'
        })
        partner_id.write({"ach_form_pdf": b64_pdf})

        mail_template_id = request.env.ref('website_application.email_sign_ach_form').sudo()
        if kw.get('attachment'):
            file = kw.get('attachment')
            ir_values = {
                'name': "ach_form_attachment",
                'type': 'binary',
                'datas': base64.b64encode(file.read()),
                'res_model': 'res.users',
                'res_id': user.id,
                'is_web_attachment': True
            }
            data_id = request.env['ir.attachment'].create(ir_values)
        try:
            mail_template_id.attachment_ids = [(6, 0, [data_id.id])]
            ctx.update({
                'email_to': 'accounting@zbspos.com',
            })
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)
            ctx.update({
                'email_to': 'form@zbspos.com',
            })
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)

            render_values = {
                'success': True,
            }
            return request.render("website_application.email_sent", render_values)
        except ValueError:
            render_values = {
                'success': False,
                'message': "E"
            }
            return request.render("website_application.email_sent", render_values)

    @http.route(['/online_order_file_update'], type='json', auth="public", methods=['POST'],
                website=True, csrf=False)
    def online_order_file_update(self, **kw):
        print(kw)
        data_url = kw.get("canvas")
        dba = kw.get("dba")
        street = kw.get("street")
        city = kw.get("city")
        state_id = kw.get("state_id")
        store_zip = kw.get("store_zip")
        country_id = kw.get("country_id")
        email = kw.get("email")
        owner_phone = kw.get("owner_phone")

        content = data_url.split(';')[1]
        image_encoded = content.split(',')[1]
        rebate_form_attachment = request.env['ir.attachment'].sudo().create({
            'name': dba + '-' + owner_phone + '-' + 'signature',
            'type': 'binary',
            'datas': image_encoded.encode('utf-8'),
        })

    @http.route(['/application_kwickpos_online_ordering/submit'], auth="public", type='http', methods=['POST'], website=True, csrf=False)
    def application_online_ordering_submit(self, **kw):

        customer_id = kw.get('customer_id')
        pos_system = kw.get('pos_system', False)
        pos_system = False if pos_system == 'undefined' else pos_system
        pos_system_dict = {
            '1': 'KwickPOS (No Deposit)',
            '2': 'New (No Deposit)',
            '3': 'Other (No Deposit)',
            '4': 'KwickPOS (VS)',
            '5': 'Aldelo ($300 Deposit Required)',
            '6': 'GDC ($300 Deposit Required)',
            '7': 'MCPOS ($300 Deposit Required)',
            '8': 'MenuSifu ($300 Deposit Required)',
            '9': 'Other ($300 Deposit Required)',
        }
        pos_system_string = pos_system_dict.get(pos_system, '1')
        need_website = kw.get('need_website', False)
        need_website = False if need_website == 'undefined' else need_website
        need_website_dict = {
            '1': 'No, link online order page to my website.',
            '2': 'No, I only need online order page as website.',
            '3': 'Yes, I need a website and online order page.',

        }
        need_website_string = need_website_dict.get(need_website, '1')
        website_address = kw.get('website_address')
        owner_name = kw.get('owner_name')
        cell_phone_number = kw.get('cell_phone_number')
        email = kw.get('email')

        wechat = kw.get('wechat')
        dba = kw.get('dba')
        business_phone_number = kw.get('business_phone_number')
        company_address = kw.get('company_address')
        restaurant_city = kw.get('restaurant_city')
        restaurant_state = kw.get('restaurant_state')
        restaurant_zipcode = kw.get('restaurant_zipcode')
        lunch_hours = kw.get('lunch_hours')
        sales_tax = kw.get('sales_tax')
        need_chinese = kw.get('need_chinese', False)
        need_chinese = False if need_chinese == 'undefined' else need_chinese
        need_chinese_dict = {
            '1': 'Yes',
            '2': 'No',
            '3': '',
        }
        language = kw.get('language',False)
        if language:
            need_chinese_dict.update({'3':language})
        need_chinese_string = need_chinese_dict.get(need_chinese, '1')
        service_type = kw.get('service_type', False)
        service_type = False if service_type == 'undefined' else service_type
        service_type_dict = {
            '1': 'Pickup Only',
            '2': 'Delivery Only',
            '3': 'Pickup and Delivery',
        }
        service_type_string = service_type_dict.get(service_type, '1')
        plan_choice = kw.get('plan_choice', False)
        plan_choice = False if plan_choice == 'undefined' else plan_choice
        plan_choice_dict = {
            '1': 'Promo Special / $1.00 Per Order (Customer Pays)',
            '2': 'Free Plan / $1.50 Per Order (Customer Pays)',
            '3': '$159/Month (Unlimited Orders)',
            '4': '5% Per Order',
        }
        plan_choice_string = plan_choice_dict.get(plan_choice, '1')
        backup_phone = kw.get('backup_phone')

        delivery_zone = kw.get('delivery_zone')
        delivery_fee = kw.get('delivery_fee')
        minimum_order_amount = kw.get('minimum_order_amount')
        free_delivering_minimum_amount = kw.get('free_delivering_minimum_amount')

        payment_option = kw.get('payment_option', False)
        payment_option = False if payment_option == 'undefined' else payment_option
        payment_option_dict = {
            '1': 'In Store + Online Payment',
            '2': 'Online Payment Only',
            '3': 'In-store Payment Only',
        }
        payment_option_string = payment_option_dict.get(payment_option, '1')
        if_cash_discount = kw.get('if_cash_discount', False)
        if_cash_discount = False if if_cash_discount == 'undefined' else if_cash_discount
        if_cash_discount_dict = {
            '1': 'Yes, customers will pay a surcharge fee for online credit card transactions',
            '2': 'No, customers will pay NO additional surcharge for online credit card transactions',
        }
        if_cash_discount_string = if_cash_discount_dict.get(if_cash_discount, '1')

        company_name = kw.get('company_name')
        ssn = kw.get('ssn')
        tax_id = kw.get('tax_id')
        is_confirm = kw.get('is_confirm')

        account_number = kw.get('account_number')
        routing_number = kw.get('routing_number')
        note = kw.get('note')
        agent_name = kw.get('agent_name')
        agent_email = kw.get('agent_email')

        from_application_signature_date = kw.get('from_application_signature_date', False)
        personal_guarantee_signature_date = kw.get('personal_guarantee_signature_date', False)
        print_client_business_legal_name = kw.get('print_client_business_legal_name', False)
        print_name_of_signer = kw.get('print_name_of_signer', False)
        client_business_principle_title = kw.get('client_business_principle_title', False)
        client_business_principle_sign_date = kw.get('client_business_principle_sign_date', False)
        date = kw.get('date', False)
        try:
            if kw.get('id', False):
                online_order_form_id = kw.get('id', False)
                online_order_form_res = request.env['online.order.form'].sudo().search([["id", "=", int(online_order_form_id)]])
                online_order_form_res.sudo().update({
                    'customer_id': customer_id,
                    'pos_system': pos_system,
                    'need_website': need_website,
                    'website_address': website_address,
                    'wechat': wechat,
                    'lunch_hours': lunch_hours,
                    'sales_tax': sales_tax,
                    'need_chinese': need_chinese,
                    'language': language,
                    'service_type': service_type,
                    'plan_choice': plan_choice,
                    'backup_phone': backup_phone,
                    'delivery_zone': delivery_zone,
                    'delivery_fee': delivery_fee,
                    'minimum_order_amount': minimum_order_amount,
                    'free_delivering_minimum_amount': free_delivering_minimum_amount,
                    'payment_option': payment_option,
                    'if_cash_discount': if_cash_discount,
                    'account_number': account_number,
                    'routing_number': routing_number,
                    'note': note,
                    'agent_email': agent_email,
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
                    'agent_name': agent_name,
                    'personal_guarantee_signature_date': personal_guarantee_signature_date,
                    'from_application_signature_date': from_application_signature_date,
                    'print_client_business_legal_name': print_client_business_legal_name,
                    'print_name_of_signer': print_name_of_signer,
                    'client_business_principle_title': client_business_principle_title,
                    'client_business_principle_sign_date': client_business_principle_sign_date,

                })
            else:
                online_order_form_res = request.env['online.order.form'].sudo().create({
                    'customer_id': customer_id,
                    'pos_system': pos_system,
                    'need_website': need_website,
                    'website_address': website_address,
                    'wechat': wechat,
                    'lunch_hours': lunch_hours,
                    'sales_tax': sales_tax,
                    'need_chinese': need_chinese,
                    'language': language,
                    'service_type': service_type,
                    'plan_choice': plan_choice,
                    'backup_phone': backup_phone,
                    'delivery_zone': delivery_zone,
                    'delivery_fee': delivery_fee,
                    'minimum_order_amount': minimum_order_amount,
                    'free_delivering_minimum_amount': free_delivering_minimum_amount,
                    'payment_option': payment_option,
                    'if_cash_discount': if_cash_discount,
                    'account_number': account_number,
                    'routing_number': routing_number,
                    'note': note,
                    'agent_email': agent_email,
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
                    'agent_name': agent_name,
                    'personal_guarantee_signature_date': personal_guarantee_signature_date,
                    'from_application_signature_date': from_application_signature_date,
                    'print_client_business_legal_name': print_client_business_legal_name,
                    'print_name_of_signer': print_name_of_signer,
                    'client_business_principle_title': client_business_principle_title,
                    'client_business_principle_sign_date': client_business_principle_sign_date,

                })
        except Exception as e:
            _logger.info("create online order form goes wrong %s", e)

        online_order_template_id = request.env.ref('website_application.email_template_application_online_order_form').id
        online_order_template = request.env['mail.template'].sudo().browse(online_order_template_id)

        if kw.get('from_application_signature', False):
            from_application_signature = kw.get('from_application_signature', False)
            from_application_signature_content = from_application_signature.split(';')[1]
            from_application_signature_encoded = from_application_signature_content.split(',')[1]
            online_order_form_res.write({'from_application_signature': from_application_signature_encoded.encode('utf-8')})
        if kw.get('personal_guarantee_signature', False):
            personal_guarantee_signature = kw.get('personal_guarantee_signature', False)
            personal_guarantee_signature_content = personal_guarantee_signature.split(';')[1]
            personal_guarantee_signature_encoded = personal_guarantee_signature_content.split(',')[1]
            online_order_form_res.write({'personal_guarantee_signature': personal_guarantee_signature_encoded.encode('utf-8')})
        if kw.get('pricing_confirmation_signature', False):
            pricing_confirmation_signature = kw.get('personal_guarantee_signature', False)
            pricing_confirmation_signature_content = pricing_confirmation_signature.split(';')[1]
            pricing_confirmation_signature_encoded = pricing_confirmation_signature_content.split(',')[1]
            online_order_form_res.write(
                {'pricing_confirmation_signature': pricing_confirmation_signature_encoded.encode('utf-8')})
        if kw.get('client_initials', False):
            client_initials = kw.get('client_initials', False)
            client_initials_content = client_initials.split(';')[1]
            client_initials_encoded = client_initials_content.split(',')[1]
            online_order_form_res.write({'client_initials': client_initials_encoded.encode('utf-8')})
        if kw.get('client_business_principle_signature', False):
            client_business_principle_signature = kw.get('client_business_principle_signature', False)
            client_business_principle_signature_content = client_business_principle_signature.split(';')[1]
            client_business_principle_signature_encoded = client_business_principle_signature_content.split(',')[1]
            online_order_form_res.write({'client_business_principle_signature': client_business_principle_signature_encoded.encode('utf-8')})
        if kw.get('signature', False):
            signature = kw.get('signature', False)
            signature_content = signature.split(';')[1]
            signature_encoded = signature_content.split(',')[1]
            online_order_form_res.write({'signature': signature_encoded.encode('utf-8')})
        attachment_ids = []
        menu_file_data_id = False
        if kw.get('menu', False):
            menu_file = kw.get('menu')
            menu_file_ir_values = {
                'name': "online_order_menu_file",
                'type': 'binary',
                'datas': base64.b64encode(menu_file.read()),

                'is_web_attachment': True
            }
            menu_file_data_id = request.env['ir.attachment'].sudo().create(menu_file_ir_values)
            online_order_form_res.write({'menu': menu_file_data_id.datas})
            attachment_ids.append(menu_file_data_id.id)
        if kw.get('owner_id', False):
            owner_id_file = kw.get('owner_id')
            owner_id_ir_values = {
                'name': "online_order_owner_id_file",
                'type': 'binary',
                'datas': base64.b64encode(owner_id_file.read()),

                'is_web_attachment': True
            }
            owner_id_file_data_id = request.env['ir.attachment'].sudo().create(owner_id_ir_values)
            online_order_form_res.write({'owner_id': owner_id_file_data_id.datas})
            attachment_ids.append(owner_id_file_data_id.id)
        if kw.get('irs_document', False):
            irs_document_file = kw.get('irs_document')
            irs_document_ir_values = {
                'name': "online_order_irs_document_file",
                'type': 'binary',
                'datas': base64.b64encode(irs_document_file.read()),

                'is_web_attachment': True
            }
            irs_document_file_data_id = request.env['ir.attachment'].sudo().create(irs_document_ir_values)
            online_order_form_res.write({'irs_document': irs_document_file_data_id.datas})
            attachment_ids.append(irs_document_file_data_id.id)
        if kw.get('void_check', False):
            void_check_file = kw.get('void_check')
            irs_document_ir_values = {
                'name': "online_order_void_check_file",
                'type': 'binary',
                'datas': base64.b64encode(void_check_file.read()),

                'is_web_attachment': True
            }
            void_check_file_data_id = request.env['ir.attachment'].sudo().create(irs_document_ir_values)
            online_order_form_res.write({'void_check': void_check_file_data_id.datas})
            attachment_ids.append(void_check_file_data_id.id)
        if kw.get('sharing_link', False):
            online_order_form_res.write({'if_shared_form': True})
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = base_url + '/application_kwickpos_online_ordering/' + str(online_order_form_res.id)
            headers = {'Content-Type': 'application/json'}
            body = {'results': {'code': 200, 'url': url}}

            return Response(json.dumps(body), headers=headers)

        try:
            pdf = request.env.ref('website_application.action_report_online_order').sudo()._render_qweb_pdf(online_order_form_res.ids)[0]
            b64_pdf = base64.b64encode(pdf)
            online_order_pdf = request.env['ir.attachment'].sudo().create({
                'type': 'binary',
                'datas': b64_pdf,
                'name': 'online_order_contract' + '.pdf',
                'mimetype': 'application/x-pdf'
            })
            attachment_ids.append(online_order_pdf.id)
            online_order_template.attachment_ids = [(6, 0, attachment_ids)]
            ctx = request.env.context.copy()
            ctx.update({
                'email_from': request.env.user.company_id.catchall_email,
                'email_to': agent_email,
                'subject': 'New KwickPOS Online Order:  ${object.dba}',
                'reply_to':'form@zbspos.com',
                'if_cash_discount': if_cash_discount_string,
                'payment_option':payment_option_string,
                'plan_choice':plan_choice_string,
                'service_type':service_type_string,
                'need_chinese':need_chinese_string,
                'pos_system':pos_system_string,
                'need_website':need_website_string,
                'from_application_signature': from_application_signature,
                'personal_guarantee_signature': personal_guarantee_signature,
                'pricing_confirmation_signature': pricing_confirmation_signature,
                'client_initials': client_initials,
                'client_business_principle_signature': client_business_principle_signature,
                'signature': signature,
            })
            online_order_template.with_context(ctx).send_mail(online_order_form_res.id, force_send=True)
            ctx.update({
                'email_from': request.env.user.company_id.catchall_email,
                'email_to': email,
                'reply_to': 'form@zbspos.com',
                'subject': 'New KwickPOS Online Order:  '+dba,

            })
            online_order_template.with_context(ctx).send_mail(online_order_form_res.id, force_send=True)
            if pos_system == '4' or pos_system == '1':
                ctx.update({
                    'email_from': request.env.user.company_id.catchall_email,
                    'email_to': 'accounting@zbspos.com',
                    'reply_to': email,
                    'subject': 'New KwickPOS Online Order:  '+dba,
                })
                online_order_template.with_context(ctx).send_mail(online_order_form_res.id, force_send=True)
            else :
                ctx.update({
                    'email_from': request.env.user.company_id.catchall_email,
                    'email_to': 'accounting@zbspos.com',
                    'reply_to': email,
                    'subject': 'Deposit Required:  '+dba
                })
                online_order_template.with_context(ctx).send_mail(online_order_form_res.id, force_send=True)
            ctx.update({
                'email_from': request.env.user.company_id.catchall_email,
                'email_to': 'form@zbspos.com',
                'reply_to': email,
                'subject': 'New KwickPOS Online Order:  '+dba
            })
            online_order_template.with_context(ctx).send_mail(online_order_form_res.id, force_send=True)
            ctx.update({
                'email_from': request.env.user.company_id.catchall_email,
                'email_to': 'deployment@zbspos.com',
                'reply_to': email,
                'subject': 'New KwickPOS Online Order:  '+dba
            })
            online_order_template.with_context(ctx).send_mail(online_order_form_res.id, force_send=True)
            ctx.update({
                'email_from': request.env.user.company_id.catchall_email,
                'email_to': 'oo@zbspos.com',
                'reply_to': email,
                'subject': 'New KwickPOS Online Order:  '+dba
            })
            online_order_template.with_context(ctx).send_mail(online_order_form_res.id, force_send=True)
            headers = {'Content-Type': 'application/json'}
            body = {'results': {'code': 201, 'message': "The Email has been sent successfully"}}

            return Response(json.dumps(body), headers=headers)
        except Exception as e:
            # raise ValidationError(e)
            _logger.info("Generate online order PDF contract error:  %s ", e)
            headers = {'Content-Type': 'application/json'}
            body = {'results': {'code': 501, 'message': "Oops , something is wrong ,please try it later"}}

            return Response(json.dumps(body), headers=headers)
        # partner_id = request.env['res.partner'].sudo().search(
        #     [('name', '=', '8642072760 - test')
        #      ])
        # partner_id.write({"ach_form_pdf": b64_pdf})
        # render_values = {
        #     'success': True,
        # }
        # return request.render("website_application.email_sent", render_values)

    @http.route(['/application_new_merchant/submit'], auth="public", type='http', methods=['POST'],
                website=True, csrf=False)
    def application_new_merchant_submit(self, **kw):
        account_type = kw.get('account_type', False)
        account_type = False if account_type == 'undefined' else account_type
        account_type_dict = {
            '1': 'New Account',
            '2': 'Change Owner',
            '3': 'Change Legal Info',
        }
        account_type_string = account_type_dict.get(account_type, '')
        old_mid = kw.get('old_mid', False)
        old_mid = False if old_mid == 'undefined' else old_mid
        is_add_paper_plan = kw.get('is_add_paper_plan', False)
        is_add_paper_plan = False if is_add_paper_plan == 'undefined' else is_add_paper_plan
        is_add_paper_plan_dict = {
            '1': 'Yes',
            '2': 'No',
        }
        is_add_paper_plan_string = is_add_paper_plan_dict.get(is_add_paper_plan, '')
        add_supply_order_dict = {
            'true': 'Yes',
            'false': 'No',

        }
        checkbook = kw.get('checkbook', False)
        checkbook = False if checkbook == 'undefined' else checkbook
        checkbook_string = add_supply_order_dict.get(checkbook, '')
        tips_trays = kw.get('tips_trays')
        tips_trays = False if tips_trays == 'undefined' else tips_trays
        tips_trays_string = add_supply_order_dict.get(tips_trays)
        no_supply_order_needed = kw.get('no_supply_order_needed', False)
        no_supply_order_needed = False if no_supply_order_needed == 'undefined' else no_supply_order_needed
        no_supply_order_needed_string = add_supply_order_dict.get(no_supply_order_needed, '')

        standalone_or_semi = kw.get('standalone_or_semi', False)
        standalone_or_semi = False if standalone_or_semi == 'undefined' else standalone_or_semi
        standalone_or_semi_dict = {
            '1': 'Standalone',
            '2': 'Semi-Integration',
        }
        standalone_or_semi_string = standalone_or_semi_dict.get(standalone_or_semi, '')
        equipment_type = kw.get('equipment_type', False)
        equipment_type = False if equipment_type == 'undefined' else equipment_type
        equipment = kw.get('equipment', False)
        equipment = False if equipment == 'undefined' else equipment
        equipment_dict = {
            '1': 'PAX S80',
            '2': 'PAX S300',
            '3': 'PAX S500',
            '4': 'FD 50',
            '5': 'Clover',
            '6': 'other',
        }
        equipment_string = equipment_dict.get(equipment, '')

        bill_to = kw.get('bill_to', False)
        bill_to = False if bill_to == 'undefined' else bill_to
        bill_to_dict = {
            '1': 'Agent',
            '2': 'Merchant',

        }
        bill_to_string = bill_to_dict.get(bill_to, '')
        equipment_quantity = kw.get('equipment_quantity', False)
        equipment_quantity = False if equipment_quantity == 'undefined' else equipment_quantity
        feature_dict = {
            'true': 'Yes',
            'false': 'No',

        }
        feature_restaurant = kw.get('feature_restaurant', False)
        equipment_quantity = False if equipment_quantity == 'undefined' else equipment_quantity
        feature_restaurant_string = feature_dict.get(feature_restaurant, '')
        feature_retail = kw.get('feature_retail', False)
        feature_retail = False if feature_retail == 'undefined' else feature_retail
        feature_retail_string = feature_dict.get(feature_retail, '')
        feature_with_tips = kw.get('feature_with_tips', False)
        feature_with_tips = False if feature_with_tips == 'undefined' else feature_with_tips
        feature_with_tips_string = feature_dict.get(feature_with_tips, '')
        feature_dial = kw.get('feature_dial', False)
        feature_dial = False if feature_dial == 'undefined' else feature_dial
        feature_dial_string = feature_dict.get(feature_dial, '')
        feature_pin_debit = kw.get('feature_pin_debit', False)
        feature_pin_debit = False if feature_pin_debit == 'undefined' else feature_pin_debit
        feature_pin_debit_string = feature_dict.get(feature_pin_debit, '')
        feature_server_id = kw.get('feature_server_id')
        feature_server_id = False if feature_server_id == 'undefined' else feature_server_id
        feature_server_id_string = feature_dict.get(feature_server_id, '')
        feature_ip = kw.get('feature_ip', False)
        feature_ip = False if feature_ip == 'undefined' else feature_ip
        feature_ip_string = feature_dict.get(feature_ip, '')
        feature_ip_input = kw.get('feature_ip_input', False)
        feature_ip_input = False if feature_ip_input == 'undefined' else feature_ip_input
        feature_auto_time_batch = kw.get('feature_auto_time_batch', False)
        feature_auto_time_batch = False if feature_auto_time_batch == 'undefined' else feature_auto_time_batch
        feature_auto_time_batch_string = feature_dict.get(feature_auto_time_batch, '')
        feature_auto_batch_time_input = kw.get('feature_auto_batch_time_input', False)
        feature_auto_batch_time_input = False if feature_auto_batch_time_input == 'undefined' else feature_auto_batch_time_input
        feature_tip_suggestions = kw.get('feature_tip_suggestions', False)
        feature_tip_suggestions = False if feature_tip_suggestions == 'undefined' else feature_tip_suggestions
        feature_tip_suggestions_string = feature_dict.get(feature_tip_suggestions, '')
        feature_tip_suggestions_input = kw.get('feature_tip_suggestions_input')
        feature_tip_suggestions_input = False if feature_tip_suggestions_input == 'undefined' else feature_tip_suggestions_input
        feature_other_feature = kw.get('feature_other_feature', False)
        feature_other_feature = False if feature_other_feature == 'undefined' else feature_other_feature
        feature_other_feature_string = feature_dict.get(feature_other_feature, '')
        feature_other_feature_input = kw.get('feature_other_feature_input')
        feature_other_feature_input = False if feature_other_feature_input == 'undefined' else feature_other_feature_input

        deployment_method = kw.get('deployment_method', False)
        deployment_method = False if deployment_method == 'undefined' else deployment_method
        deployment_method_dict = {
            '1': 'Agent Pickup',
            '2': 'Call Merchant Pickup',
            '3': 'POS Team Install',
            '4': 'Ship To DBA Address',
            '5': 'Ship To Other Address',
            '6': 'Re-Programming',

        }
        deployment_method_string = deployment_method_dict.get(deployment_method, '')
        is_ship_with_pos = kw.get('is_ship_with_pos', False)
        is_ship_with_pos = False if is_ship_with_pos == 'undefined' else is_ship_with_pos
        is_ship_with_pos_dict = {
            '1': 'Agent Pickup',
            '2': 'Call Merchant Pickup',
        }
        is_ship_with_pos_string = is_ship_with_pos_dict.get(is_ship_with_pos, '')
        ship_out_address = kw.get('ship_out_address')
        ship_out_address = False if ship_out_address == 'undefined' else ship_out_address
        ship_out_city = kw.get('ship_out_city')
        ship_out_city = False if ship_out_city == 'undefined' else ship_out_city
        ship_out_zip = kw.get('ship_out_zip')
        ship_out_zip = False if ship_out_zip == 'undefined' else ship_out_zip
        ship_out_state = kw.get('ship_out_state')
        ship_out_state = False if ship_out_state == 'undefined' else ship_out_state
        reprogram_old_mid = kw.get('reprogram_old_mid')
        reprogram_old_mid = False if reprogram_old_mid == 'undefined' else reprogram_old_mid
        pricing_type = kw.get('pricing_type', False)
        pricing_type = False if pricing_type == 'undefined' else pricing_type
        pricing_type_dict = {
            '1': 'Interchange',
            '2': 'Flat Rate',
            '3': 'Cash Discount (by Percentage %)',
            '4': 'Cash Discount (by Flat Fee $))',
        }
        pricing_type_string = pricing_type_dict.get(pricing_type, '')
        visa_sales_discount_fee = kw.get('visa_sales_discount_fee', False)
        visa_sales_discount_fee = False if visa_sales_discount_fee == 'undefined' else visa_sales_discount_fee
        visa_auth_fee = kw.get('visa_auth_fee', False)
        visa_auth_fee = False if visa_auth_fee == 'undefined' else visa_auth_fee
        amex_sales_discount_fee = kw.get('amex_sales_discount_fee', False)
        amex_sales_discount_fee = False if amex_sales_discount_fee == 'undefined' else amex_sales_discount_fee
        amex_auth_fee = kw.get('amex_auth_fee', False)
        amex_auth_fee = False if amex_auth_fee == 'undefined' else amex_auth_fee
        cash_discount_rate = kw.get('cash_discount_rate', False)
        cash_discount_rate = False if cash_discount_rate == 'undefined' else cash_discount_rate
        if_want_free_cash_discount = kw.get('if_want_free_cash_discount', False)
        if_want_free_cash_discount = False if if_want_free_cash_discount == 'undefined' else if_want_free_cash_discount
        if_want_free_cash_discount_dict = {
            '1': 'Yes',
            '2': 'No',
        }
        if_want_free_cash_discount_string = if_want_free_cash_discount_dict.get(if_want_free_cash_discount, '')
        monthly_fee = kw.get('monthly_fee')
        other_comment = kw.get('other_comment')
        date = kw.get('date')

        agent_name = kw.get('agent_name')
        agent_email = kw.get('agent_email')
        name_of_company = kw.get('name_of_company')
        dba = kw.get('dba')
        address = kw.get('address')
        city = kw.get('city')
        state = kw.get('state')
        zip_code = kw.get('zip_code')
        business_phone_number = kw.get('business_phone_number')
        fax_number = kw.get('fax_number')
        federal_tax_id = kw.get('federal_tax_id')
        type_of_business = kw.get('type_of_business')
        company_type = kw.get('company_type', False)
        company_type = False if company_type == 'undefined' else company_type
        company_type_dict = {
            '1': 'Sole Proprietorship (独资)',
            '2': 'Private Corp. (公司)',
            '3': 'Limited Liability Co. (公司)',
            '4': 'Partnership (合伙)',
        }
        company_type_string = company_type_dict.get(company_type, '')
        open_date = kw.get('open_date')
        estimated_monthly_sale_volume = kw.get('estimated_monthly_sale_volume')
        average_sales_account = kw.get('average_sales_account')
        amex = kw.get('amex', False)
        amex = False if amex == 'undefined' else amex
        amex_dict = {
            '1': 'Yes',
            '2': 'No',
        }
        amex_string = amex_dict.get(amex, '')
        owner_name = kw.get('owner_name')
        owner_email = kw.get('owner_email')
        owner_title = kw.get('owner_title')
        owner_phone_number = kw.get('owner_phone_number')
        owner_home_address = kw.get('owner_home_address')
        owner_home_city = kw.get('owner_home_city')
        owner_home_state = kw.get('owner_home_state')
        owner_home_zip_code = kw.get('owner_home_zip_code')
        ssn = kw.get('ssn')
        owner_date_of_birth = kw.get('owner_date_of_birth')
        owner_driver_license_number = kw.get('owner_driver_license_number')
        owner_state_issued = kw.get('owner_state_issued')
        owner_bank_name = kw.get('owner_bank_name')
        owner_bank_routing = kw.get('owner_bank_routing')
        owner_bank_account = kw.get('owner_bank_account')

        sign_date = kw.get('sign_date')
        personal_guarantee_sign_date = kw.get('personal_guarantee_sign_date')
        print_client_business_legal_name = kw.get('print_client_business_legal_name')
        print_name_signer = kw.get('print_name_signer')
        business_principle_title = kw.get('business_principle_title')
        business_principle_sign_date = kw.get('business_principle_sign_date')

        try:
            if kw.get('id', False):
                merchant_form_id = kw.get('id', False)
                merchant_form_res = request.env['merchant.form'].sudo().search([["id", "=", int(merchant_form_id)]])
                merchant_form_res.sudo().update({
                    'account_type': account_type,
                    'old_mid': old_mid,
                    'is_add_paper_plan': is_add_paper_plan,
                    'checkbook': checkbook_string,
                    'tips_trays': tips_trays_string,
                    'no_supply_order_needed': no_supply_order_needed_string,
                    'standalone_or_semi': standalone_or_semi,
                    'equipment_type': equipment_type,
                    'equipment': equipment,
                    'bill_to': bill_to,
                    'equipment_quantity': equipment_quantity,
                    'feature_restaurant': feature_restaurant_string,
                    'feature_retail': feature_retail_string,
                    'feature_with_tips': feature_with_tips_string,
                    'feature_dial': feature_dial_string,
                    'feature_pin_debit': feature_pin_debit_string,
                    'feature_server_id': feature_server_id_string,
                    'feature_ip': feature_ip_string,
                    'feature_auto_time_batch': feature_auto_time_batch_string,
                    'feature_tip_suggestions': feature_tip_suggestions_string,
                    'feature_other_feature': feature_other_feature_string,
                    'feature_ip_input': feature_ip_input,
                    'feature_auto_batch_time_input': feature_auto_batch_time_input,
                    'feature_tip_suggestions_input': feature_tip_suggestions_input,
                    'feature_other_feature_input': feature_other_feature_input,
                    'deployment_method': deployment_method,
                    'is_ship_with_pos': is_ship_with_pos,
                    'ship_out_address': ship_out_address,
                    'ship_out_city': ship_out_city,
                    'ship_out_zip': ship_out_zip,
                    'ship_out_state': ship_out_state,
                    'reprogram_old_mid': reprogram_old_mid,
                    'pricing_type': pricing_type,
                    'visa_sales_discount_fee': visa_sales_discount_fee,
                    'visa_auth_fee': visa_auth_fee,
                    'amex_sales_discount_fee': amex_sales_discount_fee,
                    'amex_auth_fee': amex_auth_fee,
                    'cash_discount_rate': cash_discount_rate,
                    'if_want_free_cash_discount': if_want_free_cash_discount,
                    'monthly_fee': monthly_fee,
                    'other_comment': other_comment,
                    'date': date,

                    'agent_name': agent_name,
                    'agent_email': agent_email,
                    'name_of_company': name_of_company,
                    'dba': dba,
                    'address': address,
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'business_phone_number': business_phone_number,
                    'fax_number': fax_number,
                    'federal_tax_id': federal_tax_id,
                    'type_of_business': type_of_business,
                    'company_type': company_type,
                    'open_date': open_date,
                    'estimated_monthly_sale_volume': estimated_monthly_sale_volume,
                    'average_sales_account': average_sales_account,
                    'amex': amex,

                    'owner_name': owner_name,
                    'owner_email': owner_email,
                    'owner_title': owner_title,
                    'owner_phone_number': owner_phone_number,
                    'owner_home_address': owner_home_address,
                    'owner_home_city': owner_home_city,
                    'owner_home_state': owner_home_state,
                    'owner_home_zip_code': owner_home_zip_code,
                    'ssn': ssn,
                    'owner_date_of_birth': owner_date_of_birth,
                    'owner_driver_license_number': owner_driver_license_number,
                    'owner_state_issued': owner_state_issued,
                    'owner_bank_name': owner_bank_name,
                    'owner_bank_routing': owner_bank_routing,
                    'owner_bank_account': owner_bank_account,

                    'sign_date': sign_date,
                    'personal_guarantee_sign_date': personal_guarantee_sign_date,
                    'print_client_business_legal_name': print_client_business_legal_name,
                    'print_name_signer': print_name_signer,
                    'business_principle_title': business_principle_title,
                    'business_principle_sign_date': business_principle_sign_date,


                })
            else:
                merchant_form_res = request.env['merchant.form'].sudo().create({
                    'account_type': account_type,
                    'old_mid': old_mid,
                    'is_add_paper_plan': is_add_paper_plan,
                    'checkbook': checkbook_string,
                    'tips_trays': tips_trays_string,
                    'no_supply_order_needed': no_supply_order_needed_string,
                    'standalone_or_semi': standalone_or_semi,
                    'equipment_type': equipment_type,
                    'equipment': equipment,
                    'bill_to': bill_to,
                    'equipment_quantity': equipment_quantity,
                    'feature_restaurant': feature_restaurant_string,
                    'feature_retail': feature_retail_string,
                    'feature_with_tips': feature_with_tips_string,
                    'feature_dial': feature_dial_string,
                    'feature_pin_debit': feature_pin_debit_string,
                    'feature_server_id': feature_server_id_string,
                    'feature_ip': feature_ip_string,
                    'feature_auto_time_batch': feature_auto_time_batch_string,
                    'feature_tip_suggestions': feature_tip_suggestions_string,
                    'feature_other_feature': feature_other_feature_string,
                    'feature_ip_input': feature_ip_input,
                    'feature_auto_batch_time_input': feature_auto_batch_time_input,
                    'feature_tip_suggestions_input': feature_tip_suggestions_input,
                    'feature_other_feature_input': feature_other_feature_input,
                    'deployment_method': deployment_method,
                    'is_ship_with_pos': is_ship_with_pos,
                    'ship_out_address': ship_out_address,
                    'ship_out_city': ship_out_city,
                    'ship_out_zip': ship_out_zip,
                    'ship_out_state': ship_out_state,
                    'reprogram_old_mid': reprogram_old_mid,
                    'pricing_type': pricing_type,
                    'visa_sales_discount_fee': visa_sales_discount_fee,
                    'visa_auth_fee': visa_auth_fee,
                    'amex_sales_discount_fee': amex_sales_discount_fee,
                    'amex_auth_fee': amex_auth_fee,
                    'cash_discount_rate': cash_discount_rate,
                    'if_want_free_cash_discount': if_want_free_cash_discount,
                    'monthly_fee': monthly_fee,
                    'other_comment': other_comment,
                    'date': date,

                    'agent_name': agent_name,
                    'agent_email': agent_email,
                    'name_of_company': name_of_company,
                    'dba': dba,
                    'address': address,
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'business_phone_number': business_phone_number,
                    'fax_number': fax_number,
                    'federal_tax_id': federal_tax_id,
                    'type_of_business': type_of_business,
                    'company_type': company_type,
                    'open_date': open_date,
                    'estimated_monthly_sale_volume': estimated_monthly_sale_volume,
                    'average_sales_account': average_sales_account,
                    'amex': amex,

                    'owner_name': owner_name,
                    'owner_email': owner_email,
                    'owner_title': owner_title,
                    'owner_phone_number': owner_phone_number,
                    'owner_home_address': owner_home_address,
                    'owner_home_city': owner_home_city,
                    'owner_home_state': owner_home_state,
                    'owner_home_zip_code': owner_home_zip_code,
                    'ssn': ssn,
                    'owner_date_of_birth': owner_date_of_birth,
                    'owner_driver_license_number': owner_driver_license_number,
                    'owner_state_issued': owner_state_issued,
                    'owner_bank_name': owner_bank_name,
                    'owner_bank_routing': owner_bank_routing,
                    'owner_bank_account': owner_bank_account,

                    'sign_date': sign_date,
                    'personal_guarantee_sign_date': personal_guarantee_sign_date,
                    'print_client_business_legal_name': print_client_business_legal_name,
                    'print_name_signer': print_name_signer,
                    'business_principle_title': business_principle_title,
                    'business_principle_sign_date': business_principle_sign_date,

                    'if_hidden_for_merchant': True,
                    'completely_fill': True,
                    'verify_information': True
                })
        except Exception as e:
            _logger.info("create merchant.form model goes wrong %s", e)

        new_merchant_template_id = request.env.ref(
            'website_application.email_template_application_new_merchant_form').id
        new_merchant_template = request.env['mail.template'].sudo().browse(new_merchant_template_id)

        if kw.get('signature', False):
            signature = kw.get('signature', False)
            signature_content = signature.split(';')[1]
            signature_encoded = signature_content.split(',')[1]
            merchant_form_res.write(
                {'signature': signature_encoded.encode('utf-8')})
        if kw.get('personal_guarantee_signature', False):
            personal_guarantee_signature = kw.get('personal_guarantee_signature', False)
            personal_guarantee_signature_content = personal_guarantee_signature.split(';')[1]
            personal_guarantee_signature_encoded = personal_guarantee_signature_content.split(',')[1]
            merchant_form_res.write(
                {'personal_guarantee_signature': personal_guarantee_signature_encoded.encode('utf-8')})
        if kw.get('client_initials_signature', False):
            client_initials_signature = kw.get('client_initials_signature', False)
            client_initials_signature_content = client_initials_signature.split(';')[1]
            client_initials_signature_encoded = client_initials_signature_content.split(',')[1]
            merchant_form_res.write(
                {'client_initials_signature': client_initials_signature_encoded.encode('utf-8')})
        if kw.get('client_business_principle_signature', False):
            client_business_principle_signature = kw.get('client_business_principle_signature', False)
            client_business_principle_signature_content = client_business_principle_signature.split(';')[1]
            client_business_principle_signature_encoded = client_business_principle_signature_content.split(',')[1]
            merchant_form_res.write({'client_business_principle_signature': client_business_principle_signature_encoded.encode('utf-8')})

        attachment_ids = []
        if kw.get('menu_document', False):
            menu_document = kw.get('menu_document')
            menu_document_ir_values = {
                'name': "new_merchant_menu_file",
                'type': 'binary',
                'datas': base64.b64encode(menu_document.read()),
                'is_web_attachment': True
            }
            menu_file_data_id = request.env['ir.attachment'].sudo().create(menu_document_ir_values)
            merchant_form_res.write({'menu_document': menu_file_data_id.datas})
            attachment_ids.append(menu_file_data_id.id)
        if kw.get('void_check_document', False):
            void_check_document_file = kw.get('void_check_document')
            void_check_document_ir_values = {
                'name': "new_merchant_void_check_document",
                'type': 'binary',
                'datas': base64.b64encode(void_check_document_file.read()),

                'is_web_attachment': True
            }
            void_check_document_data_id = request.env['ir.attachment'].sudo().create(void_check_document_ir_values)
            merchant_form_res.write({'void_check_document': void_check_document_data_id.datas})
            attachment_ids.append(void_check_document_data_id.id)
        if kw.get('irs_document', False):
            irs_document_file = kw.get('irs_document')
            irs_document_ir_values = {
                'name': "new_merchant_irs_document_file",
                'type': 'binary',
                'datas': base64.b64encode(irs_document_file.read()),
                'is_web_attachment': True
            }
            irs_document_file_data_id = request.env['ir.attachment'].sudo().create(irs_document_ir_values)
            merchant_form_res.write({'irs_document': irs_document_file_data_id.datas})
            attachment_ids.append(irs_document_file_data_id.id)
        if kw.get('owner_id_document', False):
            owner_id_document_file = kw.get('owner_id_document')
            irs_document_ir_values = {
                'name': "new_merchant_owner_id_document",
                'type': 'binary',
                'datas': base64.b64encode(owner_id_document_file.read()),

                'is_web_attachment': True
            }
            owner_id_document_data_id = request.env['ir.attachment'].sudo().create(irs_document_ir_values)
            merchant_form_res.write({'owner_id_document': owner_id_document_data_id.datas})
            attachment_ids.append(owner_id_document_data_id.id)

        if kw.get('sharing_link', False):

            merchant_form_res.write({'if_hidden_for_merchant': True,
                                         'completely_fill': True,
                                        'verify_information': True,
                                        'if_shared_form':True})
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = base_url + '/application_new_merchant/' + str(merchant_form_res.id)
            headers = {'Content-Type': 'application/json'}
            body = {'results': {'code': 200, 'url': url}}

            return Response(json.dumps(body), headers=headers)

        try:
            pdf = request.env.ref('website_application.action_report_new_merchant_form').sudo()._render_qweb_pdf(
                merchant_form_res.ids)[0]
            b64_pdf = base64.b64encode(pdf)
            new_merchant_pdf = request.env['ir.attachment'].sudo().create({
                'type': 'binary',
                'datas': b64_pdf,
                'name': 'new merchant contract' + '.pdf',
                'mimetype': 'application/x-pdf'
            })
            attachment_ids.append(new_merchant_pdf.id)
            new_merchant_template.attachment_ids = [(6, 0, attachment_ids)]
            ctx = request.env.context.copy()
            ctx.update({
                'email_from': request.env.user.company_id.catchall_email,
                'email_to': agent_email,
                'subject': 'We have received your response for ' + dba,
                'reply_to': 'form@zbspos.com',
                'account_type': account_type_string,
                'is_add_paper_plan': is_add_paper_plan_string,
                'checkbook': checkbook,
                'tips_trays': tips_trays,
                'no_supply_order_needed': no_supply_order_needed,
                'standalone_or_semi': standalone_or_semi_string,
                'equipment': equipment_string,
                'bill_to': bill_to_string,
                'deployment_method': deployment_method_string,
                'is_ship_with_pos': is_ship_with_pos_string,
                'pricing_type': pricing_type_string,
                'company_type': company_type_string,
                'if_want_free_cash_discount': if_want_free_cash_discount_string,
                'amex': amex_string,
                'signature': signature,
                'personal_guarantee_signature': personal_guarantee_signature,
                'client_initials_signature': client_initials_signature,
                'client_business_principle_signature': client_business_principle_signature,

            })
            new_merchant_template.with_context(ctx).send_mail(merchant_form_res.id, force_send=True)
            ctx.update({
                'email_to': owner_email,
            })
            new_merchant_template.with_context(ctx).send_mail(merchant_form_res.id, force_send=True)

            agent_employee = request.env['hr.employee'].sudo().search(
                [('work_email', '=', agent_email)
                 ])

            if agent_employee.parent_id:
                ctx.update({
                    'email_to': agent_employee.parent_id.work_email,
                    'subject': "New Application:" + dba + '-' + agent_name
                })
                new_merchant_template.with_context(ctx).send_mail(merchant_form_res.id, force_send=True)
            ctx.update({
                'email_to': 'na@zbspos.com',
                'subject': "New Application:" + dba + '-' + agent_name
            })
            new_merchant_template.with_context(ctx).send_mail(merchant_form_res.id, force_send=True)

            headers = {'Content-Type': 'application/json'}
            body = {'results': {'code': 201, 'message': "The Email has been sent successfully"}}

            return Response(json.dumps(body), headers=headers)
        except Exception as e:
            _logger.info("Generate new merchant PDF contract error:  %s ", e)
            headers = {'Content-Type': 'application/json'}
            body = {'results': {'code': 501, 'message': "oops something wrong, please try it later"}}

            return Response(json.dumps(body), headers=headers)
        # partner_id = request.env['res.partner'].sudo().search(
        #     [('name', '=', '8642072760 - test')
        #      ])
        # partner_id.write({"ach_form_pdf": b64_pdf})
        # render_values = {
        #     'success': True,
        # }
        # return request.render("website_application.email_sent", render_values)

    @http.route(['/application_questionnaire/submit'], auth="public", type='http', methods=['POST'],
                    website=True)
    def application_questionnaire_submit(self, **kw):
        user = request.env.user
        ctx = request.env.context.copy()

        difficult_dict = { '1':' 很困难 Very Difficult',
                           '2':' 困难 Difficult',
                           '3':' 一般 Average',
                           '4':' 简单 Easy',
                           '5':' 很简单 Very Easy',}
        satisfaction_dict = { '5':' 非常不满意 Not Satisfied at all',
                           '4':' 不满意 Not satisfied',
                           '3':' 一般 Average',
                           '2':' 满意 Satisfied',
                           '1':' 非常满意 Very satisfied',}
        yes_dict = { '1':'Yes',
                           '2':'No',
                           }

        question1 = ""
        question2 = ""
        question3 = ""
        question4 = ""
        question5 = ""
        phone_number = kw.get("phone_number")
        if kw.get("question1"):
            question1 = satisfaction_dict.get(kw.get("question1"))
        if kw.get("question2"):
            question2 = yes_dict.get(kw.get("question2"))
        if kw.get("question3"):
            question3 = yes_dict.get(kw.get("question3"))
        if kw.get("question4"):
            question4 = yes_dict.get(kw.get("question4"))
        if kw.get("question5"):
            question5 = yes_dict.get(kw.get("question4"))

        if kw.get("new_feature"):
            ctx.update({
                'new_feature': kw.get("new_feature"),
            })
        ctx.update({
            'phone_number': phone_number,
            'question1': question1,
            'question2': question2,
            'question3': question3,
            'question4': question4,
            'question5': question5,
        })

        mail_template_id = request.env.ref('website_application.application_questionnaire').sudo()
        try:
            ctx.update({
                'email_from': request.env.user.company_id.catchall_email,
                'email_to': 'lingy@zbspos.com',
            })
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)
            ctx.update({
                'email_from': request.env.user.company_id.catchall_email,
                'email_to': 'kevin@zbspos.com',
            })
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)
            ctx.update({
                'email_from': request.env.user.company_id.catchall_email,
                'email_to': 'vickin@zbspos.com',
            })
            mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)
            render_values = {
                'success': True,
            }
            return request.render("website_application.email_sent", render_values)
        except ValueError:
            render_values = {
                'success': False,
                'message': "something went wrong"
            }
            return request.render("website_application.email_sent", render_values)
