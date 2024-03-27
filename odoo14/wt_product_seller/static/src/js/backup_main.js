odoo.define('wt_product_seller.customer', function (require) {
'use strict';
var session = require('web.session');
var core = require('web.core');
var publicWidget = require('web.public.widget');
var Dialog = require('web.Dialog');
var _t = core._t;

    publicWidget.registry.websiteproductAddtoCart = publicWidget.Widget.extend({
        selector: '.js_sale',
        events: {
            "click .oe_product_cart": "_onAddtoCartClick",
            "change select[name='customer']": "on_change_customer"
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments);
        },
        on_change_customer: function(ev){
            var customer_id = parseInt($(ev.currentTarget).val());
            this._rpc({
                        route: '/get_customer',
                        params: {
                            'customer': customer_id,
                        },
                    }).then(function(result) {
                        window.location.reload();
                    });
        },
        _onAddtoCartClick: function (ev) {

            var url = window.location.href.split('/')
            console.log('USER     ', session.user_id)
            if (session.user_id.is_saller != True) {
                var get_customer =  $("#customer").val()
                if (!get_customer){
                    var content = $('<div>').html(_t('<p>please select customer, for whom you want to purchase product!<p/>') );
                    new Dialog(self, {
                        title: _t('Warning!'),
                        size: 'medium',
                        $content: content,
                        buttons: [
                        {text: _t('Ok'), close: true}]
                    }).open();
                    ev.stopImmediatePropagation();
                    return false;
                }
                else{
                    this._rpc({
                        route: '/get_customer',
                        params: {
                            'customer': get_customer,
                        },
                    }).then(function(result) {
                        window.reload();
                    });
                }
            }
        },

    });
});
