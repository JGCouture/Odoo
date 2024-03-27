# -*- coding: utf-8 -*-
{
    "name": "Stop Auto Add Lot| Stop Auto Add Serial",
    "author": "",
    "support": "support@softhealer.com",
    "website": "https://www.softhealer.com",
    "category": "Warehouse",
    "license": "OPL-1",
    "summary": "Stop Auto Add Lots,Stop Auto Add Serials,Stop Automatic Add Lot In Delivery Order,Stop Automatic Add Serial,Restrict Auto Add Lot In Outgoing Order,Restrict Auto Add Serial,Stop Auto Create Lot,Stop Auto Create Serial,Manage Lot,Manage Serial Odoo",
    "description": """Do you want to avoid auto-selection lot/serial on a product? This module helps to stop the automatic allocation of the lot/serial in the delivery order. So you can select lot/serial manually for the delivery order based on the requirement.""",
    "version": "14.0.1",
    "depends": [
        'sale_management',
        'stock',
    ],
    "data": [
        'views/res_config_setting.xml',
        'views/stock_move_line.xml'
    ],
    "images": ['static/description/background.png', ],
    "auto_install": False,
    "application": True,
    "installable": True,
    "price": "25",
    "currency": "EUR"
}
