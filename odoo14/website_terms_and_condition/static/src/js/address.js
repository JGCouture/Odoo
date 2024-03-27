odoo.define('wt_zbspos.address', function (require) {
'use strict';

    var core = require('web.core');
    var wSaleUtils = require('website_sale.utils');
    const wUtils = require('website.utils');
    var publicWidget = require('web.public.widget');
    var PaymentForm = require('payment.payment_form');
    var _t = core._t;

    publicWidget.registry.WebsiteSale.include({
        events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events, {
            'change select[name="find_ref"]': '_onChangeFindRef',
            'change select[name="online_add"]': '_onChangeOtherAdd'
        }),

        _onChangeFindRef: function (ev) {
            $('#online_add').val('');
            $('#ref').val('');
            $('#text_other_add').val('');
            if ($(ev.currentTarget).val() === 'referral'){
                this.$('#div_ref').removeClass('d-none')
            }
            if ($(ev.currentTarget).val() === 'agent'){
                this.$('#div_agent').removeClass('d-none')
                this.$('select.x_studio_agent_cl').select2();
                this.$('.select2-choice').css({
                    "min-width": "100%",
                    "max-width": "100%",
                    "min-height": "35px",
                    "max-height": "35px",
                    "background": "none",
                    "padding-top": "4px"
                });
            }
             if ($(ev.currentTarget).val() === 'online_ad'){
                this.$('#div_online_add').removeClass('d-none')
            }
            if ($(ev.currentTarget).val() !== 'referral'){
                this.$('#div_ref').addClass('d-none')
            }
//            if ($(ev.currentTarget).val() !== 'agent'){
//                this.$('#div_agent').addClass('d-none')
//            }
            if ($(ev.currentTarget).val() !== 'online_ad'){
                this.$('#other_add').addClass('d-none')
                this.$('#div_online_add').addClass('d-none')
            }

        },
        _onChangeOtherAdd: function(ev){
            if ($(ev.currentTarget).val() === 'other'){
                this.$('#other_add').removeClass('d-none')
            }
            if ($(ev.currentTarget).val() !== 'other'){
                this.$('#other_add').addClass('d-none')
            }

        }
    });
});
