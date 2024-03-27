# -*- encoding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2020 (http://www.bistasolutions.com)
#
##############################################################################

from odoo import models, fields, api, _
from odoo.tools.misc import get_lang
from odoo.exceptions import ValidationError



class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def action_create_payments(self):
        res = super(AccountPaymentRegister, self).action_create_payments()
        inv_ids = self.line_ids.mapped('move_id')
        for inv_id in inv_ids.filtered(lambda l: not l.is_down_payment_inv):
            inv_id.task_move_to_shipping()
        return res


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super(Picking, self).button_validate()
        tasks_ids = self.sale_id.mapped('tasks_ids')
        for task in tasks_ids:
            stage_id = self.env['project.task.type'].search([
                ('is_auto_ship', '=', True),
                ('project_ids', 'in', task.project_id.id)])
            if stage_id:
                task.write({'stage_id': stage_id.id})
        return res


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        """
        Override function to remove analytic account and analytic tags in
        downpayment product invoice line.
        :param order:
        :param name:
        :param amount:
        :param so_line:
        :return:
        """
        vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(
            order, name, amount, so_line)
        if self.advance_payment_method != 'delivered':
            vals['is_down_payment_inv'] = True
        return vals


class AccountMove(models.Model):

    _inherit = 'account.move'

    is_down_payment_inv = fields.Boolean(string="Down Payment Invoice")

    def task_move_to_shipping(self):
        order_id = self.invoice_line_ids.mapped('sale_line_ids').mapped(
            'order_id')
        tasks_ids = order_id.mapped('tasks_ids')
        for task in tasks_ids:
            stage_id = self.env['project.task.type'].search([
                ('is_inv_auto_move_inv', '=', True),
                ('project_ids', 'in', task.project_id.id)])
            if stage_id:
                task.with_context(from_inv=True).write({'stage_id': stage_id.id})

    def js_assign_outstanding_line(self, line_id):
        res = super(AccountMove, self).js_assign_outstanding_line(line_id)
        if self.payment_state == 'in_payment':
            self.task_move_to_shipping()
        return res


class Project(models.Model):
    _inherit = 'project.project'

    is_validation = fields.Boolean(string="Parent Task Validation")


class TaskType(models.Model):
    _inherit = 'project.task.type'

    is_inv_auto_create = fields.Boolean(string="Auto Invoice Created",
                                        copy=False)
    is_inv_auto_move_inv = fields.Boolean(string="Auto Move Invoice",
                                          copy=False)
    is_auto_ship = fields.Boolean(string="Auto Ship", copy=False,
                                  help="Changes Status based on delivery.")
    is_inprogress = fields.Boolean(string="In Progress")


class Task(models.Model):
    _inherit = 'project.task'

    is_inv_create = fields.Boolean(string="Invoice Created",
                                   compute='_compute_inv_create')
    is_need_approval = fields.Boolean(string="Is need approval",
                                      compute="_is_need_approval", store=True)
    is_approval_mng = fields.Boolean(string="Is approval manager",
                                     compute="_is_approval_mng")
    is_approval_user = fields.Boolean(string="Is approval manager",
                                     compute="_is_approval_mng")

    def _is_approval_mng(self):
        for obj in self:
            is_approval_mng = False
            is_approval_user = False
            if obj.is_need_approval and obj.env.user.has_group(
                    'project.group_project_user'):
                is_approval_user = True
            if obj.is_need_approval and obj.env.user.has_group(
                    'project.group_project_manager'):
                is_approval_mng = True
                is_approval_user = False

            obj.is_approval_mng = is_approval_mng
            obj.is_approval_user = is_approval_user

    @api.depends('child_ids', 'child_ids.stage_id', 'stage_id')
    def _is_need_approval(self):
        for obj in self:
            is_need_approval = False
            child_ids = obj.child_ids.filtered(
                lambda l: l.project_id.is_validation and not l.stage_id.is_closed)
            if child_ids and obj.stage_id.is_inprogress:
                is_need_approval = True
            obj.is_need_approval = is_need_approval

    def _compute_inv_create(self):
        for obj in self:
            is_inv_create = False
            order_line = obj.sale_order_id.mapped('order_line')
            order_line = order_line.filtered(
                lambda l: l.qty_invoiced < l.product_uom_qty)
            if order_line and not self.parent_id:
                is_inv_create = True
            obj.is_inv_create = is_inv_create

    def write(self, vals):
        if 'stage_id' in vals:
            auto_inv_stage_id = self.env['project.task.type'].browse(vals.get(
                'stage_id')).is_inv_auto_create
            if auto_inv_stage_id and self.is_inv_create and not self.parent_id:
                moves = self.sale_order_id._create_invoices(final=True)
                moves.action_post()
                template = self.env.ref('account.email_template_edi_invoice',
                                        raise_if_not_found=False)
                lang = get_lang(self.env)
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
            if self.is_need_approval and self.is_approval_mng:
                child_ids = self.child_ids.filtered(
                    lambda
                        l: l.project_id.is_validation and not l.stage_id.is_closed)
                for child in child_ids:
                    closed_stage = child.project_id.type_ids.filtered(
                        'is_closed')
                    child.write({'stage_id': closed_stage and closed_stage[
                        0].id})
            if self.is_need_approval and self.is_approval_user and 'from_inv'\
                    not in self._context:
                raise ValidationError(
                    _("Sub task's are not completed yet..!"))
        res = super(Task, self).write(vals)
        return res
