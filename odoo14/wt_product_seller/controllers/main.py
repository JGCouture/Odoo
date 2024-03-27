from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request


class WebsiteSale(WebsiteSale):

    @http.route(['/get/share/cart'], type='json', auth="public", methods=['POST'] , website=True)
    def get_share_cart_url(self, so_id):
        order_id = request.env['sale.order'].sudo().search([('id', '=', int(so_id))])
        if order_id:
            url = False
            return_url = False
            if order_id.website_id and order_id.website_id.domain:
                url = order_id.website_id.domain +'/shop/cart/?ref='+order_id.name[2:]
                return_url = order_id.website_id.domain +'/shop'
            else:
                base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                url = base_url+'/shop/cart/?ref='+order_id.name[2:]
                return_url = base_url + '/shop'
            if url:
                request.session['sale_order_id'] = False
                return {'base_url': return_url, 'url': url}
        else:
            return False

    @http.route(['/get/share/quote/'], type='json', auth="public", methods=['POST'] , website=True)
    def send_quotation_agent(self, so_id):
        order_id = request.env['sale.order'].sudo().search([('id', '=', int(so_id))])
        order_id.sudo()
        if order_id and order_id.sale_order_template_id:
            template = order_id.sudo().sale_order_template_id.with_context(lang=order_id.partner_id.lang)
            order_id.sudo().website_description = template.website_description
            # order_id.onchange_sale_order_template_id()

            template_id = order_id.sudo()._find_mail_template()
            lang = request.env.context.get('lang')
            template = request.env['mail.template'].sudo().browse(template_id)
            if template.lang:
                lang = template._render_lang(order_id.ids)[order_id.id]
            ctx = {
                'model': 'sale.order',
                'res_id': order_id.ids[0],
                'template_id': template_id,
                'composition_mode': 'comment',
            }
            mail_compose_id = request.env['mail.compose.message'].sudo().with_context(
                mark_so_as_sent=True,
                custom_layout="mail.mail_notification_paynow",
                proforma=False,
                force_email=True,
                model_description=order_id.with_context(lang=lang).type_name,
                use_template=bool(template_id)
            ).create(ctx)
            mail_compose_id.sudo().onchange_template_id_wrapper()
            mail_compose_id.sudo().action_send_mail()
            url = False
            return_url = False
            if order_id.website_id and order_id.website_id.domain:
                url = order_id.website_id.domain +'/shop/cart/?ref='+order_id.name[2:]
                return_url = order_id.website_id.domain +'/shop'
            else:
                base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                url = base_url+'/shop/cart/?ref='+order_id.name[2:]
                return_url = base_url + '/shop'
            if url:
                request.session['sale_order_id'] = False
                return {'base_url': return_url, 'url': url}
        else:
            return False

    @http.route(['/share/cart/email'], type='json', auth="public", methods=['POST'] , website=True)
    def email_share_cart(self, so_id):
        order_id = request.env['sale.order'].sudo().search([('id', '=', int(so_id))])
        if order_id:
            url = False
            return_url = False
            if order_id.website_id and order_id.website_id.domain:
                url = order_id.website_id.domain +'/shop/cart/?ref='+order_id.name[2:]
                return_url = order_id.website_id.domain +'/shop'
            else:
                base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                url = base_url+'/shop/cart/?ref='+order_id.name[2:]
                return_url = base_url + '/shop'
            if url:
                mail_template_id = request.env.ref('wt_product_seller.mail_template_share_cart').sudo()
                mail_template_id.with_context(share_url=url).sudo().send_mail(order_id.id, force_send=True)
                request.session['sale_order_id'] = False
                return {'base_url': return_url, 'url': url}
        else:
            return False

    @http.route(['/web/agent/customer/'], type='json', auth="public", methods=['POST'] , website=True)
    def seller_customer_create(self, customer_data):
        parent_id = request.env['res.partner'].sudo().create(customer_data.get('billing'))
        parent_id.x_studio_agent = request.env.user.seller_employee_id.id if request.env.user.seller_employee_id else False
        if customer_data and customer_data.get('shipping'):
            shipping_id = request.env['res.partner'].sudo().create(customer_data.get('shipping'))
            shipping_id.parent_id = parent_id.id
        if parent_id:
            return True

    @http.route(['/web/agent/customer/update'], type='json', auth="public", methods=['POST'], website=True)
    def seller_customer_update(self, customer_data):
        parent_id = request.website.sale_get_order().seller_partner_id
        parent_id.sudo().write(customer_data.get('billing'))
        parent_id.x_studio_agent = request.env.user.seller_employee_id.id if request.env.user.seller_employee_id else False
        if customer_data and customer_data.get('shipping') and len(parent_id.child_ids) > 0:
            shipping_id = parent_id.child_ids[0].sudo().write(customer_data.get('shipping'))
        if parent_id:
            return True

    @http.route('/get_customer', type='json', auth='public', website=True)
    def get_customer(self, customer):
        request.session['website_sale_current_pl'] = None
        sale_order_id = request.website.sale_get_order(force_create=True)
        sale_order_id.sudo().update({
            'seller_partner_id': customer,
            'is_seller': True,
            'x_studio_many2one_field_8mpil': request.env.user.seller_employee_id.id if request.env.user.seller_employee_id else False,
            'find_ref': 'agent'
        })
        return True

    @http.route(['/shop/confirmation'], type='http', auth="public", website=True, sitemap=False)
    def payment_confirmation(self, **post):
        res = super(WebsiteSale, self).payment_confirmation(**post)
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            if order.is_seller == True:
                order.sudo().update({
                    'user_id': request.env.user.id,
                    'partner_id': order.seller_partner_id.id,
                    })
                order.sudo().onchange_partner_id() 
        return res

    @http.route('/customer/order/history', type='json', auth='public', website=True)
    def customer_order_history(self, customer=False, product=False):
        value = {}
        if product:
            product = request.env['product.product'].browse(product)

            order_lines = request.env['sale.order.line'].sudo().search([]).filtered(lambda s: s.order_id.partner_id.id == int(customer) and  s.order_id.state not in ['draft', 'cancel'] and s.product_id.id == int(product.id))
            value['product_order_history'] = request.env['ir.ui.view']._render_template("wt_product_seller.product_order_history", {
                'order_lines': order_lines,
                'sel_product': product,
            })
            return value

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        partner_id = request.env.user.partner_id.id if not request.website.is_public_user() else False
        flag = True
        recent_products = []
        if request.env.user.is_seller:
            order = request.website.sale_get_order()
            if order and order.seller_partner_id:
                if order.seller_partner_id.property_product_pricelist:
                    request.session['website_sale_current_pl'] = order.seller_partner_id.property_product_pricelist.id
                    pr_id = request.session.get('website_sale_current_pl')
                    request.website.sale_get_order(force_pricelist=pr_id or False)
                partner_id = order.seller_partner_id.id
            else:
                flag = False

        res = super(WebsiteSale, self).shop(page, category, search, ppg, **post)
        return res
