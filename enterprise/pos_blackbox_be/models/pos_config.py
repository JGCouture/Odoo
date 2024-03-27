# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    report_sequence_number = fields.Integer()
    order_sequence_number = fields.Integer(string='Order Sequence Number',
                                           help='A sequence number that is incremented with each order', default=1)
    profo_order_sequence_number = fields.Integer(string='Proforma Order Sequence Number',
                                                 help='A sequence number that is incremented with each order',
                                                 default=1)
    iface_fiscal_data_module = fields.Many2one('iot.device',
                                               domain="[('type', '=', 'fiscal_data_module'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    def _compute_iot_device_ids(self):
        super(PosConfig, self)._compute_iot_device_ids()
        for config in self:
            if config.is_posbox:
                config.iot_device_ids += config.iface_fiscal_data_module

    @api.constrains("module_pos_discount", "module_pos_loyalty")
    def _check_blackbox_config(self):
        for config in self:
            if config.iface_fiscal_data_module and (config.module_pos_discount or config.module_pos_loyalty):
                raise UserError(_("Loyalty programs, reprint and global discounts cannot be used on a PoS associated with a blackbox."))

    def open_session_cb(self, check_coa=True):
        if self.iface_fiscal_data_module:
            self._check_insz_user()
            self._check_company_address()
            self._check_work_product_taxes()
            self._check_employee_insz_or_bis_number()
            self._check_pos_category()
        return super(PosConfig, self).open_session_cb(check_coa)

    def get_order_sequence_number(self):
        sequence = self.order_sequence_number
        self = self.with_context()
        self.order_sequence_number += 1
        return sequence

    def get_profo_order_sequence_number(self):
        sequence = self.profo_order_sequence_number
        self = self.with_context(allow_modify=True)
        self.profo_order_sequence_number += 1
        return sequence

    def _check_work_product_taxes(self):
        work_in = self.env.ref('pos_blackbox_be.product_product_work_in')
        work_out = self.env.ref('pos_blackbox_be.product_product_work_out')
        if not work_in.taxes_id or work_in.taxes_id.amount != 0 or not work_out.taxes_id or work_out.taxes_id.amount != 0:
            raise ValidationError(_("The WORK IN/OUT products must have a taxes with 0%."))

    def _check_insz_user(self):
        if not self.env.user.insz_or_bis_number:
            raise ValidationError(_("The user must have a INSZ or BIS number."))

    def _check_company_address(self):
        if not self.company_id.street:
            raise ValidationError(_("The address of the company must be filled."))

    def _check_pos_category(self):
        if self.limit_categories:
            if self.env.ref('pos_blackbox_be.pos_category_fdm').id not in self.iface_available_categ_ids.ids:
                raise ValidationError(_("You have to add the fiscal category to the limited category in order to use the fiscal data module"))

    @api.constrains('iface_fiscal_data_module', 'fiscal_position_ids')
    def _check_posbox_fp_tax_code(self):
        for config in self:
            for fp in config.fiscal_position_ids:
                for tax_line in fp.tax_ids:
                    if tax_line.tax_src_id.identification_letter and not tax_line.tax_dest_id.identification_letter:
                        raise ValidationError(_("Fiscal Position %s (tax %s) has an invalid tax amount. Only 21%%, 12%%, 6%% and 0%% are allowed.") % (fp.name, tax_line.tax_dest_id.name))

    def _check_employee_insz_or_bis_number(self):
        for config in self:
            if config.module_pos_hr:
                emp_list = []
                employees = config.employee_ids or self.env['hr.employee'].search([])
                for emp in employees:
                    if not emp.insz_or_bis_number:
                        emp_list.append(emp.name)
                if not self.env.user.employee_id.insz_or_bis_number:
                    emp_list.append(self.env.user.name)

                if len(emp_list) > 0:
                    raise ValidationError((", ".join(str(emp) for emp in emp_list) + _(" must have an INSZ or BIS number.")))
