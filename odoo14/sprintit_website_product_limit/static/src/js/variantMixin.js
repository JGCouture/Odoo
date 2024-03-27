odoo.define('sprintit_website_product_limit.variantMixin', function (require) {
'use strict';

//var ProductConfiguratorMixin = require('sale.ProductConfiguratorMixin');
//var sAnimations = require('website.content.snippets.animation');

var VariantMixin = require('sale.VariantMixin');
var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var core = require('web.core');
var QWeb = core.qweb;
var xml_load = ajax.loadXML(
	    '/sprintit_website_product_limit/static/src/xml/website_sale_product_limit.xml',
	    QWeb
	);


VariantMixin._onChangeProductLimit = function (ev, $parent, combination) {
	var product_id = 0;
    // needed for list view of variants
    if ($parent.find('input.product_id:checked').length) {
        product_id = $parent.find('input.product_id:checked').val();
    } else {
        product_id = $parent.find('.product_id').val();
    }
    var isMainProduct = combination.product_id &&
        ($parent.is('.js_main_product') || $parent.is('.main_product')) &&
        combination.product_id === parseInt(product_id);

    if (!this.isWebsite || !isMainProduct){
        return;
    }
   
    var qty = $parent.find('input[name="add_qty"]').val();
    var order_limit = combination.order_limit
    order_limit -= parseInt(combination.product_cart_qty);
    
    if (order_limit < 0) {
            order_limit = 0;
        }

    $parent.find('#add_to_cart').removeClass('disabled');
    if (combination.apply_order_limit == true && qty > order_limit) {
    	  combination.display_message = true
    	  var $input_add_qty = $parent.find('input[name="add_qty"]');
    	  qty = order_limit || 1
    	  $input_add_qty.val(qty);
    	  
    	  if (order_limit == 0) {
    		  $parent.find('#add_to_cart').addClass('disabled');
    	  }
    	  
    }

    xml_load.then(function () {
    	 $('.oe_website_sale')
         .find('.product_limit_messages_' + combination.order_limit)
         .remove();

    	 
        var $message = $(QWeb.render(
            'sprintit_website_product_limit.product_availability',
            combination
        ));
        $('div.product_limit_messages').html($message);
    });
    
    
};



publicWidget.registry.WebsiteSale.include({
    _onChangeCombination: function (){
        this._super.apply(this, arguments);
        VariantMixin._onChangeProductLimit.apply(this, arguments);
    }
});

return VariantMixin;

});