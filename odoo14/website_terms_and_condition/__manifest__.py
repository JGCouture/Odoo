#    Author: Sneha Vora(<https://www.warlocktechnologies.com/>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Website Terms & Conditions_report',
    'version': '1.6',
    'category': 'Website',
    'summary': 'this odoo app restrict the payment untill the customer accept terms and conditions.',
    'description': '''
    ''',
    'author': 'Sneha Vora - Warlock Technologies Pvt Ltd.',
    'website': 'http://warlocktechnologies.com',
    'support': 'support@warlocktechnologies.com',
    'depends': ['sale_management', 'sale', 'purchase', 'stock', 'website','auth_signup', 'zbs_order_status','website_application'],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/website.xml",
        "views/online_order.xml",
        "views/address_template.xml",
        "views/signup_template.xml",
        "views/product_template.xml",
        "report/report.xml",
        "report/order_report.xml",
        # "report/report_update.xml",
        'views/confirmation_template.xml',
        'views/sale.xml',
        'views/res_partner.xml',
        'views/term_template.xml'
        ],
    'images': ['static/images/screen.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
    'external_dependencies': {
    },
}
