from odoo import api, fields, models
import base64


class MerchantForm(models.Model):
    _name = 'online.order.form'
    _inherit = ['mail.thread']
    _description = 'Online Order Form'
    _order = 'id desc'

    pos_system = fields.Selection([
        ('1', 'KwickPOS (No Deposit)'),
        ('2', 'New (No Deposit)'),
        ('3', 'Other (No Deposit)'),
        ('4', 'KwickPOS (VS)'),
        ('5', 'Aldelo ($300 Deposit Required)'),
        ('6', 'GDC ($300 Deposit Required)'),
        ('7', 'MCPOS ($300 Deposit Required)'),
        ('8', 'MenuSifu ($300 Deposit Required)'),
        ('9', 'Other ($300 Deposit Required)'),

    ], string="POS System", tracking=True)
    customer_id = fields.Char(String="Customer Id", tracking=True)
    need_website = fields.Selection([
        ('1', 'No, link online order page to my website.'),
        ('2', 'No, I only need online order page as website.'),
        ('3', 'Yes, I need a website and online order page.'),
    ], string="Do you need website", tracking=True)
    website_address = fields.Char(String="Website Address", tracking=True)
    wechat = fields.Char(String="Wechat", tracking=True)
    lunch_hours = fields.Char(String="Restaurant Hours / Lunch Hours", tracking=True)
    sales_tax = fields.Char(String="Sales Tax", tracking=True)
    need_chinese = fields.Selection([
        ('1', 'Yes'),
        ('2', 'No'),
    ], string="Menu Need Chinese?", tracking=True)
    language = fields.Char(String="Language", tracking=True)
    service_type = fields.Selection([
        ('1', 'Pickup Only'),
        ('2', 'Delivery Only'),
        ('3', 'Pickup and Delivery'),

    ], string="Service Type", tracking=True)
    # plan_choice = fields.Char(String="Plan Choice")
    plan_choice = fields.Selection([
        ('1', 'Promo Special / $1.00 Per Order (Customer Pays)'),
        ('2', 'Free Plan / $1.50 Per Order (Customer Pays)'),
        ('3', '$159/Month (Unlimited Orders)'),
        ('4', '5% Per Order'),

    ], string="Plan Choice", tracking=True)
    backup_phone = fields.Char(String="Text Message Order Notification (For Backup)", tracking=True)
    delivery_zone = fields.Char(String="Delivery Zone", tracking=True)
    delivery_fee = fields.Char(String="Delivery Fee", tracking=True)
    minimum_order_amount = fields.Char(String="Minimum Order Amount", tracking=True)
    free_delivering_minimum_amount = fields.Char(String="Free Delivering Minimum Amount", tracking=True)
    # payment_option = fields.Char(String="Payment Option")
    payment_option = fields.Selection([
        ('1', 'In Store + Online Payment'),
        ('2', 'Online Payment Only'),
        ('3', 'In-store Payment Only'),

    ], string="Payment Option", tracking=True)
    # if_cash_discount = fields.Char(String="Enroll in Cash Discount?")
    if_cash_discount = fields.Selection([
        ('1', 'Yes, customers will pay a surcharge fee for online credit card transactions'),
        ('2', 'No, customers will pay NO additional surcharge for online credit card transactions'),
    ], string="Enroll in Cash Discount?", tracking=True)
    account_number = fields.Char(String="Account No.", tracking=True)
    routing_number = fields.Char(String="Routing No.", tracking=True)
    note = fields.Char(String="Note", tracking=True)
    agent_email = fields.Char(String="Agent Email", tracking=True)
    date = fields.Date(string="date", tracking=True)
    company_name = fields.Char(String="Legal Name of Business", tracking=True)
    dba = fields.Char(String="Doing Business As", tracking=True)
    company_address = fields.Char(String="Business Address", tracking=True)
    city = fields.Char(String="City", tracking=True)
    state = fields.Char(String="State", tracking=True)
    zip_code = fields.Char(String="Zip Code", tracking=True)
    business_phone_number = fields.Char(String="Business Phone Number", tracking=True)
    email = fields.Char(String="Email", tracking=True)
    tax_id = fields.Char(String="Federal Tax ID", tracking=True)

    owner_name = fields.Char(String="Owner Name", tracking=True)
    cell_phone_number = fields.Char(String="Cell Phone Number", tracking=True)

    ssn = fields.Char(String="SSN", tracking=True)

    agent_name = fields.Char(string="Agent Name", tracking=True)

    client_initials = fields.Binary(string="Client Initials", tracking=True)
    # client_business_legal_name = fields.Char(string="Print Client's Business Legal Name")
    personal_guarantee_signature = fields.Binary(string="Personal Guarantee Signature", tracking=True)
    personal_guarantee_signature_date = fields.Date(string="Personal Guarantee Sign Date", tracking=True)
    pricing_confirmation_signature = fields.Binary(string="pricing confirmation signature", tracking=True)

    from_application_signature = fields.Binary(string="From Application (Signature)", tracking=True)
    from_application_signature_date = fields.Date(string="From Application Sign Date", tracking=True)

    print_client_business_legal_name = fields.Char(string="Print Client's Business Legal Name", tracking=True)

    client_business_principle_signature = fields.Binary(string="Client's Business Principle Signature", tracking=True)
    print_name_of_signer = fields.Char(string="Print Name of Signer", tracking=True)
    client_business_principle_title = fields.Char(string="Client's Business Principle Title", tracking=True)
    client_business_principle_sign_date = fields.Date(string="Client's Business Principle Sign Date", tracking=True)
    signature = fields.Binary(string="Signature", tracking=True)

    menu = fields.Binary(string="Menu")
    owner_id = fields.Binary(string="Owner ID")
    irs_document = fields.Binary(string="IRS Document")
    void_check = fields.Binary(string="Void Check")
    #flag
    if_shared_form = fields.Boolean(default=False)

