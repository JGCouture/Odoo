odoo.define('website_file_upload.doc', function (require) {
"use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var PaymentForm = require('payment.payment_form');

    var _t = core._t;

    PaymentForm.include({
        payEvent: function (ev) {
            var self = this;
            var require_doc = $('#required_doc').val();
            var uploaded_att = $('#uploaded_att').val();
            var sale_id = $('#sale_order_temp').val();

            var find_us_pay = $('#find_us_pay').val();
            var order_type_pay = $('#order_type_pay').val();
            var agent_select_pay = $('#agent_select_pay').val();
            var ref_pay_pay = $('#ref_pay_pay').val();
            var online_add_pay = $('#online_add_pay').val();
            var text_other_add_pay = $('#text_other_add_pay').val();
            if (window.location.href.indexOf("/shop/payment") > -1){
               if ((parseInt(uploaded_att) < parseInt(require_doc)) || (require_doc && !uploaded_att)){
                ajax.jsonRpc("/check/required/document/", 'call', {'sale_id': sale_id})
                .then(function (data){
                  if (data){
                     alert(data);
                  }
                });
                return false;
            }
            else if (! order_type_pay){
                alert('Please order type.');
                return false;
            }
            else if (find_us_pay == 'agent' && !agent_select_pay){
                alert('Please select agent.');
                return false;
            }
            else if (find_us_pay == 'referral' && !ref_pay_pay){
                alert('Please enter referral.');
                return false;
            }
            else if (find_us_pay == 'online_ad' && !online_add_pay){
                alert('Please select online ads.');
                return false;
            }
            else if (find_us_pay == 'online_ad' && online_add_pay && online_add_pay == 'other' && !text_other_add_pay){
                alert('Please enter other ads.');
                return false;
            }
            else{
                if (sale_id){
                    ajax.jsonRpc("/update/order/info/", 'call', {'sale_id': sale_id,
                                                                'find_us_pay': find_us_pay,
                                                                'order_type_pay':order_type_pay,
                                                                'agent_select_pay': agent_select_pay,
                                                                'ref_pay_pay': ref_pay_pay,
                                                                'online_add_pay': online_add_pay,
                                                                'text_other_add_pay':text_other_add_pay
                                                                })
                    .then(function (data){
                    });
                }
                return this._super.apply(this, arguments);
            }
            }
            else{
                return this._super.apply(this, arguments);
            }
        },
    });

    $('.final-submit').on('click', function(e){
        var find_us_pay = $('#find_us_pay').val();
        var order_type_pay = $('#order_type_pay').val();
        var agent_select_pay = $('#agent_select_pay').val();
        var ref_pay_pay = $('#ref_pay_pay').val();
        var online_add_pay = $('#online_add_pay').val();
        var text_other_add_pay = $('#text_other_add_pay').val();

        var require_doc = $('#required_doc').val();
        var uploaded_att = $('#uploaded_att').val();
        var sale_id = $('#sale_order_temp').val();

        if ((parseInt(uploaded_att) < parseInt(require_doc)) || (require_doc && !uploaded_att)){
             alert($('#required_doc_list').val());
             e.preventDefault();
        }
        else if (! order_type_pay){
            alert('Please order type.');
            e.preventDefault();
        }
        else if (find_us_pay == 'agent' && !agent_select_pay){
            alert('Please select agent.');
            e.preventDefault();
        }
        else if (find_us_pay == 'referral' && !ref_pay_pay){
            alert('Please enter referral.');
            e.preventDefault();
        }
        else if (find_us_pay == 'online_ad' && !online_add_pay){
            alert('Please select online ads.');
            e.preventDefault();
        }
        else if (find_us_pay == 'online_ad' && online_add_pay && online_add_pay == 'other' && !text_other_add_pay){
            alert('Please enter other ads.');
            e.preventDefault();
        }
        else{
            if (sale_id){
            ajax.jsonRpc("/update/order/info/", 'call', {'sale_id': sale_id,
                                                        'find_us_pay': find_us_pay,
                                                        'order_type_pay':order_type_pay,
                                                        'agent_select_pay': agent_select_pay,
                                                        'ref_pay_pay': ref_pay_pay,
                                                        'online_add_pay': online_add_pay,
                                                        'text_other_add_pay':text_other_add_pay
                                                        })
            .then(function (data){
            });
            }
        }

    });
});