# -*- coding: utf-8 -*-

{
    'name': 'ZBS Agent Commission Report',
    'version': '1.2',
    'summary': """This add the xlsx report for agent commission.
""",
    'author': 'Anil(anil.patel13688@gmail.com)',
    'company': 'Avision Infosoft',
    'depends': ['base', 'sale', 'hr', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'view/hr_employee.xml',
        'view/product_product.xml',
        'view/sale_order.xml',
        'wizard/agent_commission_report.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
