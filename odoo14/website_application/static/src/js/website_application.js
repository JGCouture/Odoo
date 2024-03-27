

odoo.define('website_application.form', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var VariantMixin = require('sale.VariantMixin');

publicWidget.registry.website_application = publicWidget.Widget.extend(VariantMixin, {
    selector: '.website_application',
    events: _.extend({}, VariantMixin.events || {}, {
        'change select[name="country_id"]': '_changeCountry',
        'click #clearCanvas': '_clearCanvas',
        'click #ach_submit': '_achSubmit',
    }),
    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    start() {
        const def = this._super(...arguments);
        this.$('select[name="country_id"]').change();
        this.$('.js-signature').jqSignature({autoFit: true});
//        this.$('.js-signature-rma').jqSignature({autoFit: true});
        this.emptyUrl = this.$('.js-signature').jqSignature('getDataURL');
//        console.warn(this.emptyUrl);


        return def;
    },
    /**
     * @private
     */
    _changeCountry: function () {
        if (!$("#country_id").val()) {
            return;
        }
        this._rpc({
            route: "/application/country_infos/" + $("#country_id").val(),
            params: {
                mode: {}
            },
        }).then(function (data) {
            // placeholder phone_code
            $("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');

            // populate states and display
            var selectStates = $("select[name='state_id']");
            // dont reload state at first loading (done in qweb)
            if (selectStates.data('init')===0 || selectStates.find('option').length===1) {
                if (data.states.length || data.state_required) {
                    selectStates.html('');
                    _.each(data.states, function (x) {
                        var opt = $('<option>').text(x[1])
                            .attr('value', x[0])
                            .attr('data-code', x[2]);
                        selectStates.append(opt);
                    });
                    selectStates.parent('div').show();
                } else {
                    selectStates.val('').parent('div').hide();
                }
                selectStates.data('init', 0);
            } else {
                selectStates.data('init', 0);
            }

            // manage fields order / visibility
            if (data.fields) {
                if ($.inArray('zip', data.fields) > $.inArray('city', data.fields)){
                    $(".div_zip").before($(".div_city"));
                } else {
                    $(".div_zip").after($(".div_city"));
                }
                var all_fields = ["street", "zip", "city", "country_name"]; // "state_code"];
                _.each(all_fields, function (field) {
                    $(".checkout_autoformat .div_" + field.split('_')[0]).toggle($.inArray(field, data.fields)>=0);
                });
            }

            if ($("label[for='zip']").length) {
                $("label[for='zip']").toggleClass('label-optional', !data.zip_required);
                $("label[for='zip']").get(0).toggleAttribute('required', !!data.zip_required);
            }
            if ($("label[for='zip']").length) {
                $("label[for='state_id']").toggleClass('label-optional', !data.state_required);
                $("label[for='state_id']").get(0).toggleAttribute('required', !!data.state_required);
            }
        });
    },
    _clearCanvas: function () {
        this.$('.js-signature').jqSignature('clearCanvas');
//        this.$('.js-signature-rma').jqSignature('clearCanvas');
    },
    _achSubmit:function(evt){
        console.log(this.$('.js-signature').jqSignature('getDataURL'));
        this.$('#hidden_canvas').val(this.$('.js-signature').jqSignature('getDataURL'))

        if (this.emptyUrl == this.$('.js-signature').jqSignature('getDataURL')){
            alert("Please sign your name!");
            evt.preventDefault();
            return
        }
        this._rpc({
                    route: '/canvas',
                    params: {
                        'canvas': this.$('.js-signature').jqSignature('getDataURL'),
                        'dba':this.$('#DBA').val(),
                        'street':this.$('#StoreAddress').val(),
                        'city':this.$('#StoreCity').val(),
                        'state_id':this.$('#state_id').val(),
                        'store_zip':this.$('#StoreZip').val(),
                        'country_id':this.$('#country_id').val(),
                        'owner_phone':this.$('#OwnerPhone').val(),
                        'email':this.$('#OwnerEmail').val(),
                    },
                }).then(function(result) {
                    setTimeout(
                      function()
                      {
                      }, 700);
                });

    },

    /**
     * Add custom variant values and attribute values that do not generate variants
     * in the form data and trigger submit.
     *
     * @private
     * @returns {Promise} never resolved
     */
//    _submitForm: function () {
//        let params = this.rootProduct;
//        params.add_qty = params.quantity;
//
//        params.product_custom_attribute_values = JSON.stringify(params.product_custom_attribute_values);
//        params.no_variant_attribute_values = JSON.stringify(params.no_variant_attribute_values);
//
//        if (this.isBuyNow) {
//            params.express = true;
//        }
//        return wUtils.sendRequest('/shop/cart/update', params);
//    },


});


});
