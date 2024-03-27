# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    "name": "website_product_seller",
    "version": "1.3",
    "category": "website",
    "summary": "website ",
    "description": """
        webiste product sale by salesperson to any user.
    """,
    "author": "Warlock Technologies Pvt Ltd.",
    "website": "http://warlocktechnologies.com",
    "support": "info@warlocktechnologies.com",
    "depends": ['base', 'sale', 'website', 'website_sale', 'website_sale_wishlist', 'website_sale_stock', 'payment', 'hr'],
    "data": [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        "views/sale_order_view.xml",
        "views/template.xml",
        "views/assets.xml",
        "views/res_users_view.xml",
        "views/order_history_template.xml",
    ],
    "images": [],
    "license": "OPL-1",
    "installable": True,
}
