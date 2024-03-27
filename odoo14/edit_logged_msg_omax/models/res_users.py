# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models



class res_company_inherit(models.Model):
    _inherit = 'res.users'

    def action_user_edit_message(self, user_id=False, message_id=False):
        if user_id and message_id:
            message_id = self.env['mail.message'].sudo().browse(message_id)
            message_type = message_id.message_type
            model_name = message_id.model
            if message_type == 'comment' or model_name == 'sale.order' or 'project.task':
                access_dict = {}
                res_user = self.env['res.users'].sudo().browse(user_id)
                group_message_editor_for_own = self.env.user.has_group('edit_logged_msg_omax.group_message_editor_for_own')
                group_message_editor_for_all = self.env.user.has_group('edit_logged_msg_omax.group_message_editor_for_all')
                mail_history_len = len(message_id.mail_message_history_line)
                message_owner_id = message_id.create_uid.id
                current_user_id = self.env.user.id
                if group_message_editor_for_own == True and group_message_editor_for_all == False and message_owner_id == current_user_id:
                    access_dict.update({'history':mail_history_len, 'edit':group_message_editor_for_own})
                elif group_message_editor_for_own == True and group_message_editor_for_all == True:
                    access_dict.update({'history':mail_history_len, 'edit':group_message_editor_for_own})
                else:
                    pass
                group_message_deletor_for_own = self.env.user.has_group('edit_logged_msg_omax.group_message_deletor_for_own')
                group_message_deletor_for_all = self.env.user.has_group('edit_logged_msg_omax.group_message_deletor_for_all')
                if group_message_deletor_for_own == True and group_message_deletor_for_all == False and message_owner_id == current_user_id:
                    access_dict.update({'deletor':group_message_deletor_for_own})
                elif group_message_deletor_for_own == True and group_message_deletor_for_all == True:
                    access_dict.update({'deletor':group_message_deletor_for_own})
                else:
                    pass
                if access_dict:
                    return access_dict
                else:
                    return False
            else:
                return False
            
    def action_user_edit_message_view(self, user_id=False):
        if user_id:
            custom_view_id = self.env.ref("edit_logged_msg_omax.custom_message_form")
            res = { 
                    'custom_view_id' : custom_view_id.id,
                    }
            return res
            
    def action_user_delete_message(self,message_id=False):
        if message_id:
            message = self.env['mail.message'].sudo().browse(message_id).unlink()
            return True
