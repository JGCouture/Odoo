# -*- encoding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2020 (http://www.bistasolutions.com)
#
##############################################################################

{
    'name': 'Sale Auto-Invoice from Task',
    'version': '14.0.0.1',
    'summary': 'Create Auto Invoice From Task',
    'description': """
Sale Order - Create Automatic Invoice while Change task state

    """,
    'website': 'https://www.bistasolutions.com',
    'author': 'Bista Solutions Pvt.Ltd',
    'depends': ['project', 'sale_project', 'account'],
    'category': 'Accounting',
    'data': [
        'security/ir.model.access.csv',
        'wizard/submit_task_view.xml',
        'views/project_views.xml'
    ],
    'installable': True,
    'application':False,
}
