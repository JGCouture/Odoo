# -*- coding: utf-8 -*-

from odoo import api, models, fields,_
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    login_password = fields.Char(string="Portal Login Password")
    is_portal_user = fields.Boolean(string="Is Portal User", compute="check_portal_user")
    user_pass = fields.Char()
    user_created_manually = fields.Boolean(string="User Created Manually.")

    def set_user_details(self):
        self.user_pass = False
        user_id = self.env['res.users'].sudo().search([('partner_id', '=', self.id)])
        if user_id:
            self.user_pass = user_id.password

    def write(self, vals):
        if 'login_password' in vals:
            vals['user_pass'] = vals.get('login_password')
        res = super(ResPartner, self).write(vals)
        if 'login_password' in vals and self.user_created_manually:
            user_id = self.env['res.users'].sudo().search([('partner_id', '=', self.id)])
            if user_id and not vals.get('login_password'):
                raise ValidationError('Portal user already exists for this customer. you cannot set password empty.')
            if user_id and vals.get('login_password'):
                wizard_id = self.env['change.password.wizard'].sudo().create({
                    'user_ids': [(0, 0, {
                        'user_id': user_id.id,
                        'user_login': user_id.login,
                        'new_passwd': vals.get('login_password')
                    })]
                })
                wizard_id.change_password_button()
        return res

    def check_portal_user(self):
        self.is_portal_user = False
        user_id = self.env['res.users'].sudo().search([('partner_id', '=', self.id)])
        if user_id:
            self.is_portal_user = True

    def send_credentials(self):
        template = self.env.ref('zbs_contact_validation.send_login_credential_by_email')
        template.send_mail(self.id, force_send=True)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def create_portal_user(self):
        if not self.login_password:
            raise ValidationError('Please enter login password.')
        if not self.email:
            raise ValidationError('Email address required for portal users.')
        portal_wizard_id = self.env['portal.wizard'].sudo().with_context(from_custom_user=True).create({
            'user_ids': [(0, 0, {
                'partner_id': self.id,
                'email': self.email,
                'in_portal': True,
                'user_id': False
            })]
        })
        portal_wizard_id.action_apply()
        user_id = self.env['res.users'].search([('partner_id', '=', self.id)])
        self.user_created_manually = True
        if user_id:
            wizard_id = self.env['change.password.wizard'].sudo().create({
                'user_ids': [(0, 0, {
                    'user_id': user_id.id,
                    'user_login': user_id.login,
                    'new_passwd': self.login_password
                })]
            })
            wizard_id.change_password_button()

    def get_login_credentials(self):
        user_id = self.env['res.users'].search([('partner_id', '=', self.id)], limit=1)
        if user_id:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            return {'login': user_id.login, 'password': self.user_pass, 'url': base_url}
        return {'login': '', 'password': '', 'url': ''}

    @api.constrains('phone')
    def check_contact_phone(self):
        website_id = self._context.get('website_id', False)
        for rec in self.filtered(lambda l: l.phone and not website_id):
            partner_id = self.search([('phone','=',rec.phone),('id','!=', rec.id)])
            if partner_id:
                raise ValidationError(_('Contact already exist with the same phone number.'))