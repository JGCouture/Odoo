# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import json
import re
import base64
import datetime
import logging
_logger = logging.getLogger(__name__)


class Message(models.Model):
    _inherit = 'mail.message'

    def write(self, vals):
        res = super(Message, self).write(vals)
        task = None
        try:
            if self.subtype_id.id == 3:
                if self.model == 'project.task':
                    task = self.env[self.model].search([('id', '=', self.res_id)])
                    if task and task.ticket:
                        iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
                        headers = {"Content-Type": "application/json",
                                   'Accept': 'application/json'}
                        IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
                        headers.update({'X-API-KEY': IRIS_API_KEY})
                        ticket_info_response = requests.get(iris_ticket_url + '/' + str(task.ticket), headers=headers)
                        if ticket_info_response.status_code == 200:
                            ticket_info_response_data = json.loads(ticket_info_response.text)
                            updated_checklist = []
                            for check in ticket_info_response_data['checklist']:
                                if check['name'] in self.body:
                                    mail_body = re.sub('<[^<]+?>', '\n', self.body)
                                    index = mail_body.find("Original note:")
                                    checklist_note = mail_body[index+14:]
                                    tmp_dict = {'index': check['index'],
                                                'completed': True,
                                                'comment': checklist_note}

                                    updated_checklist.append(tmp_dict)
                            iris_ticket_data = {
                                "checklist": updated_checklist
                            }
                            response_update_checklist = requests.patch(iris_ticket_url + "/" + str(task.ticket),
                                                                       data=json.dumps(iris_ticket_data),
                                                                       headers=headers)
                        else:
                            _logger.exception("Editing activity iris synchronization failed")
                if self.model == 'sale.order':
                    order = self.env[self.model].search([('id', '=', self.res_id)])
                    if order and order.x_studio_ticket__1:
                        iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
                        headers = {"Content-Type": "application/json",
                                   'Accept': 'application/json'}
                        IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
                        headers.update({'X-API-KEY': IRIS_API_KEY})
                        ticket_info_response = requests.get(iris_ticket_url + '/' + str(order.x_studio_ticket__1), headers=headers)
                        if ticket_info_response.status_code == 200:
                            ticket_info_response_data = json.loads(ticket_info_response.text)
                            updated_checklist = []
                            for check in ticket_info_response_data['checklist']:
                                if check['name'] in self.body:
                                    mail_body = re.sub('<[^<]+?>', '\n', self.body)
                                    index = mail_body.find("Original note:")
                                    checklist_note = mail_body[index + 14:]
                                    tmp_dict = {'index': check['index'],
                                                'completed': True,
                                                'comment': checklist_note}

                                    updated_checklist.append(tmp_dict)
                            iris_ticket_data = {
                                "checklist": updated_checklist
                            }
                            response_update_checklist = requests.patch(iris_ticket_url + "/" + str(order.x_studio_ticket__1),
                                                                       data=json.dumps(iris_ticket_data),
                                                                       headers=headers)
                        else:
                            _logger.exception("Editing activity iris synchronization failed")
        except Exception as er:
            _logger.exception("Editing activity iris synchronization failed,  Bad request : %s !", er)

        return res


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def _action_done(self, feedback=False, attachment_ids=False):
        # attachments = self.env['ir.attachment'].search([
        #     ('res_model', '=', self._name),
        #     ('res_id', '=', self.id),
        # ])
        if self.res_id:
            order = None
            task = None
            # activities = self.env['mail.activity'].search([('res_id', '=', self.res_id), ('res_model_id', '=', 466)])
            # model = self.env['ir.model'].search([('id', '=', self.res_model_id)])
            iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
            headers = {"Content-Type" : "application/json",
                       'Accept': 'application/json'}
            IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
            headers.update({'X-API-KEY': IRIS_API_KEY})
            try:
                if self.res_model_id.model == "project.task" :
                    task = self.env[self.res_model_id.model].search([('id', '=', self.res_id)])
                    order = task.x_studio_many2one_field_7MRZY
                    ticket_info_response = requests.get(iris_ticket_url + '/' + str(task.ticket), headers=headers)
                    if ticket_info_response.status_code == 200:
                        ticket_info_response_data = json.loads(ticket_info_response.text)
                        updated_checklist = []
                        for check in ticket_info_response_data['checklist']:
                            if self.display_name == check['name']:
                                tmp_dict = {'index': check['index'],
                                            'completed': True,
                                            'comment': re.sub('<[^<]+?>', '\n', self.note)}
                                updated_checklist.append(tmp_dict)
                        iris_ticket_data = {
                            "checklist": updated_checklist
                        }
                        response_update_checklist = requests.patch(iris_ticket_url+"/"+str(task.ticket), data=json.dumps(iris_ticket_data),
                                                  headers=headers)
                        _logger.info("resolve checklist response : %s ", json.loads(response_update_checklist.text))

                if self.res_model_id.model == "sale.order":
                    order = self.env[self.res_model_id.model].search([('id', '=', self.res_id)])
                    ticket_info_response = requests.get(iris_ticket_url + '/' + str(order.x_studio_ticket__1), headers=headers)
                    if ticket_info_response.status_code == 200:
                        ticket_info_response_data = json.loads(ticket_info_response.text)
                        updated_checklist = []
                        for check in ticket_info_response_data['checklist']:
                            if self.display_name == check['name']:
                                note = "Done"
                                if self.note != "<p><br></p>" and  self.note != False:
                                    note = self.note
                                tmp_dict = {'index': check['index'],
                                            'completed': True,
                                            'comment': re.sub('<[^<]+?>', '\n', note)}
                                updated_checklist.append(tmp_dict)
                        iris_ticket_data = {
                            "checklist": updated_checklist
                        }
                        response_update_checklist = requests.patch(iris_ticket_url + "/" + str(order.x_studio_ticket__1),
                                                                   data=json.dumps(iris_ticket_data),
                                                                   headers=headers)
                        _logger.info("resolve checklist response : %s ", json.loads(response_update_checklist.text))
                    # iris_ticket_data_update_comment = {
                    #     "comment": self.display_name + " is done : " + re.sub('<[^<]+?>', '\n', self.note),
                    # }
                    # response_update_comment = requests.post(iris_ticket_url + "/" + str(order.x_studio_ticket__1) + "/comment",
                    #                                         data=json.dumps(iris_ticket_data_update_comment),
                    #                                         headers=headers)
                    # _logger.info("resolve checklist response : %s ", json.loads(response_update_comment.text))
            except Exception as er:
                _logger.exception("Mark down the activities iris synchronization failed,  Bad request : %s !", er)

        return super(MailActivity, self)._action_done(feedback=feedback, attachment_ids=attachment_ids)





