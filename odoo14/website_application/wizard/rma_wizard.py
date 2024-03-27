# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import logging
import requests
import json

_logger = logging.getLogger(__name__)


class rma_wizard(models.TransientModel):
    _inherit = 'rma.wizard'

    ticket = fields.Char('Ticket Id')

    @api.model
    def create_method(self):
        rma = super(rma_wizard, self).create_method()
        if self.ticket:
            rma.write({'ticket': self.ticket})
        else:
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json'}
            IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
            headers.update({'X-API-KEY': IRIS_API_KEY})
            iris_ticket_url = "https://zbs.iriscrm.com/api/v1/helpdesk"
            iris_ticket_data = {
                "type": 182,
                "subject": 'Odoo: RMA',
                "priority": 0,
                "group_id": 0,
                "assignType": "lead",
                "assignTo": str(self.wk_order_id.partner_id.x_studio_lead_id),
            }

            if "camera" in self.name.name.lower():
                iris_ticket_data.update({'type': 179})
            elif "computer" in self.name.name.lower():
                iris_ticket_data.update({'type': 182})
            elif "terminal" in self.name.name.lower():
                iris_ticket_data.update({'type': 180})
            elif "printer" in self.name.name.lower():
                iris_ticket_data.update({'type': 181})
            else:
                iris_ticket_data.update({'type': 242})
            response = requests.post(iris_ticket_url, data=json.dumps(iris_ticket_data), headers=headers)
            if response.status_code == 200:
                _logger.info("Create ticket response : %s ", json.loads(response.text))

                ticket_data = json.loads(response.text)
                ticket_id = ticket_data['general']['id']
                rma.write({'ticket': ticket_id})
        return rma

