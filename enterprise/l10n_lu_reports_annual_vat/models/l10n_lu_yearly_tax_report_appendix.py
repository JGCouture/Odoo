# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.exceptions import UserError

class L10nLuYearlyTaxReportAppendix(models.Model):
    """
    The manual fields in the Appendix to Operational expenditures in the LU yearly VAT report
    """
    _name = 'l10n_lu_reports_annual_vat.report.appendix.expenditures'
    _description = '"Operational Expenditures" Appendix for LU'

    # ==== Business fields ====
    report_id = fields.Many2one("l10n_lu.yearly.tax.report.manual", string="Tax Report")
    report_section_411 = fields.Char(string="Detail of expenses line 43 (411)", required=True)
    report_section_412 = fields.Float(string="Business portion expenditures VAT excluded (412)", required=True)
    report_section_413 = fields.Float(string="Business portion of VAT invoiced (413)", required=True)
