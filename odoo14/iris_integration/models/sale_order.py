# -*- coding: utf-8 -*-
import requests
import json
import logging
import datetime
from odoo import api, fields, models, _
import gspread
from odoo.modules.module import get_module_resource
import time
_logger = logging.getLogger(__name__)


odoo_user_to_iris_user = {
    '44':'416',
    '182':'187',
    '29':'351',
    '30':'300',
}

class RotationCanceledUser(models.Model):
    _name = "rotation.canceled.user"

    user_id = fields.Many2one('res.users', string='User canceled')
    sale_order = fields.Many2one('sale.order', string='Sale order canceled')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_studio_many2many_field_IExXi = fields.Many2many('project.project', 'x_product_template_project_project_rel', 'product_template_id', 'project_project_id',string="Project")



class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_studio_assign_to = fields.Many2one('res.users', string='Assign to', tracking=True)
    standalone_task = fields.Many2one('project.task', string='Standalone Task')
    is_ticket_resolved = fields.Boolean()
    x_studio_ticket__1 = fields.Char(tracking=True)
    ticket_iris_link = fields.Char(string='Iris Ticket Link', compute='compute_iris_link_using_ticket_id')
    status_payment = fields.Selection([
                    ('not_invoiced', 'NOT INVOICED'),
                    ('draft_invoice', 'DRAFT INVOICE'),
                    ('invoice_posted', 'INVOICE POSTED'),
                    ('partially_paid', 'PARTIALLY PAID'),
                    ('fully_paid', 'FULLY PAID'),
                    ('cancel', 'Cancelled'),
                    ('bad_debt', 'BAD DEBT')
    ], tracking=True)
    last_canceled_order = fields.Many2one('sale.order', string='Last canceled order', tracking=True)

    @api.depends('x_studio_ticket__1')
    def compute_iris_link_using_ticket_id(self):
        for obj in self:
            if obj.x_studio_ticket__1:
                obj.ticket_iris_link = 'https://crm.zbspos.com/helpdesk/ticket/' + str(obj.x_studio_ticket__1)
            else:
                obj.ticket_iris_link = False

    @api.onchange('x_studio_assign_to')
    def _onchange_assign_to(self):
        try:
            if self.x_studio_ticket__1:
                headers = {'Content-Type': 'application/json',
                           'Accept': 'application/json'}
                IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
                headers.update({'X-API-KEY': IRIS_API_KEY})
                iris_ticket_url = "	https://crm.zbspos.com/api/v1/helpdesk"
                assign_users = []
                if self.x_studio_assign_to:
                    iris_user = odoo_user_to_iris_user.get(str(self.x_studio_assign_to.id), 0)
                    assign_users.append(int(iris_user))
                iris_ticket_data = {
                    "assignedUsers": assign_users
                }

                response = requests.patch(iris_ticket_url + '/' + self.x_studio_ticket__1, data=json.dumps(iris_ticket_data),
                                          headers=headers)
        except Exception as e:
            _logger.info("Syn sale order's assign to ,error:  %s ", e)

    def so_to_iris(self):
        """
          Send Sales to IRIS when SO Confirmed
        """
        iris_url = "https://zbs.iriscrm.com/api/v1/leads/"
        iris_api_key = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
        if self.partner_id.x_studio_lead_id:
            lead_id = self.partner_id.x_studio_lead_id
            url = iris_url + lead_id + '/notes'
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json'}
            headers.update({'X-API-KEY': iris_api_key})
            base_url = self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url') + self.get_portal_url()
            data = {
                "tab": 2,
                "note": 'Odoo Sales Order: ' + base_url,
                "sticky": "Yes"
            }
            response = requests.post(url,
                                     data=json.dumps(data), headers=headers)
            _logger.info("== response : %s ", json.loads(response.text))
            history_obj = self.env['iris.integration.history']
            history_obj.create({'order_id': self.id,
                                'user_id': self.env.user.id,
                                'response':  json.loads(response.text)})
            message = 'Sent sales order to IRIS Lead ' + str(lead_id)
            self.message_post(body=message)

    def create_response_history(self, response, message):
        history_obj = self.env['iris.integration.history']
        history_obj.create({
                            'user_id': self.env.user.id,
                            'note': 'Sent the Contact to IRIS',
                            'response': response})
        self.message_post(body=message)

    def resolve_ticket_in_iris(self):
        domain = ["&", "&", "&", "&", "|", ['state', '=', 'sale'], ['state', '=', 'cancel'], ['x_studio_ticket__1', '!=', False],
             ['is_ticket_resolved', '=', False], ['date_order', '>=', datetime.date.today()-datetime.timedelta(days=50)],
                  "|", ['status_delivery', '=', 'delivered'], ['status_delivery', '=', 'partially']]
        # domain = [['id', '=', 8017]]
        orders = self.env['sale.order'].search(domain, order="write_date desc")
        # target_users = self.env['res.users'].search([('id', '=', 68)])
        # channel_odoo_bot_users = '%s, %s' % (odoo_bot.name, employee.user_id.name)
        channel_obj = self.env['mail.channel']
        channel_id = channel_obj.search([
            ('id', '=', 138)
        ])
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
        headers.update({'X-API-KEY': IRIS_API_KEY})
        iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
        for order in orders:
            if_skip = False
            for order_line in order.order_line:
                if order_line.product_id and not order_line.product_id.if_need_resolved and order.sale_order_type != 'new' and order.sale_order_type !='conversion':
                    if_skip = True
            if if_skip:
                continue
            if order.x_studio_ticket__1 and not order.is_ticket_resolved:
                if order.state == "cancel" or order.sale_order_type == "add_ons":
                    ticket_info_response = requests.get(iris_ticket_url + '/' + str(order.x_studio_ticket__1),
                                                        headers=headers)
                    if ticket_info_response.status_code == 200:
                        ticket_info_response_data = json.loads(ticket_info_response.text)
                        updated_checklist = []
                        for check in ticket_info_response_data['checklist']:
                            note = "Done"
                            tmp_dict = {'index': check['index'],
                                        'completed': True,
                                        'comment':  note}
                            updated_checklist.append(tmp_dict)
                        iris_ticket_data = {
                            "checklist": updated_checklist,
                            "status": "resolved",
                        }
                        resolved_ticket_type_list = [385, 386, 387]
                        if ticket_info_response_data['general']['type']['id'] in resolved_ticket_type_list:
                            response_update_checklist = requests.patch(
                                iris_ticket_url + "/" + str(order.x_studio_ticket__1),
                                data=json.dumps(iris_ticket_data),
                                headers=headers)
                            order.write({'is_ticket_resolved': True})
                            _logger.info("resolve checklist response : %s ", json.loads(response_update_checklist.text))
                else:
                    activities = order.activity_ids
                    if len(activities) <= 5:

                        iris_ticket_data_update_ticket_status = {
                            "status": "resolved",
                        }
                        resolved_ticket_type_list = [385, 386, 387]
                        ticket_info_response = requests.get(iris_ticket_url + '/' + str(order.x_studio_ticket__1), headers=headers)
                        try:
                            if ticket_info_response.status_code == 200:
                                ticket_info_response_data = json.loads(ticket_info_response.text)
                                if ticket_info_response_data['general']['type']['id'] in resolved_ticket_type_list:
                                    response_update_checklist = requests.patch(
                                        iris_ticket_url + "/" + str(order.x_studio_ticket__1),
                                        data=json.dumps(iris_ticket_data_update_ticket_status),
                                        headers=headers)
                                    _logger.info("resolve ticket  response : %s ", json.loads(response_update_checklist.text))
                                    if response_update_checklist.status_code == 200:
                                        order.write({'is_ticket_resolved': True})
                                    else:
                                        re = channel_id.message_post(
                                            subject="Iris failed request reminder",
                                            body="Fail to resolve the ticket#" + str(order.x_studio_ticket__1) + " in Iris,the reason: " + response_update_checklist.text,
                                            message_type='comment',
                                            subtype_id=self.env.ref('mail.mt_comment').id
                                        )
                        except Exception as e:  # This is the correct syntax
                            order.create_response_history(response_update_checklist, "Fail to resolve the ticket#" + str(order.x_studio_ticket__1) + " in Iris")
                            re = channel_id.message_post(
                                subject="Iris failed request reminder",
                                body="Fail to resolve the ticket#" + str(order.x_studio_ticket__1) + " in Iris",
                                message_type='comment',
                                subtype_id=self.env.ref('mail.mt_comment').id
                            )
        # semi/standalone project resolve standalone task ticket
        task_domain = [('ticket', '!=', False),
                        ('project_id', '=', 44),
                       ('is_ticket_resolved', '=', False)
                  ]
        tasks = self.env['project.task'].search(task_domain, order="write_date desc")
        for task in tasks:
            iris_ticket_data_update_ticket_status = {
                "status": "resolved",
            }
            try:
                response_update_checklist = requests.patch(
                    iris_ticket_url + "/" + str(task.ticket),
                    data=json.dumps(iris_ticket_data_update_ticket_status),
                    headers=headers)
                if response_update_checklist.status_code == 200:
                    task.write({'is_ticket_resolved': True})
                else:
                    re = channel_id.message_post(
                        subject="Iris failed request reminder",
                        body="Fail to resolve the ticket#" + str(task.ticket) + " in Iris",
                        message_type='comment',
                        subtype_id=self.env.ref('mail.mt_comment').id
                    )
            except Exception as er:
                _logger.exception("Resolve the task ticket#{0} failed,  Bad request : {1} !".format(str(task.ticket), er))

    def create_ticket_to_iris(self):
        if not self.sale_order_type and not self.x_studio_order_type :
            return
        if not self.partner_id.x_studio_lead_id :
            return
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url') + self.get_portal_url()
        iris_ticket_data = {}
        try:
            if self.sale_order_type == 'new' or self.sale_order_type == 'conversion' or self.sale_order_type == 'add_ons' :
                iris_ticket_data = {
                    "type": 385,
                    "subject": 'ERP New Pos Order',
                    "priority": 0,
                    "group_id": 0,
                    "assignType": "lead",
                    "assignTo": str(self.partner_id.x_studio_lead_id),
                }
                assign_users = []
                if self.x_studio_assign_to:
                    iris_user = odoo_user_to_iris_user.get(str(self.x_studio_assign_to.id), 0)
                    assign_users.append(int(iris_user))
                    iris_ticket_data.update({"description": "The implementer of this order is " + str(self.x_studio_assign_to.name)})

            if self.sale_order_type == 'other' or self.sale_order_type == 'accessories':
                iris_ticket_data = {
                    "type": 386,
                    "subject": 'ERP Accessory/other Order',
                    "priority": 0,
                    "group_id": 0,
                    "assignType": "lead",
                    "assignTo": str(self.partner_id.x_studio_lead_id),
                }

            if self.x_studio_order_type == 'Standalone':
                iris_ticket_data = {
                    "type": 387,
                    "subject": 'ERP Standalone Terminal',
                    "priority": 0,
                    "group_id": 0,
                    "assignType": "lead",
                    "assignTo": str(self.partner_id.x_studio_lead_id),
                }
            if self.x_studio_order_type == 'Other':

                iris_ticket_data = {
                    "type": 386,
                    "subject": 'ERP Accessory/other Order',
                    "priority": 0,
                    "group_id": 0,
                    "assignType": "lead",
                    "assignTo": str(self.partner_id.x_studio_lead_id),
                }
            if self.x_studio_order_type == 'cc_paper':
                iris_ticket_data = {
                    "type": 386,
                    "subject": 'CC Paper',
                    "priority": 0,
                    "group_id": 0,
                    "assignType": "lead",
                    "assignTo": str(self.partner_id.x_studio_lead_id),
                }

            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json'}
            IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
            headers.update({'X-API-KEY': IRIS_API_KEY})
            iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
            if self.x_studio_ticket__1:
                iris_ticket_data_update_comment = {
                    "comment": "The order is confirmed ,  more information of sales order , click the odoo link ",
                }
                response_update_comment = requests.post(iris_ticket_url + "/" + str(self.x_studio_ticket__1) + "/comment",
                                                        data=json.dumps(iris_ticket_data_update_comment),
                                                        headers=headers)
                iris_ticket_data_update_comment = {
                    "comment": base_url,
                }
                response_update_comment = requests.post(iris_ticket_url + "/" + str(self.x_studio_ticket__1) + "/comment",
                                                        data=json.dumps(iris_ticket_data_update_comment),
                                                        headers=headers)
                return
            response = requests.post(iris_ticket_url, data=json.dumps(iris_ticket_data), headers=headers)
            if response.status_code == 200:
                _logger.info("Create ticket response : %s ", json.loads(response.text))
                message = 'Create a ticket to IRIS Lead: ' + str(self.partner_id.x_studio_lead_id)
                self.message_post(body=message)
                ticket_data = json.loads(response.text)
                ticket_id = ticket_data['general']['id']
                self.write({'x_studio_ticket__1': ticket_id})
                # iris_ticket_data_update_ticket_status = {
                #     "status": "in_progress",
                # }
                # response_update_checklist = requests.patch(iris_ticket_url + "/" + str(ticket_id),
                #                                            data=json.dumps(iris_ticket_data_update_ticket_status),
                #                                            headers=headers)
                # self.create_response_history(response_update_checklist, "Update the ticket status to Inprogress in Iris")
                iris_ticket_data_update_comment = {
                    "comment": "For more information of sales order , click the odoo link ",
                }
                response_update_comment = requests.post(iris_ticket_url + "/" + str(ticket_id) + "/comment",
                                                           data=json.dumps(iris_ticket_data_update_comment),
                                                           headers=headers)
                iris_ticket_data_update_comment = {
                    "comment": base_url,
                }
                response_update_comment = requests.post(iris_ticket_url + "/" + str(ticket_id) + "/comment",
                                                        data=json.dumps(iris_ticket_data_update_comment),
                                                        headers=headers)
                # self.create_response_history(response_update_comment, "Add sale order link note the ticket in Iris")
                self.message_post(body="Add sale order link note the ticket in Iris")
        except Exception as e:
            _logger.exception("Creating a ticket failed when a sales order is confirmed : %s", e)

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        if self.x_studio_ticket__1:
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json'}
            IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
            headers.update({'X-API-KEY': IRIS_API_KEY})
            iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
            iris_ticket_data_update_comment = {
                "comment": "The sale order is cancelled in Odoo",
            }
            response_update_comment = requests.post(iris_ticket_url + "/" + str(self.x_studio_ticket__1) + "/comment",
                                                    data=json.dumps(iris_ticket_data_update_comment),
                                                    headers=headers)
            iris_ticket_data_update_ticket_status = {
                "status": "resolved",
            }
            response_update_resolved = requests.patch(
                iris_ticket_url + "/" + str(self.x_studio_ticket__1),
                data=json.dumps(iris_ticket_data_update_ticket_status),
                headers=headers)
            _logger.info("resolve checklist response : %s ", json.loads(response_update_resolved.text))
        return res

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        # Send data to iris
        self.so_to_iris()
        self.create_ticket_to_iris()
        return res

    def fetch_implementer(self):
        domain = [('sale_order_type','in',['new','conversion']),
                  ('create_date', '>=', datetime.date.today() - datetime.timedelta(days=75)),
                  ('create_date', '<=', datetime.date.today() - datetime.timedelta(days=14)),('state','=','sale')]
        orders = self.env['sale.order'].search(domain)
        implementer_list = []
        for order in orders:
            if order.x_studio_assign_to :
                subscription_total = 0
                for item in order.order_line:
                    if 'Subscription' in item.name :
                        subscription_total = subscription_total + item.price_total
                tmp_implementer = {}
                tmp_implementer["name"] = order.partner_id.name
                tmp_implementer["implementer"] = order.x_studio_assign_to.display_name
                tmp_implementer["Saas_fee"] = subscription_total
                implementer_list.append(tmp_implementer)

        sa = gspread.service_account(
            filename=get_module_resource('iris_integration', 'data/', 'totemic-gravity-359218-86911f587b12.json'))
        sh = sa.open("Implementer Data")
        # wks = sh.worksheet("Sheet1")
        length = len(implementer_list)
        wks = sh.add_worksheet(title=datetime.date.today().strftime('%y/%m/%d'),rows=length, cols=5)

        for i in range(length):
            time.sleep(0.1)
            wks.update_cell(i + 1, 1, implementer_list[i]["name"])
            wks.update_cell(i + 1, 2, implementer_list[i]["implementer"])
            wks.update_cell(i + 1, 3, implementer_list[i]["Saas_fee"])

        # ctx = self.env.context.copy()
        # user = self.env.user
        # ctx.update({"implementer_list": implementer_list})
        #
        # mail_template_id = self.env.ref('iris_integration.fetch_implementer_to_ronald').sudo()
        # try:
        #     mail_template_id.with_context(ctx).sudo().send_mail(user.id, force_send=True)
        #     ctx.update({
        #         'email_to': 'lingy@zbspos.com',
        #     })
        #
        # except ValueError:
        #     render_values = {
        #         'success': False,
        #
        #     }
