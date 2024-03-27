from odoo import api, fields, models
import base64


class OnlineOrder(models.Model):
	_name = 'online.order'
	_description = 'Online Ordering'
	_rec_name = 'partner_id'
	_order = 'id desc'

	# name = fields.Char('POS System Type', required=True)
	sequence = fields.Integer(string='Sequence', default=10)
	partner_id = fields.Many2one('res.partner', string='Customer')
	name_address = fields.Html(string="Name & Address")
	contact_details = fields.Html(string="Contact_details")
	bank_details = fields.Html(string="USt.ID &  Banking Data")
	need_website = fields.Selection([
		('no', 'NO, Link online order page to my website.'),
		('no1', 'No, I only need online order page as website.'),
		('no3', 'Yes, I want a brand new website (additional fee applies).')
	], string='Do you need a website?')
	website_address = fields.Char(string='address')
	menu_other = fields.Char(string="Need Menu in Other Lang")
	# website_option = fields.Selection([
	# 	('free', 'Free Website (Basic Functions)'),
	# 	('paid', 'Paid, Website (More Functionalities)')], string='Website Options')
	# preferred_website1 = fields.Char(string='Preferred Website 1')
	# preferred_website2 = fields.Char(string='Preferred Website 2')
	# preferred_website3 = fields.Char(string='Preferred Website 3')
	monday = fields.Char(string='Monday')
	tuesday = fields.Char(string='Tuesday')
	wednesday = fields.Char(string='Wednesday')
	thursday = fields.Char(string='Thursday')
	friday = fields.Char(string='Friday')
	saturday = fields.Char(string='Saturday')
	sunday = fields.Char(string='Sunday')

	monday_shift2 = fields.Char(string='Monday')
	tuesday_shift2 = fields.Char(string='Tuesday')
	wednesday_shift2 = fields.Char(string='Wednesday')
	thursday_shift2 = fields.Char(string='Thursday')
	friday_shift2 = fields.Char(string='Friday')
	saturday_shift2 = fields.Char(string='Saturday')
	sunday_shift2 = fields.Char(string='Sunday')

	sale_tax = fields.Char(string='Sale Tax')
	need_chinese = fields.Selection([
		('yes', 'Yes'),
		('no', 'No'),
		('other', 'Other')], string='Menu Need Chinese')
	service_type = fields.Char(string='Service Type')
	plan_choice = fields.Selection([
		('promo', 'Promo SPecial / $1.00 Per Order(Customer Pays)'),
		('free', 'Free Plan / $1.50 Per Order (Customer Pays)'),
		('fix', '5% Per Order'),
		('monthly', '$159/Month')], string='Plan Choice')
	# order_notification = fields.Char(string='Order Notification')
	delivery_zone = fields.Text(string='Delivery Zone')
	delivery_free = fields.Float(string='Delivery Free')
	free_delivery_min_amount = fields.Float(string='Free Delivery Minimum Amount')
	min_order_amount = fields.Float(string='Minimum Order Amount')
	payment_option = fields.Selection([
		('in_store', 'In Store Only'),
		('online', 'Online Payment Only'),
		('instore_online', 'In Store + Online Payment')], string='Payment Options')
	sale_order_id = fields.Many2one('sale.order', string='Sale Order')
	active = fields.Boolean(string="Active", default=False)
	order_notification = fields.Selection([
		('email', 'Email'),
		('text', 'Text Message')
	], string="Order Backup Notification Method")
	email_address = fields.Char(string="Email Address")
	backup_phone_number = fields.Char(string="Backup Phone Number")
	do_delivery = fields.Selection([
		('yes', 'Yes'),
		('no', 'No')
	], string="Do you do delivery?")
	delivery_distance = fields.Char(string="Delivery Maximum Distance in miles")
	pickup_order_time= fields.Integer(string="Pickup order food preparation time(min)")
	delivery_order_time = fields.Integer(string="Delivery order food preparation time(if available)")
	use_google_business = fields.Selection([
		('yes','Yes, I already own Google My Business'),
		('no', 'No, I have not used Google My Business')
	], string="Do you use Google My Business for your restaurant?")
	notes = fields.Text(string="Notes")

	@api.model
	def create(self, vals):
		res = super(OnlineOrder, self).create(vals)
		self.action_get_attachment(res)
		return res


	def action_get_attachment(self, res):
		pdf = self.sudo().env.ref('website_terms_and_condition.action_report_ordering')._render_qweb_pdf(res.ids)[0]
		b64_pdf = base64.b64encode(pdf)
		name = 'onlineordering'+str(res.id)
		attachment =  self.env['ir.attachment'].sudo().create({
			'name': name,
			'type': 'binary',
			'datas': b64_pdf,
			'name': name + '.pdf',
			'res_model': res.sudo().sale_order_id._name,
			'res_id': res.sudo().sale_order_id.id,
			'mimetype': 'application/x-pdf'
		})
		template_id = res.sudo().sale_order_id._find_mail_template()
		mail_template_id = self.env['mail.template'].sudo().browse(template_id)
		mail_template_id.sudo().attachment_ids = [(6, 0, [attachment.id])]
		# res.sale_order_id.sale_order_template_id.mail_template_id.attachment_ids = [(6, 0, [attachment.id])]
		return True