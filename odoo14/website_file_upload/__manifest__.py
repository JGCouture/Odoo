# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Website File Upload",
  "summary"              :  """The module allows the website customer to upload a file with his/her website order. The file can contain a request, customisation or suggestion for the seller.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-File-Upload.html",
  "description"          :  """Odoo Website File Upload
Customer order suggestion
Website Order note
Order customization
Customer order customization""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_file_upload",
  "depends"              :  ['website_sale','base', 'website_terms_and_condition'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'view/sale_order_inherit_view.xml',
                             'view/templates.xml',
                             'view/product.xml',
                             # 'view/payment_template.xml'
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
}