# -*- coding: utf-8 -*-

import json
from collections import defaultdict
from datetime import datetime
from itertools import groupby
from operator import itemgetter
from re import findall as regex_findall
from re import split as regex_split

from dateutil import relativedelta

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero, float_repr, float_round
from odoo.tools.misc import clean_context, format_date, OrderedSet

PROCUREMENT_PRIORITIES = [('0', 'Normal'), ('1', 'Urgent')]


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        if self.picking_ids and self.env.company.sh_stop_auto_add_lot:
            for picking in self.picking_ids:
                is_lot_serial_product = False
                if picking.move_ids_without_package:
                    for line in picking.move_ids_without_package:
                        if line.product_id.tracking in ['lot','serial']:
                            is_lot_serial_product = True
                if is_lot_serial_product:
                    picking.do_unreserve()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def write(self, vals):
        if self.order_id.state == 'sale' and vals.get('product_uom_qty'):
            self.env.context = dict(self.env.context)
            self.env.context.update({'from_sol_qty_change': True})
        return super(SaleOrderLine, self).write(vals)


class Stockquant_inherit(models.Model):
    _inherit = "stock.quant"

    def _gather(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        self.env['stock.quant'].flush(['location_id', 'owner_id', 'package_id', 'lot_id', 'product_id'])
        self.env['product.product'].flush(['virtual_available'])
        removal_strategy = self._get_removal_strategy(product_id, location_id)
        removal_strategy_order = self._get_removal_strategy_order(removal_strategy)
        domain = [
            ('product_id', '=', product_id.id),
        ]
        if not strict:
            if lot_id:
                # domain = expression.AND([['|', ('lot_id', '=', lot_id.id), ('lot_id', '=', False)], domain])
                if lot_id and len(lot_id) == 1:
                    domain = expression.AND([['|', ('lot_id', '=', lot_id.id), ('lot_id', '=', False)], domain])
                if lot_id and len(lot_id) > 1:
                    domain = expression.AND([['|', ('lot_id', 'in', lot_id.ids), ('lot_id', '=', False)], domain])
            if package_id:
                domain = expression.AND([[('package_id', '=', package_id.id)], domain])
            if owner_id:
                domain = expression.AND([[('owner_id', '=', owner_id.id)], domain])
            domain = expression.AND([[('location_id', 'child_of', location_id.id)], domain])
        else:
            domain = expression.AND([['|', ('lot_id', '=', lot_id.id), ('lot_id', '=', False)] if lot_id else [('lot_id', '=', False)], domain])
            domain = expression.AND([[('package_id', '=', package_id and package_id.id or False)], domain])
            domain = expression.AND([[('owner_id', '=', owner_id and owner_id.id or False)], domain])
            domain = expression.AND([[('location_id', '=', location_id.id)], domain])

        # Copy code of _search for special NULLS FIRST/LAST order
        self.check_access_rights('read')
        query = self._where_calc(domain)
        self._apply_ir_rules(query, 'read')
        from_clause, where_clause, where_clause_params = query.get_sql()
        where_str = where_clause and (" WHERE %s" % where_clause) or ''
        query_str = 'SELECT "%s".id FROM ' % self._table + from_clause + where_str + " ORDER BY "+ removal_strategy_order
        self._cr.execute(query_str, where_clause_params)
        res = self._cr.fetchall()
        # No uniquify list necessary as auto_join is not applied anyways...
        quants = self.browse([x[0] for x in res])
        quants = quants.sorted(lambda q: not q.lot_id)
        return quants


class Picking(models.Model):
    _inherit = "stock.picking"

    def _create_backorder(self):
        """ This method is called when the user chose to create a backorder. It will create a new
        picking, the backorder, and move the stock.moves that are not `done` or `cancel` into it.
        """
        backorders = self.env['stock.picking']
        for picking in self:
            moves_to_backorder = picking.move_lines.filtered(lambda x: x.state not in ('done', 'cancel'))
            if moves_to_backorder:
                backorder_picking = picking.copy({
                    'name': '/',
                    'move_lines': [],
                    'move_line_ids': [],
                    'backorder_id': picking.id
                })
                picking.message_post(
                    body=_('The backorder <a href=# data-oe-model=stock.picking data-oe-id=%d>%s</a> has been created.') % (
                        backorder_picking.id, backorder_picking.name))
                moves_to_backorder.write({'picking_id': backorder_picking.id})
                moves_to_backorder.move_line_ids.package_level_id.write({'picking_id': backorder_picking.id})
                moves_to_backorder.mapped('move_line_ids').write({'picking_id': backorder_picking.id})
                backorders |= backorder_picking
        # if backorders:
        #     backorders.action_assign()
        return backorders


    def action_assign(self):
        if self._context.get('from_sol_qty_change'):
            return True
        res = super(Picking, self).action_assign()
        if self and len(self) == 1:
            if self.picking_type_code == 'internal' or self.picking_type_code == 'outgoing':
                lst = []
                reserved_move_lines = self.move_line_ids.filtered(lambda l:l.product_id.tracking in ['serial','lot'] and l.product_uom_qty)
                unreserve_move_lines = self.move_line_ids.filtered(lambda l:l.product_id.tracking in ['serial','lot'] and not l.product_uom_qty)
                for each in self.move_line_ids:
                    if each.lot_id:
                        each.delivery_lot_name = each.lot_id.name
                if reserved_move_lines:
                    for each in reserved_move_lines:
                        if each.lot_id and unreserve_move_lines:
                            unreserve_line = unreserve_move_lines.filtered(lambda l:l.lot_id == each.lot_id)
                            if unreserve_line:
                                lst.append(unreserve_line)
                if lst:
                    for each in lst:
                        each.sudo().unlink()
        if self and len(self) > 1:
            for rec in self:
                if rec.picking_type_code == 'internal' or rec.picking_type_code == 'outgoing':
                    lst = []
                    reserved_move_lines = rec.move_line_ids.filtered(lambda l:l.product_id.tracking in ['serial','lot'] and l.product_uom_qty)
                    unreserve_move_lines = rec.move_line_ids.filtered(lambda l:l.product_id.tracking in ['serial','lot'] and not l.product_uom_qty)
                    for each in rec.move_line_ids:
                        if each.lot_id:
                            each.delivery_lot_name = each.lot_id.name
                    if reserved_move_lines:
                        for each in reserved_move_lines:
                            if each.lot_id and unreserve_move_lines:
                                unreserve_line = unreserve_move_lines.filtered(lambda l:l.lot_id == each.lot_id)
                                if unreserve_line:
                                    lst.append(unreserve_line)
                    if lst:
                        for each in lst:
                            each.sudo().unlink()
        return res