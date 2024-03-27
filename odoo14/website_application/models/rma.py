# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import logging

_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class RmaRma(models.Model):
    _inherit = 'rma.rma'

    ticket = fields.Char("Ticket Id")
    ticket_iris_link = fields.Char(string='Iris Ticket Link', compute='compute_iris_link_using_ticket_id')

    @api.depends('ticket')
    def compute_iris_link_using_ticket_id(self):
        for obj in self:
            if obj.ticket:
                obj.ticket_iris_link = 'https://crm.zbspos.com/helpdesk/ticket/' + str(obj.ticket)
            else:
                obj.ticket_iris_link = False

class RmaForm(models.Model):
    _name = "rma.form"
    _inherit = ['mail.thread']
    _description = "for customer to file a rma application"

    sequence = fields.Char('RMA Application Reference', require=True, index=True, copy=False, default='New')
    service_type = fields.Selection([
        ('1', 'RMA Warranty Request (Approval needed)'),
        ('2', 'Repair (Non Warranty Repair - Fee Applys)'),
    ], string='Service Type', tracking=True)
    dba = fields.Char("Business Name", required=True, tracking=True)
    email = fields.Char("Email", tracking=True)
    lead_id = fields.Char(string="Lead Id", tracking=True)
    contact_name = fields.Char(string="Contact Name", tracking=True)
    contact_phone = fields.Char(string="Contact Phone", tracking=True)
    restaurant_address = fields.Char(string="Restaurant Address", tracking=True)
    restaurant_city = fields.Char(string="City", tracking=True)
    restaurant_zipcode = fields.Char(string="Zip Code", tracking=True)
    country_id = fields.Char(string="Country", tracking=True)
    state_id = fields.Char(string="State", tracking=True)
    model_number = fields.Char(string="Model Number", tracking=True)
    serial_number = fields.Char(string="Serial Number", tracking=True)
    date_of_purchase = fields.Datetime(string='Date of Purchase', tracking=True)
    detailed_fault_description = fields.Char(string="Detailed Fault Description", tracking=True)
    picture_of_faulty_device = fields.Image(string="Picture of faulty device", tracking=True)
    is_agree = fields.Boolean(string="I agree to the terms and conditions", tracking=True)
    signature = fields.Image(string="Signature", tracking=True)
    sale_order = fields.Many2one('sale.order', string='Sale Order', tracking=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('refused', 'Refused'),
            ('approved', 'Approved'),
        ],
        default="new", tracking=True
    )
    reason = fields.Text(string='Reason', tracking=True)

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('rma.form')
        return super(RmaForm, self).create(vals)

    def action_approve(self):
        self.status = 'approved'
        template_id = self.env.ref('website_application.email_template_application_rma_warranty_approve').id
        template = self.env['mail.template'].browse(template_id)
        ctx = self.env.context.copy()
        ctx.update({
            'email_to': 'support@zbspos.com',
            'email_from': self.env.user.company_id.catchall_email,
            'service_type': dict(self._fields['service_type'].selection).get(self.service_type)
        })
        template.with_context(ctx).send_mail(self.id, force_send=True)
        ctx.update({
            'email_to': 'accounting@zbspos.com',

        })
        template.with_context(ctx).send_mail(self.id, force_send=True)
        if self.email:
            ctx.update({
                'email_to': self.email,

            })
            template.with_context(ctx).send_mail(self.id, force_send=True)
        else:
            if self.sale_order:
                ctx.update({
                    'email_to': self.sale_order.partner_id.email,

                })
                template.with_context(ctx).send_mail(self.id, force_send=True)

    def action_refuse(self):
        self.status = 'refused'
        template_id = self.env.ref('website_application.email_template_application_rma_warranty_reject').id
        template = self.env['mail.template'].browse(template_id)
        ctx = self.env.context.copy()
        ctx.update({
            'email_to': 'support@zbspos.com',
            'email_from': self.env.user.company_id.catchall_email,
            'service_type': dict(self._fields['service_type'].selection).get(self.service_type),

        })
        if self.reason:
            ctx.update({
                'reason': self.reason
            })
        else:
            raise UserError("You have not filled the rejected reason!")
        template.with_context(ctx).send_mail(self.id, force_send=True)
        if self.email:
            ctx.update({
                'email_to': self.email,

            })
            template.with_context(ctx).send_mail(self.id, force_send=True)
        else:
            if self.sale_order:
                ctx.update({
                    'email_to': self.sale_order.partner_id.email,

                })
                template.with_context(ctx).send_mail(self.id, force_send=True)
