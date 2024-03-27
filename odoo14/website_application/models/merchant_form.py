from odoo import api, fields, models
import base64


class MerchantForm(models.Model):
    _name = 'merchant.form'
    _inherit = ['mail.thread']
    _description = 'Merchant Form'
    _order = 'id desc'

    account_type = fields.Selection([
        ('1', 'New Account'),
        ('2', 'Change Owner'),
        ('3', 'Change Legal Info')
    ], string="Account Type", tracking=True)
    old_mid = fields.Char(string="Old MID", tracking=True)
    is_add_paper_plan = fields.Selection([
        ('1', 'Yes'),
        ('2', 'No')
    ], string="Add Paper Plan ($14.95 / Month)", tracking=True)
    checkbook = fields.Char(string="Checkbooks", tracking=True)
    tips_trays = fields.Char(string="Tips Trays", tracking=True)
    no_supply_order_needed = fields.Char(string="No Supply Order Needed", tracking=True)
    standalone_or_semi = fields.Selection([
        ('1', 'Yes'),
        ('2', 'No')
    ], string="Standalone OR Semi-Integration ", tracking=True)
    equipment_type = fields.Char(string="Specify your equipment type", tracking=True)
    equipment = fields.Selection([
        ('1', 'PAX S80'),
        ('2', 'PAX S300'),
        ('3', 'PAX S500'),
        ('4', 'FD 50'),
        ('5', 'Clover'),
        ('6', 'Other')
    ], string="Equipment", tracking=True)
    bill_to = fields.Selection([
        ('1', 'Agent'),
        ('2', 'Merchant')
    ], string="Bill to?", tracking=True)
    equipment_quantity = fields.Char(string="Equipment Quantity", tracking=True)

    feature_restaurant = fields.Char(string="Restaurant", tracking=True)
    feature_retail = fields.Char(string="Retail", tracking=True)
    feature_with_tips = fields.Char(string="With tips", tracking=True)
    feature_dial = fields.Char(string="Dial", tracking=True)
    feature_pin_debit = fields.Char(string="Pin-Debit", tracking=True)
    feature_server_id = fields.Char(string="Service ID", tracking=True)
    feature_ip = fields.Char(string="IP", tracking=True)
    feature_auto_time_batch = fields.Char(string="Auto Batch", tracking=True)
    feature_tip_suggestions = fields.Char(string="Tip Suggestions", tracking=True)
    feature_other_feature = fields.Char(string="Other", tracking=True)
    feature_ip_input = fields.Char(string="IP Address", tracking=True)
    feature_auto_batch_time_input = fields.Char(string="Auto Batch Time", tracking=True)
    feature_tip_suggestions_input = fields.Char(string="Tip Suggestions", tracking=True)
    feature_other_feature_input = fields.Char(string="Other Feature", tracking=True)
    deployment_method = fields.Selection([
        ('1', 'Agent Pickup'),
        ('2', 'Call Merchant Pickup'),
        ('3', 'POS Team Install'),
        ('4', 'Ship To DBA Address'),
        ('5', 'Ship To Other Address'),
        ('6', 'Re-Programming')
    ], string="Deployment Method", tracking=True)
    is_ship_with_pos = fields.Selection([
        ('1', 'Yes'),
        ('2', 'No')
    ], string="Ship with pos", tracking=True)
    ship_out_address = fields.Char(string="Ship out address", tracking=True)
    ship_out_city = fields.Char(string="Ship out city", tracking=True)
    ship_out_state = fields.Char(string="Ship out state", tracking=True)
    ship_out_zip = fields.Char(stirng="Ship out zip code", tracking=True)
    reprogram_old_mid = fields.Char(string="Reprogram Old mid", tracking=True)
    pricing_type = fields.Selection([
        ('1', 'Interchange'),
        ('2', 'Flat Rate'),
        ('3', 'Cash Discount (by Percentage %)'),
        ('4', 'Cash Discount (by Flat Fee $))')
    ], string="Pricing Type", tracking=True)
    visa_sales_discount_fee = fields.Char(string="VISA/MC/DISCOVER Sales Discount Fee", tracking=True)
    visa_auth_fee = fields.Char(string="VISA/MC/DISCOVER Auth Fee", tracking=True)
    amex_sales_discount_fee = fields.Char(string="AMEX Sales Discount Fee", tracking=True)
    amex_auth_fee = fields.Char(string="AMEX Auth Fee", tracking=True)
    cash_discount_rate = fields.Char(string="Cash Discount Rate", tracking=True)
    other_comment = fields.Char(string="Other Comment", tracking=True)
    if_want_free_cash_discount = fields.Selection([
        ('1', 'Yes'),
        ('2', 'No')
    ], string="Do you want Free Cash Discount Pricing List/Menu (For Massage ONLY)?", tracking=True)
    monthly_fee = fields.Char(string="Monthly Fee", tracking=True)
    other_comment = fields.Char(string="Other Comment", tracking=True)
    date = fields.Date(string="Date", tracking=True)

    sign_date = fields.Date(string="sign date", tracking=True)
    personal_guarantee_sign_date = fields.Date(string="personal guarantee sign date", tracking=True)
    print_client_business_legal_name = fields.Char(string="print client business legal name", tracking=True)
    print_name_signer = fields.Char(string="print name signer", tracking=True)
    business_principle_title = fields.Char(string="business principle title", tracking=True)
    business_principle_sign_date = fields.Date(string="business principle sign date", tracking=True)

    #business information
    agent_name = fields.Char(string="Your Sales Agent", tracking=True)
    agent_email = fields.Char(string="Agent Email", tracking=True)
    name_of_company = fields.Char(string="Legal Name of Business", tracking=True)
    dba = fields.Char(string="Doing Business As", tracking=True)
    address = fields.Char(string="Address", tracking=True)
    city = fields.Char(string="City", tracking=True)
    state = fields.Char(string="State", tracking=True)
    zip_code = fields.Char(string="Zip Code", tracking=True)
    business_phone_number = fields.Char(string="Business Phone Number", tracking=True)
    fax_number = fields.Char(string="Fax Number", tracking=True)
    federal_tax_id = fields.Char(string="Federal Tax ID", tracking=True)
    type_of_business = fields.Char(string="Type of Business", tracking=True)
    company_type = fields.Selection([
        ('1', 'Sole Proprietorship (独资)'),
        ('2', 'Private Corp. (公司)'),
        ('3', 'Limited Liability Co. (公司)'),
        ('4', 'Partnership (合伙)')
    ], string="Company Type", tracking=True)
    open_date = fields.Date(string="Business Open Date", tracking=True)
    estimated_monthly_sale_volume = fields.Char(string="Estimated Monthly Sale Volume", tracking=True)
    average_sales_account = fields.Char(string="Average Sales Amount", tracking=True)
    amex = fields.Selection([
        ('1', 'Yes'),
        ('2', 'No')
    ], string="Amex", tracking=True)
    owner_name = fields.Char(string="Owner's Name ", tracking=True)
    owner_email = fields.Char(string="Email", tracking=True)
    owner_title = fields.Char(string="Tittle", tracking=True)
    owner_phone_number = fields.Char(string="Cell Phone Number", tracking=True)
    owner_home_address = fields.Char(string="Home Address", tracking=True)
    owner_home_city = fields.Char(string="Home City", tracking=True)
    owner_home_state = fields.Char(string="Home State", tracking=True)
    owner_home_zip_code = fields.Char(string="Home Zip", tracking=True)
    ssn = fields.Char(string="Social Security Number", tracking=True)
    owner_date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    owner_driver_license_number = fields.Char(string="Driver License Number", tracking=True)
    owner_state_issued = fields.Char(string="State Issued", tracking=True)
    owner_bank_name = fields.Char(string="Bank Name", tracking=True)
    owner_bank_routing = fields.Char(string="Bank Routing", tracking=True)
    owner_bank_account = fields.Char(string="Bank Account", tracking=True)
    #attachment
    menu_document = fields.Binary(string="Menu/Price List Upload", tracking=True)
    void_check_document = fields.Binary(string="Voided Check", tracking=True)
    irs_document = fields.Binary(string="IRS Document", tracking=True)
    owner_id_document = fields.Binary(string="Owner's ID ", tracking=True)
    other_document = fields.Binary(string="Other Document", tracking=True)
    #signature
    signature = fields.Binary(string="Signature", tracking=True)
    personal_guarantee_signature = fields.Binary(string="Personal Guarantee Signature", tracking=True)
    client_initials_signature = fields.Binary(string="Client Initials", tracking=True)
    client_business_principle_signature = fields.Binary(string="Client's Business Principle Sign Date", tracking=True)
    #flag
    if_hidden_for_merchant = fields.Boolean(string="if hidden for merchant", default=False, tracking=True)
    completely_fill = fields.Boolean(default=False, tracking=True)
    verify_information = fields.Boolean(default=False, tracking=True)
    if_shared_form = fields.Boolean(default=False, tracking=True)