from odoo import api, fields, models
import base64
from odoo.exceptions import UserError, ValidationError, RedirectWarning
import requests
import json
from odoo.exceptions import ValidationError
import logging
import re

_logger = logging.getLogger(__name__)

US_STATE_DICT = {
'AL': 9,
'AK': 10,
'AZ': 11,
'AR': 12,
'CA': 13,
'CO': 14,
'CT': 15,
'DE': 16,
'DC': 17,
'FL': 18,
'GA': 19,
'HI': 20,
'ID': 21,
'IL': 22,
'IN': 23,
'IA': 24,
'KS': 25,
'KY': 26,
'LA': 27,
'ME': 28,
'MT': 29,
'NE': 30,
'NV': 31,
'NH': 32,
'NJ': 33,
'NM': 34,
'NY': 35,
'NC': 36,
'ND': 37,
'OH': 38,
'OK': 39,
'OR': 40,
'MD': 41,
'MA': 42,
'MI': 43,
'MN': 44,
'MS': 45,
'MO': 46,
'PA': 47,
'RI': 48,
'SC': 49,
'SD': 50,
'TN': 51,
'TX': 52,
'UT': 53,
'VT': 54,
'VA': 55,
'WA': 56,
'WV': 57,
'WI': 58,
'WY': 59,
'FM': 61,
'GU': 62,
'PW': 65,
'PR': 66,
'VI': 67
}


class ProjectTask(models.Model):
	_inherit = 'project.task'

	x_studio_many2one_field_7MRZY = fields.Many2one('sale.order', string='Sales Order')
	is_ticket_resolved = fields.Boolean(string="Is Ticket Resolved")
	x_studio_lead_id = fields.Char(string='Lead ID')
	ticket = fields.Char(string='Ticket ID')
	ticket_link = fields.Char(string='Ticket Link')
	color = fields.Integer('Color', store=True)
	color_priority = fields.Selection([
		('Normal', 'Normal'),
		('Medium', 'Medium'),
		('Rush', 'Rush'),
	], string="Priority",)

	@api.model
	def write(self, vals):
		res = super(ProjectTask, self).write(vals)
		headers = {'Content-Type': 'application/json',
				   'Accept': 'application/json'}
		IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
		headers.update({'X-API-KEY': IRIS_API_KEY})
		iris_ticket_url = "	https://crm.zbspos.com/api/v1/helpdesk"
		try:
			if self.x_studio_many2one_field_LEq7b and self.x_studio_many2one_field_LEq7b.id == 1 and \
					self.partner_id.x_studio_lead_id and vals.get('x_studio_many2one_field_LEq7b', False):
				task_tag = self.env['x_task_tag'].search([('id', '=', self.x_studio_many2one_field_LEq7b.id)])

				iris_ticket_data = {
					"type": int(task_tag.x_studio_ticket_type_id),
					"subject": 'ERP Standalone Terminal',
					"priority": 0,
					"group_id": 0,
					"assignType": "lead",
					"description": re.sub('<[^<]+?>', '\n',
										  "Standalone Terminal" if self.description == '<p><br></p>' else self.description),
					"assignTo": int(self.partner_id.x_studio_lead_id),
				}
				if self.ticket:
					response = requests.patch(iris_ticket_url + '/' + self.ticket, data=json.dumps(iris_ticket_data),
											  headers=headers)
					create_ticket_response = json.loads(response.text)
					if response.status_code == 200:
						_logger.info("==update a ticket when a task is updated,successful response ")
					else:
						_logger.info("==update a ticket when a task is updated,failed response : %s ",
									 json.loads(response.text))
				else:
					response = requests.post(iris_ticket_url, data=json.dumps(iris_ticket_data), headers=headers)
					create_ticket_response = json.loads(response.text)
					if response.status_code == 200:
						ticket_id = create_ticket_response['general']['id']
						self.write({'ticket': ticket_id})
						_logger.info("==create a ticket when a task is create,successful response ")
					else:
						_logger.info("==create a ticket when a task is created,failed response : %s ",
									 json.loads(response.text))
		except Exception as e:
			_logger.exception("==create iris standalone terminal ticket when a task is created, failed request : %s ", e)

		return res

	@api.model
	def create(self, vals):
		res = super(ProjectTask, self).create(vals)
		#File Build Ticket
		try:
			if res.x_studio_many2one_field_LEq7b and res.x_studio_many2one_field_LEq7b.id == 1 \
					and res.partner_id.x_studio_lead_id and vals.get('x_studio_many2one_field_LEq7b', False):

				headers = {'Content-Type': 'application/json',
						   'Accept': 'application/json'}
				IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
				headers.update({'X-API-KEY': IRIS_API_KEY})
				iris_ticket_url = "https://crm.zbspos.com/api/v1/helpdesk"
				task_tag = self.env['x_task_tag'].search([('id', '=', res.x_studio_many2one_field_LEq7b.id)])
				iris_ticket_data = {
					"type": int(task_tag.x_studio_ticket_type_id),
					"subject": 'ERP Standalone Terminal',
					"priority": 0,
					"group_id": 0,
					"assignType": "lead",
					"description": re.sub('<[^<]+?>', '\n', "Standalone Terminal" if res.description == '<p><br></p>' else res.description),
					"assignTo": int(res.partner_id.x_studio_lead_id),
				}
				response = requests.post(iris_ticket_url, data=json.dumps(iris_ticket_data), headers=headers)
				if response.status_code == 200:
					create_ticket_response = json.loads(response.text)
					ticket_id = create_ticket_response['general']['id']
					res.write({'ticket_link':"https://crm.zbspos.com/helpdesk/ticket/" + str(ticket_id),
								'ticket':str(ticket_id)})
				else:
					_logger.info("==Create a ticket when a task is created, failed request : %s ", json.loads(response.text))
		except Exception as e:
				_logger.exception("==Create a ticket when a task is created, failed request : %s ", e)
		return res

	@api.onchange('color_priority')
	def _get_color(self):
		"""Compute Color value according to the conditions"""
		for rec in self:
			if rec.color_priority == "Rush":
				rec.color = 1
			if rec.color_priority == "Normal":
				rec.color = 0
			if rec.color_priority == "Medium":
				rec.color = 3

	@api.onchange('x_studio_lead_id')
	def _onchange_vehicle(self):
		iris_url_lead = "https://zbs.iriscrm.com/api/v1/leads/"
		iris_url_lead = iris_url_lead + str(self.x_studio_lead_id)
		headers = {'Content-Type': 'application/json',
				   'Accept': 'application/json'}
		IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
		headers.update({'X-API-KEY': IRIS_API_KEY})
		response = requests.get(iris_url_lead, headers=headers)
		lead_data = json.loads(response.text)
		if response.status_code == 200:
			business_phone = lead_data['details'][0]['fields'][13]['value']
			owner_name = lead_data['details'][0]['fields'][7]['value']
			Street = lead_data['details'][0]['fields'][9]['value']
			email = lead_data['details'][0]['fields'][17]['value']
			mid = ""
			if lead_data['details'][0]['fields'][2]['value']:
				mid = lead_data['details'][0]['fields'][2]['value']
			dba = lead_data['details'][0]['fields'][0]['value']
			customer = self.env['res.partner'].search(['|', ('phone', '=', business_phone), ('x_studio_lead_id', '=', str(self.x_studio_lead_id))])
			if customer:
				self.partner_id = customer[0]
				customer.write({
								'x_studio_lead_id': str(self.x_studio_lead_id),
								'merchant_id': str(mid)})
			else:
				new_customer = self.env['res.partner'].create({
						'phone': business_phone,
						'mobile': business_phone,
						'street': Street,
						'x_studio_owner_name': owner_name,
						'email': email,
						'name': business_phone + ' - ' + dba,
						'merchant_id': str(mid)
					})
				new_customer.write({'x_studio_lead_id': str(self.x_studio_lead_id)})
				self.partner_id = new_customer

	@api.onchange('x_studio_many2one_field_7MRZY')
	def _onchange_sale_order(self):
		if self.x_studio_many2one_field_7MRZY:
			self.x_studio_many2one_field_7MRZY.write({"standalone_task": self.id.origin})

	def syn_ticket_to_project_from_iris_periodically(self):

		ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
		headers = {'Content-Type': 'application/json',
				   'Accept': 'application/json'}
		IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
		headers.update({'X-API-KEY': IRIS_API_KEY})
		param = {
			'per_page': 10,
			'sort_dir': 'desc',
			'sort_by': 'modified',
            'type': str(390),
			'unassigned': 1
		}
		try:
			response = requests.get(ticket_url, headers=headers, params=param)
			if response.status_code == 200:
				ticket_data = json.loads(response.text)
				for ticket in ticket_data['data']:
					ticket_info_response = requests.get(ticket_url + '/' + str(ticket['id']), headers=headers)
					if ticket_info_response.status_code == 200:
						ticket_info_response_data = json.loads(ticket_info_response.text)
						subject = str(ticket_info_response_data['general']['subject'])
						description = str(ticket_info_response_data['general']['description'])
						description = description.replace('\n', '<br>')
						lead_id = str(ticket_info_response_data['general']['lead_id'])
						ticket_id = str(ticket_info_response_data['general']['id'])
						ticket_type_id = ticket_info_response_data['general']['type']['id']
						task_tag = self.env['x_task_tag'].search([('x_studio_ticket_type_id', '=', ticket_type_id)])
						partner = self.env['res.partner'].search(
							[('x_studio_lead_id', '=', lead_id)])
						partner_id = partner[0].id if partner else False
						task = self.env['project.task'].search([('ticket', '=', ticket_id)])
						if task:
							task.write({
								'name': subject,
								'partner_id': partner_id,
								'description': description,
								'ticket': ticket_id,
								'x_studio_many2one_field_LEq7b': task_tag.id
							})
						else:
							task = self.env['project.task'].create({
								'project_id': 44,
								'name': subject,
								'partner_id': partner_id,
								'description': description,
								'ticket': ticket_id,
								'x_studio_many2one_field_LEq7b': task_tag.id
							})
						for comment_info in ticket_info_response_data['comments']:
							comment_body = comment_info['comment'].replace('#bold_start', '')
							comment_body = comment_body.replace('#bold_end', '')
							comment_body = comment_body.replace('\n', '<br>')
							domain = [('body', '=', comment_body), ('model', '=', 'project.task'),
									  ('message_type', '=', 'comment'), ('res_id', '=', task.id)]
							message = self.env['mail.message'].sudo().search(domain)
							if not message:

								values = {
									'body': comment_body,
									'model': 'project.task',
									'message_type': 'comment',
									'no_auto_thread': False,
									'res_id': task.id,
								}
								message = self.env['mail.message'].sudo().create(values)
						for checklist_info in ticket_info_response_data['checklist']:
							if not checklist_info['completed']:
								task_model_id = self.env['ir.model'].search([('model', '=', 'project.task')], limit=1).id
								domain = [('summary', '=', checklist_info['name']), ('activity_type_id', '=', 4),
										  ('res_model_id', '=', task_model_id), ('res_id', '=', task.id)]
								unchecked_activity = self.env['mail.activity'].sudo().search(domain)
								if not unchecked_activity:
									values = {
										 'summary': checklist_info['name'],
										'activity_type_id': 4,
										'res_model_id': task_model_id,
										'res_id': task.id,
									}
									activity = self.env['mail.activity'].sudo().create(values)
							else:
								task_model_id = self.env['ir.model'].search([('model', '=', 'project.task')], limit=1).id
								domain = [('summary', '=', checklist_info['name']), ('activity_type_id', '=', 4),
										  ('res_model_id', '=', task_model_id), ('res_id', '=', task.id)]
								checked_activity = self.env['mail.activity'].sudo().search(domain)
								checked_activity.unlink()
		except Exception as er:
			_logger.exception("Syn iris tickets to project failed, bad request : %s !", er)
