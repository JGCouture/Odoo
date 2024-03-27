# -*- coding: utf-8 -*-

import json
from collections import defaultdict
from datetime import datetime
from itertools import groupby
from operator import itemgetter
from re import findall as regex_findall
from re import split as regex_split

from dateutil import relativedelta
from odoo.exceptions import UserError, Warning

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero, float_repr, float_round
from odoo.tools.misc import clean_context, format_date, OrderedSet


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _update_reserved_quantity(self, need, available_quantity, location_id, lot_id=None, package_id=None, owner_id=None, strict=True):
        """ Create or update move lines.
        """
        self.ensure_one()

        if self.picking_code == 'outgoing' or self.picking_code == 'internal' and not lot_id:
            lots = []
            if self.move_line_ids:
                prod_move_line = self.move_line_ids.filtered(lambda l:l.product_id == self.product_id)
                if prod_move_line:
                    for line in prod_move_line:
                        lots.append(line.lot_id.id)
                    if lots:
                        lot_id = self.env['stock.production.lot'].browse(lots)
                    else:
                        lot_id = self.env['stock.production.lot']
                    # prod_move_line.sudo().unlink()

        if not lot_id:
            lot_id = self.env['stock.production.lot']
        if not package_id:
            package_id = self.env['stock.quant.package']
        if not owner_id:
            owner_id = self.env['res.partner']

        taken_quantity = min(available_quantity, need)

        # `taken_quantity` is in the quants unit of measure. There's a possibility that the move's
        # unit of measure won't be respected if we blindly reserve this quantity, a common usecase
        # is if the move's unit of measure's rounding does not allow fractional reservation. We chose
        # to convert `taken_quantity` to the move's unit of measure with a down rounding method and
        # then get it back in the quants unit of measure with an half-up rounding_method. This
        # way, we'll never reserve more than allowed. We do not apply this logic if
        # `available_quantity` is brought by a chained move line. In this case, `_prepare_move_line_vals`
        # will take care of changing the UOM to the UOM of the product.
        if not strict and self.product_id.uom_id != self.product_uom:
            taken_quantity_move_uom = self.product_id.uom_id._compute_quantity(taken_quantity, self.product_uom, rounding_method='DOWN')
            taken_quantity = self.product_uom._compute_quantity(taken_quantity_move_uom, self.product_id.uom_id, rounding_method='HALF-UP')

        quants = []
        rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        if self.product_id.tracking == 'serial':
            if float_compare(taken_quantity, int(taken_quantity), precision_digits=rounding) != 0:
                taken_quantity = 0

        try:
            with self.env.cr.savepoint():
                if not float_is_zero(taken_quantity, precision_rounding=self.product_id.uom_id.rounding):
                    quants = self.env['stock.quant']._update_reserved_quantity(
                        self.product_id, location_id, taken_quantity, lot_id=lot_id,
                        package_id=package_id, owner_id=owner_id, strict=strict
                    )
        except UserError:
            taken_quantity = 0

        # Find a candidate move line to update or create a new one.
        for reserved_quant, quantity in quants:
            to_update = next((line for line in self.move_line_ids if line._reservation_is_updatable(quantity, reserved_quant)), False)
            if to_update:
                uom_quantity = self.product_id.uom_id._compute_quantity(quantity, to_update.product_uom_id, rounding_method='HALF-UP')
                uom_quantity = float_round(uom_quantity, precision_digits=rounding)
                uom_quantity_back_to_product_uom = to_update.product_uom_id._compute_quantity(uom_quantity, self.product_id.uom_id, rounding_method='HALF-UP')
            if to_update and float_compare(quantity, uom_quantity_back_to_product_uom, precision_digits=rounding) == 0:
                to_update.with_context(bypass_reservation_update=True).product_uom_qty += uom_quantity
            else:
                if self.product_id.tracking == 'serial':
                    self.env['stock.move.line'].create([self._prepare_move_line_vals(quantity=1, reserved_quant=reserved_quant) for i in range(int(quantity))])
                else:
                    self.env['stock.move.line'].create(self._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant))
        return taken_quantity

    @api.onchange('move_line_ids', 'move_line_nosuggest_ids')
    def onchange_move_line_ids(self):
        res = super(StockMove, self).onchange_move_line_ids()
        if self.picking_type_id.code in ['internal', 'outgoing']:
            breaking_char = '\n'
            if self.picking_type_id.show_reserved:
                move_lines = self.move_line_ids
            else:
                move_lines = self.move_line_nosuggest_ids
            for move_line in move_lines:
                # Look if the `lot_name` contains multiple values.
                if breaking_char in (move_line.delivery_lot_name or ''):
                    split_lines = move_line.delivery_lot_name.split(breaking_char)
                    split_lines = list(filter(None, split_lines))
                    filter_list = []
                    [filter_list.append(x) for x in split_lines if x not in filter_list]
                    already_used_lot = []
                    if filter_list:
                        for each_lot in filter_list:
                            lot_id = self.env['stock.production.lot'].search([('name','=', each_lot),('company_id','=', move_line.company_id.id), ('product_id','=',move_line.product_id.id)])
                            if lot_id:
                                available = lot_id.quant_ids.filtered(lambda l:l.location_id.usage == 'internal' and l.available_quantity)
                                if not available:
                                    already_used_lot.append(each_lot)
                    if already_used_lot:
                        raise Warning("Following serial number already used please remove it : " + ','.join(already_used_lot))

                    lot_serial_id = self.env['stock.production.lot'].search(
                        [('name', '=', filter_list[0]), ('company_id', '=', move_line.company_id.id), ('product_id','=', move_line.product_id.id)])
                    if lot_serial_id:
                        available = lot_serial_id.quant_ids.filtered(
                            lambda l: l.location_id.usage == 'internal' and l.available_quantity)
                        move_line.delivery_lot_name = filter_list[0]
                        move_line.location_id = available[0].location_id.id
                        move_line.lot_id = lot_serial_id.id
                    if filter_list:
                        auto_moves_lst = []
                        for new_ml in filter_list[1:]:
                            lot_serial_id = self.env['stock.production.lot'].search(
                                [('name', '=', new_ml), ('company_id', '=', move_line.company_id.id),('product_id','=',move_line.product_id.id)])
                            if lot_serial_id:
                                available = lot_serial_id.quant_ids.filtered(
                                    lambda l: l.location_id.usage == 'internal' and l.available_quantity)
                                auto_moves_lst.append((0,0, {
                                    'delivery_lot_name': new_ml,
                                    'location_id': available[0].location_id.id,
                                    'move_id': self.id,
                                    'lot_id': lot_serial_id.id,
                                    'qty_done': 1,
                                }))
                        if auto_moves_lst:
                            self.update({'move_line_ids': auto_moves_lst})
                else:
                    if not move_line.lot_id:
                        lot_serial_id = self.env['stock.production.lot'].search(
                            [('name', '=', move_line.delivery_lot_name), ('company_id', '=', move_line.company_id.id), ('product_id','=',move_line.product_id.id)])
                        if lot_serial_id:
                            available = lot_serial_id.quant_ids.filtered(
                                lambda l: l.location_id.usage == 'internal' and l.available_quantity)
                            move_line.delivery_lot_name = move_line.delivery_lot_name
                            move_line.location_id = available[0].location_id.id
                            move_line.lot_id = lot_serial_id.id
        return res


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    delivery_lot_name = fields.Char(string="Lot/Serial")