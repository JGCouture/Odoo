# -*- encoding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2019 (http://www.bistasolutions.com)
#
##############################################################################

from odoo import models
from odoo.tools.misc import get_lang


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super(Picking, self).button_validate()
        for rec in self:
            auto_create_invoice = self.partner_id.auto_create_invoice \
                or self.partner_id.parent_id.auto_create_invoice
            if not auto_create_invoice:
                auto_create_invoice = self.env['ir.config_parameter'].sudo().\
                    get_param('auto_create_invoice')

            auto_send_mail_invoice = self.partner_id.auto_send_mail_invoice \
                or self.partner_id.parent_id.auto_send_mail_invoice
            if not auto_send_mail_invoice:
                auto_send_mail_invoice = self.env['ir.config_parameter'].sudo().\
                    get_param('auto_send_mail_invoice')

            auto_validate_invoice = self.partner_id.auto_validate_invoice \
                or self.partner_id.parent_id.auto_validate_invoice
            if not auto_validate_invoice:
                auto_validate_invoice = self.env['ir.config_parameter'].sudo().\
                    get_param('auto_validate_invoice')

            if rec.move_lines and rec.picking_type_id.code == 'outgoing' and auto_create_invoice:
                move_lines = rec.move_lines.filtered(lambda x: x.sale_line_id and x.state == 'done')

                sale_order = move_lines.mapped('sale_line_id').mapped('order_id')
                if sale_order:
                    moves = sale_order._create_invoices(final=True)
                    if auto_send_mail_invoice:
                        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
                        lang = get_lang(rec.env)
                        if template and template.lang:
                            lang = template._render_lang(moves.ids)[moves.id]
                        else:
                            lang = lang.code

                        ctx = dict(
                            default_model='account.move',
                            mark_invoice_as_sent=True,
                            custom_layout="mail.mail_notification_paynow",
                            model_description=moves.with_context(lang=lang).type_name,
                            force_email=True
                        )
                        template.with_context(ctx).send_mail(moves.id, force_send=True)

                    if auto_validate_invoice:
                        moves.action_post()
        return res
