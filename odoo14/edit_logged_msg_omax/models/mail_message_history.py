# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api,fields, models
from datetime import timedelta, datetime



class MailMessageHistory(models.Model):
    _name = "mail.message.history"
    _description = "Mail Message History"
    
    mail_message_id = fields.Many2one('mail.message',string="Mail Message Reference", readonly=True, ondelete='cascade')
    date_time = fields.Datetime(string='Date', readonly=True)
    body = fields.Html('Body', default='', sanitize_style=True, readonly=True)
    message_edit = fields.Many2one('res.users', string='Edited by', readonly=True)
    
    
    
class Message(models.Model):
    _inherit = 'mail.message'
    
    mail_message_history_line = fields.One2many('mail.message.history', 'mail_message_id', string='Message History')
    def write(self, vals):
        res = None
        for each in self:
            exist_body = each.body
            res = super(Message, each).write(vals)
            custom_ctx = each._context.get('chatter_message_id')
            if each.env.context.get('chatter_message_id'):
                if 'body' in vals:
                    value = {
                            'mail_message_id' : each.id,
                            'date_time' : datetime.now(),
                            'body' : vals['body'],
                            'message_edit' : each.env.user.id,
                        }
                    new_body = vals['body']

                    new_body_text = each.env["ir.fields.converter"].text_from_html(new_body, 100, 1000, "...")
                    exist_body_text = each.env["ir.fields.converter"].text_from_html(exist_body, 100, 1000, "...")
                    if exist_body_text != new_body_text:
                        create = each.mail_message_history_line.create(value)
        return res
