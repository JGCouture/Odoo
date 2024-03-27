# -*- coding: utf-8 -*-
import requests
import json
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import json
import re
from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_semi = fields.Boolean(string="Is Semi")
    is_standalone = fields.Boolean(string="Is Standalone")

class StockPicking(models.Model):
    _inherit = "stock.picking"

    # def write(self, vals):
    #     res = super(StockPicking, self).write(vals)
    #     if vals.get('carrier_tracking_ref'):
    #         if self.sale_id.standalone_task and "OUT" in self.display_name:
    #             message_body = "no tracking number"
    #             if self.carrier_tracking_ref:
    #                 message_body = str(self.carrier_tracking_ref)
    #             type_id = int(self.sale_id.standalone_task.x_studio_many2one_field_LEq7b.x_studio_ticket_type_id)
    #             mid = ""
    #             if self.partner_id.merchant_id:
    #                 mid = self.partner_id.merchant_id
    #             tmp_model_list = []
    #             for move_line in self.move_ids_without_package.move_line_ids:
    #                 if move_line.display_name and move_line.lot_id.display_name:
    #                     tmp_model = "Terminal: {model}, SN: {serial}"
    #                     tmp_model_str = tmp_model.format(model=move_line.display_name, serial=move_line.lot_id.display_name )
    #                     tmp_model_list.append(tmp_model_str)
    #
    #             iris_ticket_data = {
    #                 "type": type_id,
    #                 "subject": ' ; '.join(tmp_model_list),
    #                 "priority": 0,
    #                 "group_id": 0,
    #                 "assignType": "lead",
    #                 "assignTo": str(self.sale_id.standalone_task.x_studio_lead_id),
    #                 "description": re.sub('<[^<]+?>', '', self.sale_id.standalone_task.description)
    #
    #             }
    #             headers = {'Content-Type': 'application/json',
    #                        'Accept': 'application/json'}
    #             IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
    #             headers.update({'X-API-KEY': IRIS_API_KEY})
    #             iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
    #             response = requests.post(iris_ticket_url, data=json.dumps(iris_ticket_data), headers=headers)
    #             if response.status_code == 200:
    #                 _logger.info("create ticket response : %s ", json.loads(response.text))
    #                 message = 'create a ticket to IRIS Lead: ' + str(self.sale_id.standalone_task.x_studio_lead_id)
    #                 self.message_post(body=message)
    #                 ticket_data = json.loads(response.text)
    #                 ticket_id = ticket_data['general']['id']
    #                 self.sale_id.write({'x_studio_ticket__1': ticket_id})
    #                 updated_checklist = []
    #                 for check in ticket_data['checklist']:
    #                     tmp_dict = {'index': check['index'],
    #                                 'completed': True,
    #                                 'comment': 'done'}
    #                     if check['name'] == 'Deployment Tracking':
    #                         tmp_dict.update({'comment': message_body})
    #                     updated_checklist.append(tmp_dict)
    #                 iris_ticket_data = {
    #                     "status": "resolved",
    #                     "checklist": updated_checklist
    #                 }
    #                 response_update_checklist = requests.patch(iris_ticket_url + "/" + str(ticket_id),
    #                                                            data=json.dumps(iris_ticket_data),
    #                                                            headers=headers)
    #                 _logger.info("resolve checklist response : %s ", json.loads(response_update_checklist.text))
    #     return res

    def create_response_history(self, response, message):
        history_obj = self.env['iris.integration.history']
        history_obj.create({
                            'user_id': self.env.user.id,
                            'note': 'Sent the Contact to IRIS',
                            'response': response})
        self.message_post(body=message)

    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
        headers.update({'X-API-KEY': IRIS_API_KEY})
        iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
        if vals.get('carrier_tracking_ref', False) and "OUT" in self.display_name and self.sale_id.x_studio_ticket__1:
            tracking_message_body = "No tracking number"
            if self.carrier_tracking_ref:
                tracking_message_body = "Tracking number: " + str(self.carrier_tracking_ref)
            tmp_model_list = []
            tmp_model_list.append(tracking_message_body)
            iris_ticket_data_update_comment = {
                "comment": '\n'.join(tmp_model_list),
            }
            try:
                response_update_comment = requests.post(
                    iris_ticket_url + "/" + str(self.sale_id.x_studio_ticket__1) + "/comment",
                    data=json.dumps(iris_ticket_data_update_comment),
                    headers=headers)
                self.create_response_history(response_update_comment, "Add tracking number comment to the ticket in Iris")
                _logger.info("Add tracking number comment response : %s ", json.loads(response_update_comment.text))
            except Exception as er:
                _logger.exception("Tracking number of the sale order to iris synchronization failed,  Bad request : %s !",
                                  er)
        if vals.get('date_done', False) and self.state == 'done' :
            if "OUT" in self.display_name and self.sale_id.x_studio_ticket__1:
                tmp_model_list = []
                # if self.sale_id.x_studio_order_type:
                for move_line in self.move_ids_without_package.move_line_ids:
                    if move_line.display_name :
                        tmp_model = "Equipment: {model}, SN: {serial}"
                        serial_number = move_line.lot_id.display_name if move_line.lot_id else "None"
                        tmp_model_str = tmp_model.format(model=move_line.display_name, serial=serial_number)
                        tmp_model_list.append(tmp_model_str)
                # else:
                #     for move_line in self.move_ids_without_package.move_line_ids:
                #         if move_line.display_name and move_line.lot_id.display_name and move_line.product_id.product_tmpl_id.is_semi:
                #             tmp_model = "Terminal: {model}, SN: {serial}"
                #             tmp_model_str = tmp_model.format(model=move_line.display_name, serial=move_line.lot_id.display_name )
                #             tmp_model_list.append(tmp_model_str)
                iris_ticket_data_update_comment = {
                    "comment": '\n'.join(tmp_model_list),
                }
                try:
                    response_update_comment = requests.post(iris_ticket_url + "/" + str(self.sale_id.x_studio_ticket__1) + "/comment",
                                                            data=json.dumps(iris_ticket_data_update_comment),
                                                            headers=headers)
                    self.create_response_history(response_update_comment, "Add Serial Number comment to the ticket in Iris")
                    _logger.info("resolve checklist response : %s ", json.loads(response_update_comment.text))
                    if self.sale_id.standalone_task and self.sale_id.standalone_task.description:
                        # iris_ticket_data_update_ticket_status = {
                        #     "description": self.sale_id.standalone_task.description
                        # }
                        iris_ticket_data_update_ticket_status = {
                            "description": re.sub('<[^<]+?>', '\n', self.sale_id.standalone_task.description)
                        }
                        response_update_checklist = requests.patch(iris_ticket_url + "/" + str(self.sale_id.x_studio_ticket__1),
                                                                   data=json.dumps(iris_ticket_data_update_ticket_status),
                                                                   headers=headers)
                        _logger.info("update ticket description response : %s ", json.loads(response_update_checklist.text))
                    iris_ticket_data_update_ticket_status = {
                        "status": "resolved",
                    }
                    response_update_resolved = requests.patch(
                        iris_ticket_url + "/" + str(self.sale_id.x_studio_ticket__1),
                        data=json.dumps(iris_ticket_data_update_ticket_status),
                        headers=headers)
                    _logger.info("resolve checklist response : %s ", json.loads(response_update_resolved.text))
                except Exception as er:
                    _logger.exception("Serial number of the sale order to iris synchronization failed,  Bad request : %s !", er)
                # else:
                #     iris_ticket_data_update_ticket_status = {
                #         "status": "resolved",
                #     }
                #     response_update_checklist = requests.patch(
                #         iris_ticket_url + "/" + str(self.sale_id.x_studio_ticket__1),
                #         data=json.dumps(iris_ticket_data_update_ticket_status),
                #         headers=headers)
                #     _logger.info("resolve checklist response : %s ", json.loads(response_update_checklist.text))
        return res