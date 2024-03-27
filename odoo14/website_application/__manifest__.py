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
    'name': 'Website Application',
    'version': '1.6',
    'category': 'Website',
    'summary': 'Website Application',
    'description': '''
    ''',
    'author': 'Sneha Vora - Warlock Technologies Pvt Ltd.',
    'website': 'http://warlocktechnologies.com',
    'support': 'support@warlocktechnologies.com',
    'depends': ['sale_management', 'sale', 'purchase', 'stock', 'website', 'website_sale', 'rma', 'base_automation'],
    "data": [
        "security/form_security_view.xml",
        "security/ir.model.access.csv",
        "report/report.xml",
        "report/report_ach.xml",
        "report/report_template.xml",
        "report/report_online_order.xml",
        "report/report_new_merchant.xml",
        "views/website_application_form_template.xml",
        "views/merchant_template.xml",
        "views/kwickpos_online_order_template.xml",
        "views/rma_form_template.xml",
        "views/saas_ach_authorization_template.xml",
        "views/menu.xml",
        "action/automated_action.xml",
        "views/assets.xml",
        "views/mail_template_data.xml",
        "views/mail_template_rebate.xml",
        "views/mail_template_rebate_to_sales.xml",
        "views/mail_template_questionnaire.xml",
        "views/mail_template_rma_approve.xml",
        "views/mail_template_rma_reject.xml",
        "views/mail_template_rma.xml",
        "views/mail_template_online_order_form_to_agent.xml",
        "views/mail_template_new_merchant_to_agent.xml",
        "views/mail_template_ach.xml",
        "views/rma_view.xml",
        "data/sequence.xml",
        "data/sequence.xml",
        "wizard/rma_wizard_view.xml"
        ],
    'images': ['static/images/screen.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
    'external_dependencies': {
    },
}
