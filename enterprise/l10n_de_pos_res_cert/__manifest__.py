# -*- coding: utf-8 -*-

{
    'name': "Germany - Certification for Point of Sale of type restaurant",

    'summary': """
Germany TSS Regulation for restaurant
""",

    'description': """
This module brings the technical requirements for the new Germany regulation regarding the restaurant.
Install this if you are using the Point of Sale app with restaurant in Germany.
""",

    'category': 'Accounting/Localizations/Point of Sale',
    'version': '0.1',

    'depends': ['pos_restaurant', 'l10n_de_pos_cert'],
    'installable': True,
    'auto_install': True,

    'data': [
        'views/l10n_de_pos_res_cert_templates.xml',
    ],
    'license': 'OEEL-1',
}
