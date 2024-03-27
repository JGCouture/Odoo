# -*- coding: utf-8 -*-

import base64
import collections
import datetime
import hashlib
import pytz
import threading
import re

import requests
from lxml import etree
from random import randint
from werkzeug import urls

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # kp_online_order = fields.Many2one('online.order.form', string='Kp online order')
    find_ref = fields.Selection(string="How did you find us?", selection=[('agent', 'Agent'), ('referral', 'Referral'), ('online_ad', 'Online ad')])
    online_add = fields.Selection([
        ('wechat', 'WeChat'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('other', 'Other')
    ], string="Find By")
    ach_void_check = fields.Binary(string='ACH Void Check')

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if res.phone and len(res.phone) == 10:
            res.phone = res.phone[:3] + '-' + res.phone[3:6] + '-' + res.phone[6:]
        if res.mobile and len(res.mobile) == 10:
            res.mobile = res.mobile[:3] + '-' + res.mobile[3:6] + '-' + res.mobile[6:]
        return res

    def write(self, vals):
        if vals.get('phone') and len(vals.get('phone')) == 10:
            vals['phone'] = vals.get('phone')[:3] + '-' + vals.get('phone')[3:6] + '-' + vals.get('phone')[6:]
        if vals.get('mobile') and len(vals.get('mobile')) == 10:
            vals['mobile'] = vals.get('mobile')[:3] + '-' + vals.get('mobile')[3:6] + '-' + vals.get('mobile')[6:]
        return super(ResPartner, self).write(vals)

    @api.model
    def signup_retrieve_info(self, token):
        """ retrieve the user info about the token
            :return: a dictionary with the user information:
                - 'db': the name of the database
                - 'token': the token, if token is valid
                - 'name': the name of the partner, if token is valid
                - 'login': the user login, if the user already exists
                - 'email': the partner email, if the user does not exist
        """
        partner = self._signup_retrieve_partner(token, raise_exception=True)
        res = {'db': self.env.cr.dbname}
        if partner.signup_valid:
            res['token'] = token
            res['name'] = partner.name
        if partner.user_ids:
            res['login'] = partner.user_ids[0].login
        else:
            res['email'] = res['login'] = partner.email or ''
        if partner.street:
            res['street'] = partner.street
        if partner.street2:
            res['street2'] = partner.street2
        if partner.city:
            res['city'] = partner.city
        if partner.zip:
            res['zip1'] = partner.zip
        if partner.state_id:
            res['state_id'] = partner.state_id.id
        if partner.country_id:
            res['country_id'] = partner.country_id.id
        if partner.mobile:
            res['mobile'] = partner.mobile
        if partner.phone:
            res['phone'] = partner.phone
        if partner.x_studio_owner_name:
            res['x_studio_owner_name'] = partner.x_studio_owner_name
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        self = self.with_user(name_get_uid or self.env.uid)
        # as the implementation is in SQL, we force the recompute of fields if necessary
        self.recompute(['display_name'])
        self.flush()
        if args is None:
            args = []
        order_by_rank = self.env.context.get('res_partner_search_mode')
        if (name or order_by_rank) and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            self.check_access_rights('read')
            where_query = self._where_calc(args)
            self._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            from_str = from_clause if from_clause else 'res_partner'
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(self.env.cr)

            fields = self._get_name_search_order_by_fields()

            query = """SELECT res_partner.id
                         FROM {from_str}
                      {where} ({email} {operator} {percent}
                           OR {display_name} {operator} {percent}
                           OR {reference} {operator} {percent}
                           OR {phone} {operator} {percent}
                           OR {vat} {operator} {percent})
                           -- don't panic, trust postgres bitmap
                     ORDER BY {fields} {display_name} {operator} {percent} desc,
                              {display_name}
                    """.format(from_str=from_str,
                               fields=fields,
                               where=where_str,
                               operator=operator,
                               email=unaccent('res_partner.email'),
                               display_name=unaccent('res_partner.display_name'),
                               reference=unaccent('res_partner.ref'),
                               phone=unaccent('res_partner.phone'),
                               percent=unaccent('%s'),
                               vat=unaccent('res_partner.vat'),)

            where_clause_params += [search_name]*4  # for email / display_name, reference
            where_clause_params += [re.sub('[^a-zA-Z0-9\-\.]+', '', search_name) or None]  # for vat
            where_clause_params += [search_name]  # for order by
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)
            self.env.cr.execute(query, where_clause_params)
            return [row[0] for row in self.env.cr.fetchall()]

        return super(ResPartner, self)._name_search(name, args, operator=operator, limit=limit, name_get_uid=name_get_uid)