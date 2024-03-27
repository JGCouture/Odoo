odoo.define('wt_product_seller.customer', function (require) {
'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var Dialog = require('web.Dialog');
    var _t = core._t;

    publicWidget.registry.websiteproductAddtoCart = publicWidget.Widget.extend({
        selector: '.js_sale',
        events: {
            'click .oe_product_cart': '_onAddtoCartClick',
            'click .product_order_history': '_onOrderHistoryClick',
            "change select[name='customer']": "on_change_customer"
        },
        start: function () {
            var self = this;
            this.$('.js-example-basic-single').select2();
            this.$('.select2-choice').css({
                    "min-width": "185px",
                    "max-width": "185px",
                    "min-height": "35px",
                    "max-height": "35px",
                    "background": "none",
                    "padding-top": "4px"
                });
            return this._super.apply(this, arguments);
        },
        init: function () {
            this._super.apply(this, arguments);
            this._popoverRPC = null;
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
            if ($("#is_seller_customer").val() == 'True') {
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
            }
        },
        _onOrderHistoryClick: function (ev) {
            $(this.selector).not(ev.currentTarget).popover('hide');

            var get_customer =  $("#customer").val();
            var $product_id = $(ev.target).closest('form').find("input[name='product_id']");
            var product_id = parseInt($product_id.val(), 10);
            this._rpc({
                route: '/customer/order/history',
                params: {
                    'customer': get_customer,
                    'product': product_id,
                },
            }).then(function(result) {
                var value = result;
                $('.product_history_popup').html(result.product_order_history);
                $("#product_quick_views_popup").modal('show');

            });
        },
    });

    publicWidget.registry.WebsiteSale.include({
        events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events, {
            'click .add_to_cart_json_cl': 'add_to_cart_customer',
            'click #share_cart_link' : 'copy_share_cart_link',
            'click #share_cart_send_quote' : 'share_cart_sent_quote_email',
            'click #share_cart_email' : 'customer_share_cart_email',
            'click #web_create_customer': "create_web_customer",
            'click #web_update_customer': "update_web_customer",
            'change #use_diff_address' : 'change_billing_shipping',
            'change #use_diff_address_update' : 'change_billing_shipping_update',
        }),
        add_to_cart_customer:function(ev){
            if ($("#is_seller_customer").val() == 'True') {
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
            }
            var $input = $(ev.target).closest('form').find("input[name='add_qty']");
            var $product_id = $(ev.target).closest('form').find("input[name='product_id']");
            var value = parseInt($input.val() || 0, 10);
            var add_product_id = parseInt($product_id.val(), 10);
            this._rpc({
                route: "/shop/cart/update_json",
                params: {
                    product_id: add_product_id,
                    add_qty: value,
                },
            }).then(function (data) {
                var $q = $(".my_cart_quantity");
                if (data.cart_quantity) {
                    _.each($(".my_cart_quantity"), function(qn){
                        $(qn).text(data.cart_quantity);
                    });
                }
            });
        },
        copy_share_cart_link : function(ev){
            var so_id = $('#sale_order_id').val();
            if(so_id){
                ajax.jsonRpc("/get/share/cart/", 'call', {'so_id': so_id})
                .then(function (data){
                  if (data){
                    navigator.clipboard.writeText(data['url']);
                    alert('Share cart link copied to clipboard.');
//                    window.location.href = data['base_url'];
                    window.location.pathname = "/shop";
                  }
                  else{
                    alert('Something went wrong...');
                  }
                });
            }
        },

        share_cart_sent_quote_email : function(ev){
            var so_id = $('#sale_order_id').val();
            if(so_id){
                ajax.jsonRpc("/get/share/quote/", 'call', {'so_id': so_id})
                .then(function (data){
                  if (data){
                    navigator.clipboard.writeText(data['url']);
                    alert('Quotation send to the customer.');
//                    window.location.href = data['base_url'];
                    window.location.pathname = "/shop";
                  }
                  else{
                    alert('Something went wrong...');
                  }
                });
            }
        },

        customer_share_cart_email : function(ev){
            var so_id = $('#sale_order_id').val();
            if(so_id){
                ajax.jsonRpc("/share/cart/email/", 'call', {'so_id': so_id})
                .then(function (data){
                  if (data){
                    navigator.clipboard.writeText(data['url']);
                    alert('Share cart link copied to clipboard and email send to the customer.');
//                      window.location.href = data['base_url'];
                        window.location.pathname = "/shop";

                  }
                  else{
                    alert('Something went wrong...');
                  }
                });
            }
        },
        update_web_customer : function(ev){
            var billing_shipping = $('#use_diff_address_update').is(":checked");
            var lead_id = $('#billing_lead_id_update').val();

            //billing address
            var owner_billing = $('#x_studio_owner_name_billing_update').val();
            var customer_name = $('#customer_name_billing_update').val();
            var billing_email = $('#email_billing_update').val();
            var phone_billing = $('#phone_billing_update').val();
            var mobile_billing = $('#mobile_billing_update').val();
            var street_billing = $('#street_billing_update').val();
            var street2_billing = $('#street2_billing_update').val();
            var city_billing = $('#city_billing_update').val();
            var zip_billing = $('#zip_billing_update').val();
            var country_billing = $('#country_id_billing_update').val();
            var state_billing = $('#state_id_billing_update').val();

            //shipping address

            var owner_ship = $('#x_studio_owner_name_ship_update').val();
            var customer_name_ship = $('#customer_name_ship_update').val();
//            var billing_email_ship = $('#billing_email_ship').val();
            var phone_billing_ship = $('#phone_billing_ship_update').val();
            var mobile_billing_ship = $('#mobile_billing_ship_update').val();
            var street_billing_ship = $('#street_billing_ship_update').val();
            var street2_billing_ship = $('#street2_billing_ship_update').val();
            var city_billing_ship = $('#city_billing_ship_update').val();
            var zip_billing_ship = $('#zip_billing_ship_update').val();
            var country_billing_ship = $('#country_billing_ship_update').val();
            var state_billing_ship = $('#state_billing_ship_update').val();

            if (!owner_billing || !customer_name || !billing_email || !phone_billing || !mobile_billing || !street_billing || !city_billing || !zip_billing || !country_billing || !state_billing){
                alert('fields mark with "*" is required.');
                return false;
            }

            if (billing_shipping == true){
                if (!owner_ship || !customer_name_ship || !phone_billing_ship || !mobile_billing_ship || !street_billing_ship || !city_billing_ship || !zip_billing_ship || !country_billing_ship || !state_billing_ship){
                    alert('fields mark with "*" is required.');
                    return false;
                }
            }

//            if(phone_billing  ){
//                alert("Please enter valid billing address business phone number.");
//                $('#phone_billing_update').removeAttr('readonly');
//                return false;
//            }
//            if(mobile_billing ){
//                alert("Please enter valid billing address cell phone number.");
//                $('#mobile_billing_update').removeAttr('readonly');
//                return false;
//            }

            if (billing_email){
                var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
                if (!billing_email.match(validRegex)) {
                    alert("Please enter valid email address.");
                    return false;
              }
            }

//            if(billing_shipping && phone_billing_ship  ){
//                alert("Please enter valid shipping address phone number.");
//                return false;
//            }
//            if(billing_shipping && mobile_billing_ship ){
//                alert("Please enter valid shipping  address cell phone number.");
//                return false;
//            }

            var billing_obj = {
                'x_studio_lead_id': lead_id,
                'name': customer_name,
                'x_studio_owner_name': owner_billing,
                'email':billing_email,
                'phone':phone_billing,
                'mobile':mobile_billing,
                'street':street_billing,
                'street2':street2_billing,
                'city': city_billing,
                'zip':zip_billing,
                'country_id': parseInt(country_billing),
                'state_id': parseInt(state_billing)
            };
            var shipping_obj = {
                'name': customer_name_ship,
                'x_studio_owner_name': owner_ship,
                'phone':phone_billing_ship,
                'mobile':mobile_billing_ship,
                'street':street_billing_ship,
                'street2':street2_billing_ship,
                'city': city_billing_ship,
                'zip':zip_billing_ship,
                'country_id': parseInt(country_billing_ship),
                'state_id': parseInt(state_billing_ship),
                'type': 'delivery'
            };
            if (billing_shipping == true){
                var final_data = {
                'billing': billing_obj,
                'shipping': shipping_obj
                }
            }
            else{
                var final_data = {
                'billing': billing_obj,
                }
            }

            ajax.jsonRpc("/web/agent/customer/update", 'call', {'customer_data': final_data})
                .then(function (data){
                  if (data){
                        location.reload();
                  }
                  else{
                    alert('Something went wrong...');
                  }
                });
        },
        create_web_customer : function(ev){
            var billing_shipping = $('#use_diff_address').is(":checked");
            var lead_id = $('#billing_lead_id').val();

            //billing address
            var owner_billing = $('#x_studio_owner_name_billing').val();
            var customer_name = $('#customer_name_billing').val();
            var billing_email = $('#email_billing').val();
            var phone_billing = $('#phone_billing').val();
            var mobile_billing = $('#mobile_billing').val();
            var street_billing = $('#street_billing').val();
            var street2_billing = $('#street2_billing').val();
            var city_billing = $('#city_billing').val();
            var zip_billing = $('#zip_billing').val();
            var country_billing = $('#country_id_billing').val();
            var state_billing = $('#state_id_billing').val();

            //shipping address

            var owner_ship = $('#x_studio_owner_name_ship').val();
            var customer_name_ship = $('#customer_name_ship').val();
//            var billing_email_ship = $('#billing_email_ship').val();
            var phone_billing_ship = $('#phone_billing_ship').val();
            var mobile_billing_ship = $('#mobile_billing_ship').val();
            var street_billing_ship = $('#street_billing_ship').val();
            var street2_billing_ship = $('#street2_billing_ship').val();
            var city_billing_ship = $('#city_billing_ship').val();
            var zip_billing_ship = $('#zip_billing_ship').val();
            var country_billing_ship = $('#country_billing_ship').val();
            var state_billing_ship = $('#state_billing_ship').val();

            if (!owner_billing || !customer_name || !billing_email || !phone_billing || !mobile_billing || !street_billing || !city_billing || !zip_billing || !country_billing || !state_billing){
                alert('fields mark with "*" is required.');
                return false;
            }

            if (billing_shipping == true){
                if (!owner_ship || !customer_name_ship || !phone_billing_ship || !mobile_billing_ship || !street_billing_ship || !city_billing_ship || !zip_billing_ship || !country_billing_ship || !state_billing_ship){
                    alert('fields mark with "*" is required.');
                    return false;
                }
            }

            if(phone_billing && phone_billing.length != 10){
                alert("Please enter valid billing address phone number.");
                return false;
            }
            if(mobile_billing && mobile_billing.length != 10){
                alert("Please enter valid shipping address cell phone number.");
                return false;
            }

            if (billing_email){
                var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
                if (!billing_email.match(validRegex)) {
                    alert("Please enter valid email address.");
                    return false;
              }
            }

            if(phone_billing_ship && phone_billing_ship.length != 10){
                alert("Please enter valid shipping address phone number.");
                return false;
            }
            if(mobile_billing_ship && mobile_billing_ship.length != 10){
                alert("Please enter valid billing address cell phone number.");
                return false;
            }

            var billing_obj = {
                'x_studio_lead_id': lead_id,
                'name': customer_name,
                'x_studio_owner_name': owner_billing,
                'email':billing_email,
                'phone':phone_billing,
                'mobile':mobile_billing,
                'street':street_billing,
                'street2':street2_billing,
                'city': city_billing,
                'zip':zip_billing,
                'country_id': parseInt(country_billing),
                'state_id': parseInt(state_billing)
            };
            var shipping_obj = {
                'name': customer_name_ship,
                'x_studio_owner_name': owner_ship,
                'phone':phone_billing_ship,
                'mobile':mobile_billing_ship,
                'street':street_billing_ship,
                'street2':street2_billing_ship,
                'city': city_billing_ship,
                'zip':zip_billing_ship,
                'country_id': parseInt(country_billing_ship),
                'state_id': parseInt(state_billing_ship),
                'type': 'delivery'
            };
            if (billing_shipping == true){
                var final_data = {
                'billing': billing_obj,
                'shipping': shipping_obj
                }
            }
            else{
                var final_data = {
                'billing': billing_obj,
                }
            }

            ajax.jsonRpc("/web/agent/customer/", 'call', {'customer_data': final_data})
                .then(function (data){
                  if (data){
                        location.reload();
                  }
                  else{
                    alert('Something went wrong...');
                  }
                });
        },

        change_billing_shipping : function(ev){
            if ($('#use_diff_address').is(":checked")){
                this.$('.ship_add').removeClass('d-none');
                this.$('.div_ship_add').removeClass('d-none');
            }
            else{
                this.$('.ship_add').addClass('d-none');
                this.$('.div_ship_add').addClass('d-none');
            }
        },
        change_billing_shipping_update : function(ev){
            if ($('#use_diff_address_update').is(":checked")){
                this.$('.ship_add_update').removeClass('d-none');
                this.$('.div_ship_add_update').removeClass('d-none');
            }
            else{
                this.$('.ship_add_update').addClass('d-none');
                this.$('.div_ship_add_update').addClass('d-none');
            }
        }
    });
});