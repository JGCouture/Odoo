# -*- coding: utf-8 -*-
import requests
import json
import logging
import sys
import traceback
import time # Import whole time module

from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)

NAME_TO_IRIS_USER_ID = {
'AARON FENG': 115,
'AKIRA ISHIKAWA': 46,
'ALAN LEONG': 47,
'ALFIE HU': 367,
'ALLEN HE': 218,
'AMY LI': 49,
'AMY LIANG': 316,
'ANDREW XU': 286,
'ANDY BAZAR': 165,
'ANDY LAM': 97,
'ANGELA DONG': 50,
'ANNY CHEN': 225,
'ASHLEY ZBS': 118,
'AVENA WU': 348,
'BAOLONG TAN': 302,
'BEN BURKIN': 52,
'BEN LIU': 53,
'BENJAMIN BROWN': 342,
'BILLY PAN': 226,
'BIN CHEN': 207,
'BINBIN SHAO': 394,
'BING FENG CHEN': 321,
'BRENT VANDE VELDE': 250,
'CANDY HE': 392,
'CHANGWEI CHEN': 197,
'CHAO QIN': 138,
'CHAOXIAN GUO': 279,
'CHRIS MUI': 56,
'CINDY LAM': 57,
'CINDY QIN': 31,
'COMMI TONG': 58,
'DAVID LI': 59,
'DEVEN ZHAO': 213,
'DIEP LY': 355,
'DONG LIU': 133,
'EDWARD FORD-BALL': 112,
'ELINA WU': 73,
'ELLA HUANG': 396,
'EMILY OU YANG': 300,
'ENSON SHI': 63,
'ERICK PARRA': 147,
'ERIN ZHOU': 307,
'ESTHER SUEN': 303,
'ETHAN ZHOU': 272,
'EVA ZHANG': 389,
'FAISAL AZAD': 219,
'FAN WANG': 269,
'FAT HONG YANG': 203,
'FENG LIN': 315,
'FLORA LIU': 185,
'FRANCISCO WANG': 221,
'FRANK WANG': 34,
'FUZHOU REPORTING': 319,
'GAN GUO': 64,
'GARY CHEN': 340,
'GARY LIU': 65,
'GDC POS': 66,
'GEOFG HUANG': 314,
'GORDON LEE': 331,
'GREGORY WYMAN': 242,
'GUANG ZHAO': 354,
'GUOTAI LI': 323,
'HAI LI': 136,
'HANK TAN': 69,
'HARRIS CHEN': 229,
'HAWAII LIN': 70,
'HELEN HUANG': 395,
'HOWARD WANG': 71,
'HOWIE YU': 374,
'JACK SUN': 107,
'JACK ZHAO': 290,
'JACKY LI': 129,
'JASMINE ZHENG': 293,
'JASON HAN': 72,
'JAY LU': 154,
'JCH DESIGN': 116,
'JEFF LIM': 36,
'JEFFERY PAN': 232,
'JENNY XIAO': 45,
'JI LE NI': 184,
'JIANDONG WU': 222,
'JIANHUA': 74,
'JIANHUA CHEN': 152,
'JIARUI CHEN': 259,
'JING LI': 121,
'JING LIN': 170,
'JOBS CHEN': 376,
'JOE ARCE': 360,
'JOE JAIME': 255,
'JOE OU': 343,
'JOHN SZETO': 339,
'JOHNNY NGUYEN': 361,
'JOI CHEN': 311,
'JOJO ZHAO': 169,
'JUAN SOTO': 156,
'JUDY YANG': 240,
'JUSTIN YANG': 362,
'KAI LEE': 75,
'KEMAL OZKANCA': 267,
'KEN LIN': 76,
'KEN ZHENG': 227,
'KENSOU CHEN': 273,
'KEVIN DIN': 77,
'KEVIN SHI': 190,
'KEVIN ZHAO': 19,
'KEZHU CHEN': 345,
'KIA GEMUENDEN': 324,
'KIM WANG': 353,
'KIMI JIN': 351,
'KIMMY ZHENG WANG': 189,
'KRIS KAO': 371,
'KRISTY TANG': 281,
'KWICK POS': 68,
'LANXIN XU': 215,
'LIAN DEABREU': 358,
'LILY ZHENG': 385,
'LINA LIN': 366,
'LINDA CHEN': 356,
'LING YANG': 205,
'LISA HUANG': 22,
'LISA LI': 174,
'LISA WANG': 79,
'LIZHI JIANG': 375,
'LIZHI LIN': 264,
'LONG YANG': 164,
'LUCY LIU': 145,
'LYNN YEOH': 329,
'MARIO LU': 142,
'MARK BROWN': 198,
'MARK KEARNEY': 372,
'MARK WANG': 80,
'MARTIN WONG': 83,
'MAX LI': 214,
'MENG ZHEN WANG': 175,
'MHADY SHIHADEH': 378,
'MIA WU': 297,
'MIKE LIN': 84,
'MIKEY LU': 391,
'MIN LIN ZHANG': 146,
'MING YE': 128,
'MING YING ZHANG': 258,
'MINGQUAN ZHANG': 327,
'MOUSSA YE': 338,
'MYLES BALL': 317,
'NANCY LAN': 38,
'NETCOM PAYSYSTEM': 249,
'NHU HUYNH': 330,
'ODOO BOT': 390,
'OLIVIA WANG': 276,
'OMAR RIVERA': 301,
'PINKY CHEUNG': 85,
'QIAO ZHENG': 253,
'QING HUI WU': 274,
'QING LIN': 199,
'QINGDU ZHENG': 196,
'QIULAN HUANG': 357,
'RACHEL EVE': 202,
'REMY CHEN': 236,
'RENA LIN': 334,
'RICHARD LIN': 150,
'RICKY ZHOU': 88,
'ROMY YE': 304,
'RONALD LENG': 383,
'RONG YU': 379,
'SABRINA YOU': 134,
'SAFIA ARIF': 308,
'SAIHERA CHEN': 359,
'SAIT ONAL': 257,
'SALLY JIANG': 111,
'SAM HUANG': 91,
'SAM LIU': 180,
'SAM LUO': 89,
'SAMMI YANG': 310,
'SARA SU': 364,
'SASA LIU': 280,
'SELINA WU': 230,
'SHAN CHENG': 344,
'SHAOZHOU JIANG': 245,
'SHU YING JIANG': 155,
'SHUAI JIN': 191,
'SOR TAN': 110,
'STACY LIANG': 187,
'STEVEN CALKINS': 95,
'SU KUEI LEE': 393,
'SUNNY LIN': 96,
'SYNOPAY INC': 208,
'SZE LAM CHENG': 168,
'TAM WENG': 42,
'TAMMIE CHEN': 157,
'TERRY ZHENG': 349,
'TIAN LONG LI': 151,
'TIAN WU': 326,
'TIFFANY QIAN': 87,
'TOM JIN': 341,
'TONY CHENG': 143,
'TONY HUANG': 397,
'TRENTON STINSON': 211,
'TRUONG THINH THIEM': 384,
'VICKI NI': 398,
'VICTOR SHING WONG': 217,
'VINCENT': 192,
'VIVIAN YAN': 178,
'WANZHEN YANG': 193,
'WEI LIN': 209,
'WENLI XIONG': 212,
'WILL YANG': 282,
'WILSON HUANG': 181,
'WING CHENG': 381,
'WINNIE WANG': 179,
'WINNIE ZHENG': 237,
'WINSTON WANG': 161,
'WISDOM ZHANG': 291,
'XIA LIN': 135,
'XIAO YI ZHANG': 328,
'XINBO LI': 149,
'XING ZHEN': 98,
'XUEYING WANG': 99,
'YI CHEN': 312,
'YINGTONG GAN': 183,
'YONG LUO': 100,
'YOUNG ZHAO': 235,
'YUAN LIN': 254,
'YUAN ZHE': 101,
'YUEJUN JIANG': 102,
'YUEN KWOK': 318,
'YUN PAN': 387,
'YUNMING HE': 233,
'YUZHEN RUAN': 268,
'ZACK HUANG': 103,
'ZBS POS': 104,
'ZEHONG CHEN': 177,
'ZHONG INC': 105,
'ZI ZHI ZHU': 106
}


US_STATE_DICT = {
'AL': 9,
'AK': 10,
'AZ': 11,
'AR': 12,
'CA': 13,
'CO': 14,
'CT': 15,
'DE': 16,
'DC': 17,
'FL': 18,
'GA': 19,
'HI': 20,
'ID': 21,
'IL': 22,
'IN': 23,
'IA': 24,
'KS': 25,
'KY': 26,
'LA': 27,
'ME': 28,
'MT': 29,
'NE': 30,
'NV': 31,
'NH': 32,
'NJ': 33,
'NM': 34,
'NY': 35,
'NC': 36,
'ND': 37,
'OH': 38,
'OK': 39,
'OR': 40,
'MD': 41,
'MA': 42,
'MI': 43,
'MN': 44,
'MS': 45,
'MO': 46,
'PA': 47,
'RI': 48,
'SC': 49,
'SD': 50,
'TN': 51,
'TX': 52,
'UT': 53,
'VT': 54,
'VA': 55,
'WA': 56,
'WV': 57,
'WI': 58,
'WY': 59,
'FM': 61,
'GU': 62,
'PW': 65,
'PR': 66,
'VI': 67
}


class ResPartner(models.Model):
    _inherit = "res.partner"

    merchant_id = fields.Char(string='Merchant Id', tracking=True)
    iris_lead_link = fields.Char(string='Iris lead link', compute='compute_iris_link_using_lead_id')
    x_studio_lead_id = fields.Char(string='X Studio Lead', tracking=True)
    mobile = fields.Char(string='Mobile', tracking=True)
    street = fields.Char(string='Street', tracking=True)
    street2 = fields.Char(string='Street2', tracking=True)
    city = fields.Char(string='City', tracking=True)
    state_id = fields.Many2one('res.country.state', string='State', tracking=True, ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', tracking=True, ondelete='restrict')
    find_ref = fields.Selection([
        ('agent', 'Agent'),
        ('referral', 'Referral'),
        ('online_ad', 'Online Ads')
    ], string="How did you find us?", tracking=True)
    online_add = fields.Selection([
        ('wechat', 'WeChat'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('other', 'Other')
    ], string="Find By", tracking=True)

    def compute_iris_link_using_lead_id(self):
        for obj in self:
            if obj.x_studio_lead_id:
                obj.write({'iris_lead_link':'https://crm.zbspos.com/lead/view/' + str(obj.x_studio_lead_id) })
            else:
                obj.write({'iris_lead_link': False})

    def create_iris_link_using_lead_id(self):
        partners = self.env['res.partner'].search([])
        for partner in partners:
            if partner.x_studio_lead_id and partner.x_studio_lead_id != "0001":
                partner.sudo().write(
                        {'iris_lead_link': 'https://crm.zbspos.com/lead/view/'  + partner.x_studio_lead_id})

    def fetch_lead_id_from_iris_periodically(self):

        lead_url = "https://zbs.iriscrm.com/api/v1/leads"
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
        headers.update({'X-API-KEY': IRIS_API_KEY})
        contacts = self.env['res.partner'].search([('id', '=',20453)])
        phone = ''
        for contact in contacts:
            if contact.phone and not contact.iris_lead_link :
                if contact.phone[0] == '+':
                    phone = contact.phone[3:]
                else:
                    phone = contact.phone
                param = {
                    'fields[9]': phone
                }
                response = requests.get(lead_url, headers=headers, params=param)

                ticket_data = json.loads(response.text)
                if len(ticket_data['data']) > 0:
                    lead_id = ticket_data['data'][0]['id']
                    contact.sudo().write({'iris_lead_link': 'https://zbs.iriscrm.com/lead/view/' + str(lead_id)})
                    contact.sudo().write({'x_studio_lead_id': str(lead_id)})
                time.sleep(0.4)

    def syn_lead_to_contact_from_iris_periodically(self):

        lead_url = "https://zbs.iriscrm.com/api/v1/leads"
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        IRIS_API_KEY = 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'
        headers.update({'X-API-KEY': IRIS_API_KEY})
        param = {
            'per_page': 10,
            'sort_dir': 'desc',
            'sort_by': 'modified'
        }
        response = requests.get(lead_url, headers=headers, params=param)
        if response.status_code == 200:
            ticket_data = json.loads(response.text)
            for lead in ticket_data['data']:
                lead_info_response = requests.get(lead_url + '/' + str(lead['id']), headers=headers)
                if lead_info_response.status_code == 200:
                    lead_info_response_data = json.loads(lead_info_response.text)
                    business_phone = lead_info_response_data['details'][0]['fields'][13]['value']
                    dba = lead_info_response_data['details'][0]['fields'][0]['value']
                    merchant_id = lead_info_response_data['details'][0]['fields'][2]['value']
                    email = lead_info_response_data['details'][0]['fields'][17]['value']
                    street = lead_info_response_data['details'][0]['fields'][9]['value']
                    city = lead_info_response_data['details'][0]['fields'][10]['value']
                    state = US_STATE_DICT.get(lead_info_response_data['details'][0]['fields'][11]['value'], False)
                    zip = lead_info_response_data['details'][0]['fields'][12]['value']
                    contact = self.env['res.partner'].search(['|', ('phone', '=', '+1 ' + str(business_phone)), ('x_studio_lead_id', '=', str(lead['id'])) ])
                    try:
                        if contact:
                            contact.write({
                                'x_studio_lead_id': str(lead['id']),
                                'merchant_id': merchant_id,
                                'name': business_phone + ' - ' + dba,
                                'street': street,
                                'city': city,
                                'state_id': state,
                                'zip': zip
                            })
                        else:
                            self.env['res.partner'].create({
                                'x_studio_lead_id': str(lead['id']),
                                'iris_lead_link': 'https://crm.zbspos.com/lead/view/' + str(lead['id']),
                                'name': business_phone + ' - ' + dba,
                                'email': email,
                                'street': street,
                                'city': city,
                                'state_id': state,
                                'zip': zip,
                                'phone': '+1 ' + business_phone,
                                'merchant_id': merchant_id,
                            })
                    except Exception as e:
                        _logger.info("Syn lead failed, send reqeust " + e)

    def create_response_history(self, response, message):
        history_obj = self.env['iris.integration.history']
        history_obj.create({'partner_id': self.id,
                            'user_id': self.env.user.id,
                            'note': 'Sent the Contact to IRIS',
                            'response': response})
        self.message_post(body=message)

    def send_contact_to_iris(self):
        url = "https://zbs.iriscrm.com/api/v1/leads"

        fields = [
            {
                "id": 1,
                "value": self.name
            },
        ]

        if self.street:
            street = self.street
            if self.street2:
                street = street + ' ' + self.street2
            fields.append({
                "id": 4,
                "value": street})

        if self.city:
            fields.append({
                "id": 6,
                "value": self.city})

        if self.state_id:
            fields.append({
                "id": 7,
                "value": self.state_id.code})

        if self.zip:
            fields.append({
                "id": 8,
                "value": self.zip})

        if self.phone:
            fields.append({
                "id": 9,
                "value": str(self.phone).split(' ')[1]})

        if self.mobile:
            fields.append({
                "id": 10,
                "value": str(self.mobile).split(' ')[1]})
            fields.append({
                "id": 3784,
                "value": str(self.mobile).split(' ')[1]})

        if self.email:
            fields.append({
                "id": 12,
                "value": self.email})

        if self.x_studio_owner_name:
            fields.append({
                "id": 3777,
                "value": self.x_studio_owner_name})

        odoo_agent = self.x_studio_agent.name.upper()
        iris_agnet_id = NAME_TO_IRIS_USER_ID.get(odoo_agent, 390)

        data = {'campaign': 1, 'status': 28, 'source': 1, 'group': 1,
                'users': [iris_agnet_id], 'fields': fields}
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'X-API-KEY': 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'}
        _logger.info("== Data : %s ", json.dumps(data))
        response = requests.post(url, data=json.dumps(data), headers=headers)
        _logger.info("== response : %s ", json.loads(response.text))
        leadID = json.loads(response.text)['leadId']
        self.x_studio_lead_id = leadID
        message = 'Automation: Sent the Contact to IRIS and created Lead ' + str(
            leadID)
        self.create_response_history(response, message)

    def get_iris_lead_to_odoo(self, leadID):
        api = "https://zbs.iriscrm.com/api/v1/leads/"
        url = api + leadID
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'X-API-KEY': 'ZZTFHJJULdhlVuVz6amD6Vgt3yHLomgTWI7vy1jwfDwmDaXgWt'}

        try:
            response = requests.get(url, headers=headers)
            _logger.info("== response : %s ", json.loads(response.text))
            response.raise_for_status()
            fields = json.loads(response.text)['details'][0]['fields']
            state = fields[9]['value']
            state_id = US_STATE_DICT.get(state, 1)
            vals = {
                'name': fields[0]['value'],
                'street': fields[7]['value'],
                'city': fields[8]['value'],
                'state_id': state_id,
                'zip': fields[10]['value'],
                'phone': '+1 ' + fields[11]['value'],
                'mobile': '+1 ' + fields[12]['value'],
                'email': fields[15]['value'],
                'x_studio_owner_name': fields[5]['value'],
                'iris_lead_link': 'https://crm.zbspos.com/lead/view/' + str(leadID),
                'merchant_id': fields[2]['value']
            }
            self.write(vals)
            message = 'Automation: Sent the Contact to IRIS and created Lead ' + str(
                leadID)
            self.create_response_history(response, message)

        except requests.HTTPError as error:
            if error.response.status_code in (204, 404):
                _logger.exception("Bad request %s : %s !",
                                  error.response.status_code,
                                  error.response.content)
            else:
                _logger.exception("Bad request : %s !",
                                error.response.content)
            message = 'Request not send to  IRIS, Please check log. ' + str(
                leadID)
            self.create_response_history(json.loads(error.response.text), message)
        except Exception as er:
            _logger.exception("Bad request : %s !", er)
            ex_type, ex_value, ex_traceback = sys.exc_info()
            message = 'Request not send to  IRIS, Please check log. ' + str(
                leadID)
            trace_back = traceback.extract_tb(ex_traceback)
            stack_trace = []
            for trace in trace_back:
                stack_trace.append(
                    "Line : %d, Func.Name : %s, Message : %s" % (
                    trace[1], trace[2], trace[3]))
            stack_trace = '\n'.join(stack_trace)
            self.create_response_history(stack_trace, message)

    @api.model
    def create(self, vals):
        result = super(ResPartner, self).create(vals)
        if 'website_id' not in self._context and result.x_studio_lead_id:
            if result.x_studio_lead_id == '0':
                result.send_contact_to_iris()

        return result
