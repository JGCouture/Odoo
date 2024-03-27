# -*- coding: utf-8 -*-
{
    'name': "ai_website_customizations",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'author': "",
    'version': '20.0',
    'depends': ['base','sale','website_sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/sale_order.xml',
        'report/invoice.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
