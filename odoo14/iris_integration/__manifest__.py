# -*- coding: utf-8 -*-
{
    'name': "IRIS Integration",

    'summary': """
       IRIS Integration
       """,

    'description': """
        IRIS Integration
    """,

    'author': "BistaSolutions",
    'website': "http://www.bistasolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '2.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'project', 'delivery', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/res_config_settings_views.xml',
        'views/canceled_order_view.xml',
        'views/iris_integration_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
