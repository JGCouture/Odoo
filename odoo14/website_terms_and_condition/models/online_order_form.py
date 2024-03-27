from odoo import api, fields, models


class MerchantForm(models.Model):
    _inherit = 'online.order.form'

    partner = fields.Many2one('res.partner', string="Partner")
    sale_order_id = fields.Many2one('sale.order', string="Sale Order Id")
    bank = fields.Char(string="Bank")