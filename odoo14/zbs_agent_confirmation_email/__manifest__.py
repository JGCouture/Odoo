# -*- coding: utf-8 -*-

{
    'name': 'ZBS Agent Confirmation Email',
    'version': '1.0',
    'summary': """This module send email to the agent on sale order confirmation.
""",
    'author': 'Anil(anil.patel13688@gmail.com)',
    'company': 'Avision Infosoft',
    'depends': ['base', 'sale', 'hr', 'project'],
    'data': [
        'data/mail_template.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
}