odoo.define('website_terms_and_condition.terms', function (require) {
"use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var PaymentForm = require('payment.payment_form');

    var _t = core._t;

    PaymentForm.include({
        payEvent: function (ev) {
            var self = this;
            if (ev.type === 'submit') {
                var button = $(ev.target).find('*[type="submit"]')[0]
            } else {
                var button = ev.target;
            }
            if (! self.$('#flexCheckDefault')[0].checked){
                alert("Please Accept our Teams and Conditions")
                self.enableButton(button);
                return false;
            }
            else if ($('#order_type_pay').val() && $('#order_type_pay').val() == 'add_ons'){
                return this._super.apply(this, arguments);
            }
            else if (self.$('#ordering').length > 0 && (! self.$('#ordering')[0].checked)){
                alert("Please fill the form of online ordering")
                self.enableButton(button);
                return false;
            }else if (self.$('#ach').length > 0 && (! self.$('#ach')[0].checked)){

                alert("Please fill the form of ach")
                self.enableButton(button);
                return false;
            }
            else{
                return this._super.apply(this, arguments);
            }
        },
    });

    $('.signup_country').on('change', function(){
        var country_id = $('.signup_country').val();
        if (country_id){
            ajax.jsonRpc("/get/signup/states/", 'call', {'country_id': country_id})
            .then(function (data){
              if (data){
                $('.signup_state').empty();
                $('.signup_state').append(new Option('Select State', ''));
                for (const key of Object.keys(data)){
                    $('.signup_state').append(new Option(data[key], key));
                }
              }
              else{
                $('.signup_state').empty();
                $('.signup_state').append(new Option('', 'Select State'));
              }
            });
        }
        else{
            console.log('\n\n no country selecte')
        }
    });

//    $(document).ready(function(){
//    if (window.location.href.indexOf("/shop/payment") > -1) {
//        var order = $('#sale_order_id').val();
//        if (order){
//            ajax.jsonRpc("/check/term/", 'call', {'order': order})
//            .then(function (data){
//              if (data){
//                var attachment = $('.wk_file_success').length;
//                if (attachment == 0){
//                    $("#terms_condition_modal").modal('show');
//                }
//              }
//            });
//        }
//    }
//});

});
