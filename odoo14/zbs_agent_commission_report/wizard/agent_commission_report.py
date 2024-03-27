# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
import xlwt
import calendar
import io
import base64
import re
import pytz


class AgentCommissionReport(models.TransientModel):
    _name = 'agent.commission.report'
    _description = "Agent Commission Report"

    def get_employee(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
        if employee_id:
            return employee_id.id

    data = fields.Binary(string="Data")
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')
    name = fields.Char(string='File Name', readonly=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    employee_id = fields.Many2one('hr.employee', default=get_employee, string="Agent")

    def print_xls(self):
        styleP = xlwt.XFStyle()
        stylePC = xlwt.XFStyle()
        stylePCleft = xlwt.XFStyle()
        styleBorder = xlwt.XFStyle()
        stylebigfont = xlwt.XFStyle()
        stylebigfonty = xlwt.XFStyle()
        fontbold = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment_lft = xlwt.Alignment()
        alignment_lft.horz = xlwt.Alignment.HORZ_LEFT
        font = xlwt.Font()
        fontP = xlwt.Font()
        bigfont = xlwt.Font()
        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        font.bold = False
        fontP.bold = True
        styleP.font = font
        # stylePC.font = fontP
        stylePC.alignment = alignment
        stylePCleft.alignment =alignment_lft
        styleBorder.font = fontP
        fontbold.font = fontP
        styleBorder.alignment = alignment
        styleBorder.borders = borders
        stylebigfont.font = bigfont
        bigfont.height = 320
        bigfont.font = bigfont
        bigfont.bold = True
        stylebigfont.alignment = alignment
        stylebigfont.borders = borders
        stylebigfonty.font = bigfont
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']
        bigfont.height = 320
        bigfont.font = bigfont
        bigfont.bold = True
        stylebigfonty.alignment = alignment
        stylebigfonty.borders = borders
        stylebigfonty.pattern= pattern
        employee_ids = []
        if self.employee_id:
            employee_ids.append(self.employee_id)
        else:
            dept_ids = self.env['hr.department'].search([], order="id")
            for each_d in dept_ids:
                sql_query = """
                            SELECT id,name from hr_employee
                            WHERE 
                            department_id = %i order by name
                        """ % (each_d.id)
                self.env.cr.execute(sql_query)
                sorted_lst = [row[0] for row in self.env.cr.fetchall()]
                if sorted_lst:
                    for each_emp in sorted_lst:
                        employee_ids.append(self.env['hr.employee'].browse(each_emp))
        employees_without_dept = self.env['hr.employee'].search([('department_id','=',False)])
        if employees_without_dept:
            for ewd in employees_without_dept:
                employee_ids.append(ewd)
        workbook = xlwt.Workbook(encoding="utf-8")
        for agent in employee_ids:
            start_date = self.start_date - relativedelta(months=12)
            sql_query = """
                        SELECT id from sale_order
                        WHERE 
                        CAST(date_order AS Date) BETWEEN '%s' AND '%s' 
                        AND company_id = %i 
                        AND x_studio_many2one_field_8mpil = %i
                        AND state in ('sale','cancel')
                    """ % (start_date, self.end_date, int(self.env.company.id), agent.id)
            self.env.cr.execute(sql_query)

            sale_order_lst = [row[0] for row in self.env.cr.fetchall()]
            if sale_order_lst:
                sale_order_ids = self.env['sale.order'].browse(sale_order_lst)
                incomplete_lst = []
                complete_lst = []
                cancel_lst = []
                commission_subtotal = 0
                bonus_cnt_partial = 0
                bonus_cnt_full = 0
                for each in sale_order_ids:
                    promo_line = False
                    pack_line = False
                    if each.order_line:
                        promo_line = each.order_line.filtered(lambda l:l.product_id.is_promotion_product)
                        pack_line = each.order_line.filtered(lambda l:l.product_id.is_package_product)
                    #date order
                    date_order = ''
                    if each.date_order:
                        date_order = datetime.strftime(each.date_order, '%m/%d/%Y')
                    #product & qty column
                    product_qty = ''
                    total_line = 0
                    if each.order_line:
                        sale_lines = each.order_line.filtered(lambda l: not l.product_id.not_show_in_agent_report and not l.display_type == 'line_section' and not l.display_type == 'line_note' and l.product_uom_qty > 0)
                        if sale_lines:
                            for line in sale_lines:
                                total_line += 1
                                if product_qty:
                                    product_qty += "\n" + str(round(line.product_uom_qty,2)) + 'x ' + line.product_id.name
                                else:
                                    product_qty = str(round(line.product_uom_qty, 2)) + 'x ' + line.product_id.name
                    if not total_line:
                        total_line = 1

                    paid_in_full = 'No'
                    paid_in_full_date = ''
                    paid_in_full_date_date = False
                    total_paid = 0
                    if each.invoice_ids:
                        payment_lst = []
                        for inv in each.invoice_ids:
                            if inv.payment_state in ['paid','in_payment']:
                                total_paid += inv.amount_total - inv.amount_residual
                                reconcile_inv_vals = inv._compute_payments_widget_reconciled_info_agent_commission()
                                if reconcile_inv_vals and reconcile_inv_vals.get('content'):
                                    for each_payment in reconcile_inv_vals.get('content'):
                                        if each_payment.get('account_payment_id'):
                                            payment_lst.append(each_payment.get('account_payment_id'))
                        last_payment_id = False
                        if payment_lst:
                            last_payment_id = self.env['account.payment'].sudo().browse(max(payment_lst))
                        if last_payment_id:
                            if last_payment_id.date:
                                paid_in_full_date = datetime.strftime(last_payment_id.date, '%m/%d/%Y')
                                paid_in_full_date_date = last_payment_id.date
                    if total_paid >= each.amount_total:
                        paid_in_full = 'Yes'

                    #misc ther cost
                    other_cost = 0
                    shipping_cost = 0
                    if each.order_line:
                        misc_order_line = each.order_line.filtered(lambda l:l.product_id.is_misc_product)
                        if misc_order_line:
                            other_cost = sum(misc_order_line.mapped('price_subtotal'))
                        shipping_order_line = each.order_line.filtered(lambda l:l.product_id.is_shipping_product)
                        if shipping_order_line:
                            shipping_cost = sum(shipping_order_line.mapped('price_subtotal'))
                    total_other_cost = shipping_cost + other_cost + each.amount_tax
                    net_amount =  each.amount_total - total_other_cost
                    saas = 'No'
                    if each.order_line:
                        subscription_order_line = each.order_line.filtered(lambda l:l.product_id.recurring_invoice)
                        if subscription_order_line:
                            saas = 'Yes'

                    commission_per = '0.00'
                    if agent.commission_per:
                        commission_per = '%.2f'% agent.commission_per

                    bonus = 0
                    # if each.order_line:
                    #     promotion_line = each.order_line.filtered(lambda l:l.product_id.is_promotion_product)
                    #     package_line = each.order_line.filtered(lambda l:l.product_id.is_package_product)
                    #     if package_line and promotion_line:
                    existing_sale_lines = self.env['sale.order.line'].search([('order_id.partner_id', '=', each.partner_id.id),
                                                                              ('order_id.state', 'in', ['sale','done']),
                                                                              '|',('product_id.is_promotion_product','=', True),
                                                                                ('product_id.is_package_product', '=', True)
                                                                              ])
                    order_lst = []
                    if existing_sale_lines:
                        for sale_line in existing_sale_lines:
                            if sale_line.order_id.id not in order_lst:
                                promotion_line_existing = sale_line.order_id.order_line.filtered(
                                    lambda l: l.product_id.is_promotion_product)
                                package_line_existing = sale_line.order_id.order_line.filtered(
                                    lambda l: l.product_id.is_package_product)
                                if promotion_line_existing and package_line_existing:
                                    order_lst.append(sale_line.order_id.id)
                    if order_lst and min(order_lst) == each.id:
                        bonus = 500

                    # if not bonus:
                    #     for line in each.order_line:
                    #         sale_order_line_ids = self.env['sale.order.line'].search([('product_id','=', line.product_id.id)] , order='id asc', limit=1)
                    #         if sale_order_line_ids:
                    #             check_product_line = each.order_line.filtered(lambda l:l.id == sale_order_line_ids[0].id)
                    #             if check_product_line:
                    #                 bonus = 500
                    #                 break
                    commission_amt = 0
                    paid_in_date_range = False
                    if paid_in_full_date_date:
                        if paid_in_full_date_date >= self.start_date and paid_in_full_date_date <= self.end_date:
                            paid_in_date_range = True
                    if each.amount_total <= 0:
                        paid_in_full = 'Yes'
                        if each.date_order and each.date_order.date() >= self.start_date and each.date_order.date() <= self.end_date:
                            paid_in_date_range = True
                    commission_amt += bonus
                    if agent.commission_per and net_amount:
                        commission_amt += (net_amount * agent.commission_per) / 100
                    order_type = ''
                    if each.sale_order_type:
                        if each.sale_order_type == 'new':
                            order_type = 'New'
                        elif each.sale_order_type == 'conversion':
                            order_type = 'Conversion'
                        elif each.sale_order_type == 'add_ons':
                            order_type = 'Add Ons'
                        elif each.sale_order_type == 'accessories':
                            order_type = 'Accessories'
                        elif each.sale_order_type == 'other':
                            order_type = 'Other'
                    if each.state == 'cancel':
                        if each.date_cancel and each.date_cancel >= self.start_date and each.date_cancel <= self.end_date:
                            inv_lst = []
                            if each.invoice_ids:
                                for each_inv in each.invoice_ids:
                                    if each_inv.name:
                                        inv_lst.append(each_inv.name)
                            if each.picking_ids:
                                cancel_lst.append({
                                    'date_order': date_order,
                                    'agent': agent.name,
                                    'invoice': ', '.join(inv_lst) if inv_lst else '',
                                    'customer': each.partner_id.name,
                                    'product_qty': product_qty,
                                    'paid_in_full': paid_in_full,
                                    'total': commission_amt,
                                    'total_line': total_line,
                                    'so_no': each.name,
                                    'cancel_date': datetime.strftime(each.date_cancel, '%m/%d/%Y') if each.date_cancel else '',
                                    'order_type' : order_type
                                })
                    else:
                        if paid_in_full == 'Yes' and paid_in_date_range:
                            commission_subtotal += commission_amt
                            if each.date_order.date() >= self.start_date and each.date_order.date() <= self.end_date:
                                if promo_line and pack_line:
                                    bonus_cnt_full = bonus_cnt_full + 1
                            # if bonus:
                            #     bonus_cnt_full = bonus_cnt_full + 1
                            # worksheet.row(i).height = 400 + (total_line * 180)
                            complete_lst.append({
                                'name' : agent.name,
                                'date_order': date_order,
                                'paid_in_full_date': paid_in_full_date,
                                'so_number': each.name,
                                'partner': each.partner_id.name,
                                'product_qty': product_qty,
                                'paid_in_full': paid_in_full,
                                'amount_total': '%.2f'% each.amount_total,
                                'other_cost': '%.2f'% other_cost,
                                'amount_tax': '%.2f'% each.amount_tax,
                                'shipping_cost': '%.2f'% shipping_cost,
                                'net_amount': '%.2f'% net_amount,
                                'saas': saas,
                                'commission_per': commission_per,
                                'bonus': bonus,
                                'commission_amt': '%.2f'% commission_amt,
                                'order_type': order_type
                            })
                        else:
                            if (paid_in_full != 'Yes') or (paid_in_full == 'Yes' and paid_in_full_date_date and paid_in_full_date_date > self.end_date):
                                if bonus:
                                    bonus_cnt_partial = bonus_cnt_partial + 1
                                inv_lst = []
                                if each.invoice_ids:
                                    for each_inv in each.invoice_ids:
                                        if each_inv.name:
                                            inv_lst.append(each_inv.name)
                                if each.date_order.date() >= self.start_date and each.date_order.date() <= self.end_date:
                                    if promo_line and pack_line:
                                        bonus_cnt_full += 1
                                incomplete_lst.append({
                                    'date_order' : date_order,
                                    'agent' : agent.name,
                                    'invoice' : ', '.join(inv_lst) if inv_lst else '',
                                    'customer': each.partner_id.name,
                                    'product_qty': product_qty,
                                    'paid_in_full' : paid_in_full,
                                    'total' : commission_amt,
                                    'total_line' : total_line,
                                    'order_type': order_type
                                })
                if incomplete_lst or complete_lst or cancel_lst:
                    worksheet = workbook.add_sheet(agent.name + '_' + str(agent.id))
                    worksheet.col(0).width = 9000
                    worksheet.row(0).height = 480
                    worksheet.row(1).height = 480
                    worksheet.col(1).width = 5600
                    worksheet.col(2).width = 5000
                    worksheet.col(3).width = 6000
                    worksheet.col(4).width = 6000
                    worksheet.col(5).width = 9000
                    worksheet.col(6).width = 5000
                    worksheet.col(7).width = 5000
                    worksheet.col(8).width = 5000
                    worksheet.col(9).width = 5000
                    worksheet.col(10).width = 5000
                    worksheet.col(11).width = 5000
                    worksheet.col(12).width = 5000
                    worksheet.col(13).width = 5000
                    worksheet.col(14).width = 5000
                    worksheet.col(15).width = 5000
                    date = datetime.strftime(self.start_date, '%m/%d/%Y') + ' To ' + datetime.strftime(self.end_date,
                                                                                                       '%m/%d/%Y')
                    worksheet.write_merge(0, 0, 0, 13, agent.name + ' : ' + ' Commission Report', style=stylebigfont)
                    worksheet.write_merge(1, 1, 15, 15, 'TOTAL', style=stylebigfont)
                    worksheet.write_merge(1, 1, 0, 13, date, style=stylebigfont)
                    worksheet.write_merge(3, 3, 0, 0, 'AGENT', style=styleBorder)
                    worksheet.write_merge(3, 3, 1, 1, 'SO DATE', style=styleBorder)
                    worksheet.write_merge(3, 3, 2, 2, 'PAID IN FULL DATE', style=styleBorder)
                    worksheet.write_merge(3, 3, 3, 3, 'INVOICE#', style=styleBorder)
                    worksheet.write_merge(3, 3, 4, 4, 'ORDER TYPE', style=styleBorder)
                    worksheet.write_merge(3, 3, 5, 5, 'CUSTOMER NAME', style=styleBorder)
                    worksheet.write_merge(3, 3, 6, 6, 'PRODUCT & QTY', style=styleBorder)
                    worksheet.write_merge(3, 3, 7, 7, 'PAID IN FULL?', style=styleBorder)
                    worksheet.write_merge(3, 3, 8, 8, 'INVOICE TOTAL', style=styleBorder)
                    worksheet.write_merge(3, 3, 9, 9, 'OTHER', style=styleBorder)
                    worksheet.write_merge(3, 3, 10, 10, 'SALES TAX', style=styleBorder)
                    worksheet.write_merge(3, 3, 11, 11, 'SHIPPING', style=styleBorder)
                    worksheet.write_merge(3, 3, 12, 12, 'NET', style=styleBorder)
                    worksheet.write_merge(3, 3, 13, 13, 'Saas?', style=styleBorder)
                    worksheet.write_merge(3, 3, 14, 14, 'COMM %', style=styleBorder)
                    worksheet.write_merge(3, 3, 15, 15, 'BONUS', style=styleBorder)
                    worksheet.write_merge(3, 3, 16, 16, 'TOTAL', style=styleBorder)
                    i = 4
                    if complete_lst:
                        for complete_order in complete_lst:
                            worksheet.write_merge(i, i, 0, 0, complete_order.get('name') or '', style=stylePC)
                            worksheet.write_merge(i, i, 1, 1, complete_order.get('date_order'), style=stylePC)
                            worksheet.write_merge(i, i, 2, 2, complete_order.get('paid_in_full_date'), style=stylePC)
                            worksheet.write_merge(i, i, 3, 3, complete_order.get('so_number'), style=stylePC)
                            worksheet.write_merge(i, i, 4, 4, complete_order.get('order_type'), style=stylePC)
                            worksheet.write_merge(i, i, 5, 5, complete_order.get('partner'), style=stylePC)
                            worksheet.write_merge(i, i, 6, 6, complete_order.get('product_qty'), style=stylePCleft)
                            worksheet.write_merge(i, i, 7, 7, complete_order.get('paid_in_full'), style=stylePC)
                            worksheet.write_merge(i, i, 8, 8, complete_order.get('amount_total'), style=stylePC)
                            worksheet.write_merge(i, i, 9, 9, complete_order.get('other_cost'), style=stylePC)
                            worksheet.write_merge(i, i, 10, 10, complete_order.get('amount_tax'), style=stylePC)
                            worksheet.write_merge(i, i, 11, 11, complete_order.get('shipping_cost') , style=stylePC)
                            worksheet.write_merge(i, i, 12, 12, complete_order.get('net_amount'), style=stylePC)
                            worksheet.write_merge(i, i, 13, 13, complete_order.get('saas'), style=stylePC)
                            worksheet.write_merge(i, i, 14, 14, complete_order.get('commission_per') , style=stylePC)
                            worksheet.write_merge(i, i, 15, 15, complete_order.get('bonus'), style=stylePC)
                            worksheet.write_merge(i, i, 16, 16, complete_order.get('commission_amt'), style=stylePC)
                            i = i + 1
                    i = i + 1
                    worksheet.write_merge(i, i, 15, 15, "Sub Total", style=styleBorder)
                    worksheet.write_merge(i, i, 16, 16, '%.2f'% commission_subtotal, style=styleBorder)
                    i = i + 1
                    worksheet.write_merge(i, i, 14, 14, "Qty", style=stylePC)
                    worksheet.write_merge(i, i, 15, 15, '%.2f' % bonus_cnt_full, style=stylePC)
                    i = i + 1
                    final_bonus = 0
                    final_total = commission_subtotal
                    if bonus_cnt_full >= 1 and bonus_cnt_full <=4:
                        final_bonus = 0
                        final_total += 0
                    if bonus_cnt_full >=5 and bonus_cnt_full <= 6:
                        final_bonus = 500
                        final_total += 500
                    if bonus_cnt_full >= 7 and bonus_cnt_full <=8:
                        final_bonus = 1000
                        final_total += 1000
                    if bonus_cnt_full >= 9 and bonus_cnt_full <=10:
                        final_bonus = 1500
                        final_total += 1500
                    if bonus_cnt_full >= 11 and bonus_cnt_full <=12:
                        final_bonus = 2000
                        final_total += 2000
                    if bonus_cnt_full >= 13 and bonus_cnt_full <=14:
                        final_bonus = 2500
                        final_total += 2500
                    if bonus_cnt_full >= 15 and bonus_cnt_full <= 16:
                        final_bonus = 3000
                        final_total += 3000
                    if bonus_cnt_full >= 17:
                        final_bonus = 3000
                        final_total += 3000

                    worksheet.write_merge(i, i, 15, 15, "Bonus", style=stylePC)
                    worksheet.write_merge(i, i, 16, 16, '%.2f' % final_bonus, style=stylePC)
                    i = i +1
                    worksheet.write_merge(i, i, 15, 15, "TOTAL", style=styleBorder)
                    worksheet.write_merge(i, i, 16, 16, '%.2f' % final_total, style=styleBorder)
                    worksheet.write_merge(1, 1, 16, 16, '%.2f' % final_total, style=stylebigfonty)
                    if incomplete_lst:
                        worksheet.write_merge(i, i, 0, 8, agent.name + ' : ' + 'INCOMPLETE',style=styleBorder)
                        i = i + 1
                        worksheet.write_merge(i, i, 0, 0, "AGENT", style=styleBorder)
                        worksheet.write_merge(i, i, 1, 1, "SO DATE", style=styleBorder)
                        worksheet.write_merge(i, i, 2, 2, "", style=styleBorder)
                        worksheet.write_merge(i, i, 3, 3, "INVOICE#", style=styleBorder)
                        worksheet.write_merge(i, i, 4, 4, "ORDER TYPE", style=styleBorder)
                        worksheet.write_merge(i, i, 5, 5, "CUSTOMER NAME", style=styleBorder)
                        worksheet.write_merge(i, i, 6, 6, "PRODUCT & QTY", style=styleBorder)
                        worksheet.write_merge(i, i, 7, 7, "PAID IN FULL?", style=styleBorder)
                        worksheet.write_merge(i, i, 8, 8, "INVOICE TOTAL", style=styleBorder)
                        i = i + 1
                        for pending_order in incomplete_lst:
                            # worksheet.row(i).height = 400 + (180 * pending_order.get('total_line'))
                            worksheet.write_merge(i, i, 0, 0, pending_order.get('agent'), style=stylePC)
                            worksheet.write_merge(i, i, 1, 1, pending_order.get('date_order'), style=stylePC)
                            worksheet.write_merge(i, i, 2, 2, '', style=stylePC)
                            worksheet.write_merge(i, i, 3, 3, pending_order.get('invoice'), style=stylePC)
                            worksheet.write_merge(i, i, 4, 4, pending_order.get('order_type'), style=stylePC)
                            worksheet.write_merge(i, i, 5, 5, pending_order.get('customer'), style=stylePC)
                            worksheet.write_merge(i, i, 6, 6, pending_order.get('product_qty'), style=stylePCleft)
                            worksheet.write_merge(i, i, 7, 7, pending_order.get('paid_in_full'), style=stylePCleft)
                            worksheet.write_merge(i, i, 8, 8, '%.2f'% pending_order.get('total'), style=stylePC)
                            i = i + 1

                    #cancel order data
                    if cancel_lst:
                        i = i + 1
                        worksheet.write_merge(i, i, 0, 7, agent.name + ' : ' + 'CANCELED ORDERS', style=styleBorder)
                        i = i + 1
                        worksheet.write_merge(i, i, 0, 0, "AGENT", style=styleBorder)
                        worksheet.write_merge(i, i, 1, 1, "SO DATE", style=styleBorder)
                        worksheet.write_merge(i, i, 2, 2, "SO No.", style=styleBorder)
                        worksheet.write_merge(i, i, 3, 3, "Cancellation Date", style=styleBorder)
                        worksheet.write_merge(i, i, 4, 4, "ORDER TYPE", style=styleBorder)
                        # worksheet.write_merge(i, i, 4, 4, "INVOICE#", style=styleBorder)
                        worksheet.write_merge(i, i, 5, 5, "CUSTOMER NAME", style=styleBorder)
                        worksheet.write_merge(i, i, 6, 6, "PRODUCT & QTY", style=styleBorder)
                        worksheet.write_merge(i, i, 7, 7, "PAID IN FULL?", style=styleBorder)
                        worksheet.write_merge(i, i, 8, 8, "INVOICE TOTAL", style=styleBorder)
                        i = i + 1
                        for co in cancel_lst:
                            # worksheet.row(i).height = 400 + (180 * pending_order.get('total_line'))
                            worksheet.write_merge(i, i, 0, 0, co.get('agent'), style=stylePC)
                            worksheet.write_merge(i, i, 1, 1, co.get('date_order'), style=stylePC)
                            worksheet.write_merge(i, i, 2, 2, co.get('so_no'), style=stylePC)
                            worksheet.write_merge(i, i, 3, 3, co.get('cancel_date'), style=stylePC)
                            worksheet.write_merge(i, i, 4, 4, co.get('order_type'), style=stylePC)
                            # worksheet.write_merge(i, i, 4, 4, co.get('invoice'), style=stylePC)
                            worksheet.write_merge(i, i, 5, 5, co.get('customer'), style=stylePC)
                            worksheet.write_merge(i, i, 6, 6, co.get('product_qty'), style=stylePCleft)
                            worksheet.write_merge(i, i, 7, 7, co.get('paid_in_full'), style=stylePCleft)
                            worksheet.write_merge(i, i, 8, 8, '%.2f'% co.get('total'), style=stylePC)
                            i = i + 1
                    file_data = io.BytesIO()
                    workbook.save(file_data)
        self.write({
            'state': 'get',
            'data': base64.encodestring(file_data.getvalue()),
            'name': 'agent_commission_report.xls'
        })
        return {
            'name': 'Agent Commission Report',
            'type': 'ir.actions.act_window',
            'res_model': 'agent.commission.report',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new'
        }