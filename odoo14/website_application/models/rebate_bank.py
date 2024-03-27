from odoo import api, fields, models
import base64


class RebateBank(models.Model):
	_name = 'rebate.bank'
	_description = 'Rebate Bank'

	sales_name = fields.Char(string='Sales Name')
	sales_email = fields.Char(string='Sales Email')
	store_name = fields.Char(string='store name')
	store_phone = fields.Char(string='store phone')
	store_address = fields.Char(string='store address')
	store_city = fields.Char(string='store city')
	store_zip = fields.Char(string='store zip')
	country = fields.Char(string='country ')
	state = fields.Char(string='state ')
	owner_name = fields.Char(string='owner name')
	owner_phone = fields.Char(string='owner phone')
	owner_email = fields.Char(string='owner email')
	purchase_date = fields.Char(string='purchase date')
	bank_name = fields.Char(string='bank name')
	bank_routing = fields.Char(string='routing')
	bank_account = fields.Char(string='account')


	# def action_get_attachment(self, res):
	# 	pdf = self.sudo().env.ref('website_terms_and_condition.action_report_ordering')._render_qweb_pdf(res.ids)[0]
	# 	b64_pdf = base64.b64encode(pdf)
	# 	name = 'onlineordering'+str(res.id)
	# 	attachment = self.env['ir.attachment'].sudo().create({
	# 		'name': name,
	# 		'type': 'binary',
	# 		'datas': b64_pdf,
	# 		'name': name + '.pdf',
	# 		'res_model': res.sudo().sale_order_id._name,
	# 		'res_id': res.sudo().sale_order_id.id,
	# 		'mimetype': 'application/x-pdf'
	# 	})
	# 	template_id = res.sudo().sale_order_id._find_mail_template()
	# 	mail_template_id = self.env['mail.template'].sudo().browse(template_id)
	# 	mail_template_id.sudo().attachment_ids = [(6, 0, [attachment.id])]
	# 	# res.sale_order_id.sale_order_template_id.mail_template_id.attachment_ids = [(6, 0, [attachment.id])]
	# 	return True