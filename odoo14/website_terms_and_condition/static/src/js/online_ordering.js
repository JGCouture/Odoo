odoo.define('wt_tricsa_website.cart', function (require) {
'use strict';

    var core = require('web.core');
    var wSaleUtils = require('website_sale.utils');
    const ajax = require('web.ajax');
    const Dialog = require('web.Dialog');
    const publicWidget = require('web.public.widget');
    var _t = core._t;

        publicWidget.registry.online_ordering = publicWidget.Widget.extend({
        selector: '#online_ordering_modal',
        events: {
            'click .online_order_submit': '_onSubmitOrdering',
               'click #kp_online_order_pricing_confirmation_signature_clear': 'kp_online_order_pricing_confirmation_signature_clear',
            'click #kp_online_order_from_application_signature_clear': 'kp_online_order_from_application_signature_clear',
            'click #kp_online_order_personal_guarantee_signature_clear': 'kp_online_order_personal_guarantee_signature_clear',
            'click #kp_online_order_client_initials_clear': 'kp_online_order_client_initials_clear',
            'click #kp_online_order_client_business_principle_signature_clear': 'kp_online_order_client_business_principle_signature_clear',
            'click #kp_online_order_signature_clear': 'kp_online_order_signature_clear',
        },
        start() {
            const def = this._super(...arguments);
            this.$('.kp_online_order_pricing_confirmation_signature').jqSignature({lineWidth: 3,width: 600,height: 100});
            this.kp_online_order_pricing_confirmation_signature_emptyUrl = this.$('.kp_online_order_pricing_confirmation_signature').jqSignature('getDataURL');
            this.$('.kp_online_order_from_application_signature').jqSignature({lineWidth: 3,width: 600,height: 100});
            this.kp_online_order_from_application_signature_emptyUrl = this.$('.kp_online_order_from_application_signature').jqSignature('getDataURL');
            this.$('.kp_online_order_personal_guarantee_signature').jqSignature({lineWidth: 3,width: 600,height: 100});
            this.kp_online_order_personal_guarantee_signature_emptyUrl = this.$('.kp_online_order_personal_guarantee_signature').jqSignature('getDataURL');
            this.$('.kp_online_order_client_initials').jqSignature({lineWidth: 3,width: 600,height: 100});
            this.kp_online_order_client_initials_emptyUrl = this.$('.kp_online_order_client_initials').jqSignature('getDataURL');
            this.$('.kp_online_order_client_business_principle_signature').jqSignature({lineWidth: 3,width: 600,height: 100});
            this.kp_online_order_client_business_principle_signature_emptyUrl = this.$('.kp_online_order_client_business_principle_signature').jqSignature('getDataURL');
            this.$('.kp_online_order_signature').jqSignature({lineWidth: 3,width: 600,height: 100});
            this.kp_online_order_signature_emptyUrl = this.$('.kp_online_order_signature').jqSignature('getDataURL');
    //        console.warn(this.emptyUrl);
            return def;
        },
        kp_online_order_pricing_confirmation_signature_clear: function (ev) {
            this.$('.kp_online_order_pricing_confirmation_signature').jqSignature('clearCanvas');
        },
        kp_online_order_from_application_signature_clear: function (ev) {
            this.$('.kp_online_order_from_application_signature').jqSignature('clearCanvas');
        },
        kp_online_order_personal_guarantee_signature_clear: function (ev) {
            this.$('.kp_online_order_personal_guarantee_signature').jqSignature('clearCanvas');
        },
        kp_online_order_client_initials_clear: function (ev) {
            this.$('.kp_online_order_client_initials').jqSignature('clearCanvas');
        },
        kp_online_order_client_business_principle_signature_clear: function (ev) {
            this.$('.kp_online_order_client_business_principle_signature').jqSignature('clearCanvas');
        },
        kp_online_order_signature_clear: function (ev) {
            this.$('.kp_online_order_signature').jqSignature('clearCanvas');
        },

        _onSubmitOrdering: function (ev) {
            var self = this;
            var partner_id = parseInt(this.$("input[name='partner_id']").val());
            // var name = this.$("input[name='name']").val();
             var need_website = this.$("input[name='need_website']:checked").val();
             var website_address = this.$("input[name='website_address']").val();
             var menu_other = this.$("input[name='menu_other']").val();
            // var website1 = this.$("input[name='website1']").val();
            // var website2 = this.$("input[name='website2']").val();
            // var website3 = this.$("input[name='website3']").val();
            var monday = this.$("input[name='monday']").val();
            var tuesday = this.$("input[name='tuesday']").val();
            var wednesday = this.$("input[name='wednesday']").val();
            var thursday = this.$("input[name='thursday']").val();
            var friday = this.$("input[name='friday']").val();
            var saturday = this.$("input[name='saturday']").val();
            var sunday = this.$("input[name='sunday']").val();

            var monday_shift2 = this.$("input[name='monday_shift2']").val();
            var tuesday_shift2 = this.$("input[name='tuesday_shift2']").val();
            var wednesday_shift2 = this.$("input[name='wednesday_shift2']").val();
            var thursday_shift2 = this.$("input[name='thursday_shift2']").val();
            var friday_shift2 = this.$("input[name='friday_shift2']").val();
            var saturday_shift2 = this.$("input[name='saturday_shift2']").val();
            var sunday_shift2 = this.$("input[name='sunday_shift2']").val();

            var sale_tax = this.$("input[name='sale_tax']").val();
            var email_address = this.$("input[name='email_address']").val();
            var backup_phone_number = this.$("input[name='backup_phone_number']").val();
            var delivery_distance = this.$("input[name='delivery_distance']").val();
            var pickup_order_time = this.$("input[name='pickup_order_time']").val();
            var delivery_order_time = this.$("input[name='delivery_order_time']").val();
            var need_chinese = this.$("input[name='need_chinese']:checked").val();
//            var service_type = this.$("input[name='service_type']").val();
            var plan_choice = this.$("input[name='plan_choice']:checked").val();
            var order_notification = this.$("input[name='notification_choice']:checked").val();
            var do_delivery = this.$("input[name='do_delivery']:checked").val();
//            var delivery_zone = this.$("input[name='delivery_zone']").val();
            var delivery_free = this.$("input[name='delivery_free']").val();
            var min_order_amount = this.$("input[name='min_order_amount']").val();
//            var free_delivery_min_amount = this.$("input[name='free_delivery_min_amount']").val();
            var payment_option = this.$("input[name='payment_option']:checked").val();
            var notes = this.$("textarea[name='notes']").val();
            var sale_order_id = this.$("input[name='sale_order_id']").val();
             if (this.kp_online_order_pricing_confirmation_signature_emptyUrl == $('.kp_online_order_pricing_confirmation_signature').jqSignature('getDataURL')){
                ev.preventDefault();
                alert("Please sign your name in the pricing confirmation Signature!");
                return;
            }
            if (this.kp_online_order_from_application_signature_emptyUrl == $('.kp_online_order_from_application_signature').jqSignature('getDataURL')){
                ev.preventDefault();
                alert("Please sign your name in the from application Signature!");
                return;
            }
            if (this.kp_online_order_personal_guarantee_signature_emptyUrl == $('.kp_online_order_personal_guarantee_signature').jqSignature('getDataURL')){
                ev.preventDefault();
                alert("Please sign your name in the personal guarantee Signature!");
                return;
            }
            if (this.kp_online_order_client_initials_emptyUrl == $('.kp_online_order_client_initials').jqSignature('getDataURL')){
                ev.preventDefault();
                alert("Please sign your name in the client initials Signature!");
                return;
            }
            if (this.kp_online_order_client_business_principle_signature_emptyUrl == $('.kp_online_order_client_business_principle_signature').jqSignature('getDataURL')){
                ev.preventDefault();
                alert("Please sign your name in the client business principle signature!");
                return;
            }
            if (this.kp_online_order_signature_emptyUrl == $('.kp_online_order_signature').jqSignature('getDataURL')){
                ev.preventDefault();
                alert("Please sign your name in the signature");
                return;
            }
            if (!$('#company_name').val()) {
                alert('Enter your company name!');
                ev.preventDefault();
                return
            }
            if (!$('#customer_id').val()) {
                alert('Enter your customer id !');
                ev.preventDefault();
                return
            }

            if (!$('#ssn').val()) {
                alert('Enter your ssn!');
                ev.preventDefault();
                return
            }
            if (!$('#tax_id').val()) {
                alert('Enter your tax id!');
                ev.preventDefault();
                return
            }
            if (!$('#bank').val()) {
                alert('Enter your bank name!');
                ev.preventDefault();
                return
            }
            if (!$('#account_number').val()) {
                alert('Enter your account number!');
                ev.preventDefault();
                return
            }
            if (!$('#routing_number').val()) {
                alert('Enter your routing number!');
                ev.preventDefault();
                return
            }
            if (!$('#pos_system').val()) {
                alert('Choose your pos system!');
                ev.preventDefault();
                return
            }
            if (!$("input:radio[name='online_order_terms']").is(":checked")){
                alert('Check the online order terms !');
                ev.preventDefault();
                return
            }
            if (!sale_tax ){
                alert("Input sale tax datetime");
                 ev.preventDefault();
            }
            if (!monday ){
                alert("Input monday datetime");
                 ev.preventDefault();
            }
            if (!tuesday){
                alert("Input tuesday datetime");
                 ev.preventDefault();
            }
            if ( !wednesday ){
                alert("Input wednesday datetime");
                 ev.preventDefault();
            }
            if (!thursday ){
                alert("Input thursday datetime");
                 ev.preventDefault();
            }
            if (!friday ){
                alert("Input friday datetime");
                 ev.preventDefault();
            }
            if (!saturday ){
                alert("Input saturday datetime");
                 ev.preventDefault();
            }
            if (!sunday){
                alert("Input sunday datetime");
                 ev.preventDefault();
            }
            if ($('#menu').get(0).files.length === 0) {
                alert('Upload the menu document !');
                ev.preventDefault();
                return
            }
            if ($('#irs_document').get(0).files.length === 0) {
                alert('Upload the irs document !');
                ev.preventDefault();
                return
            }
            if ($('#owner_id').get(0).files.length === 0) {
                alert('Upload the owner id document!');
                ev.preventDefault();
                return
            }
            if ($('#void_check').get(0).files.length === 0) {
                alert('Upload the void check document!');
                ev.preventDefault();
                return false;
            }
            if (!$("input:radio[name='plan_choice']").is(":checked")){
                alert('Check the plan choice !');
                ev.preventDefault();
                return
            }
             if (!$("input:radio[name='if_cash_discount']").is(":checked")){
                alert('Check the cash discount !');
                ev.preventDefault();
                return
            }
            if(backup_phone_number && backup_phone_number.length != 10){
                alert("Please enter valid phone number.");
                ev.preventDefault();
                return false;
            }
            if (email_address){
                var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
                if (!email_address.match(validRegex)) {
                    alert("Please enter valid email address.");
                    ev.preventDefault();
                    return
              }
            }
            if (!$('#from_application_signature_date').val()) {
                alert('Enter your from application signature date!');
                ev.preventDefault();
                return
            }
            if (!$('#print_client_business_legal_name').val()) {
                alert('Enter your from print client business legal name!');
                ev.preventDefault();
                return
            }
            if (!$('#personal_guarantee_signature_date').val()) {
                alert('Enter your personal guarantee signature date!');
                ev.preventDefault();
                return
            }
            if (!$('#client_business_principle_sign_date').val()) {
                alert('Enter your client business principle sign date!');
                ev.preventDefault();
                return
            }
            if (!$('#client_business_principle_title').val()) {
                alert('Enter your client business principle title!');
                ev.preventDefault();
                return
            }
            if (!$('#print_name_of_signer').val()) {
                alert('Enter your print name of signer!');
                ev.preventDefault();
                return
            }
            if (!$('#date').val()) {
                alert('Enter your date!');
                ev.preventDefault();
                return
            }
            var use_google_business = this.$("input[name='use_google_business']:checked").val();

            if (!order_notification){
                order_notification = false;
            }

            const fd = new FormData();
            fd.append("csrf_token", $('#csrf_token').val())

            fd.append("sale_order_id", sale_order_id);
            fd.append("partner_id", partner_id)
            fd.append("need_website", need_website)
            fd.append("website_address", website_address)
            fd.append("menu_other", menu_other)

            fd.append("customer_id", $('#customer_id').val())
            fd.append("pos_system", $('#pos_system').val())
            fd.append("sale_tax", sale_tax)
            fd.append("email_address", email_address)
            fd.append("backup_phone_number", backup_phone_number)
            fd.append("do_delivery", do_delivery)
            fd.append("need_chinese", need_chinese)
            fd.append("plan_choice", plan_choice)
            fd.append("order_notification", order_notification)
            fd.append("min_order_amount", min_order_amount);
            fd.append("payment_option", payment_option);

            fd.append("delivery_free", delivery_free);
            fd.append("delivery_distance", delivery_distance);
            fd.append("pickup_order_time", pickup_order_time);
            fd.append("delivery_order_time", delivery_order_time);
            fd.append("use_google_business", use_google_business);
            fd.append("notes", notes);

            fd.append("bank", $('#bank').val());
            fd.append("account_number", $('#account_number').val());
            fd.append("routing_number", $('#routing_number').val());

            fd.append("company_name", $('#company_name').val());
            fd.append("ssn", $('#ssn').val());
            fd.append("tax_id", $('#tax_id').val());
            fd.append('if_cash_discount', $('input[name="if_cash_discount"]:checked').val());

            fd.append('kp_online_order_pricing_confirmation_signature', this.$('.kp_online_order_pricing_confirmation_signature').jqSignature('getDataURL'));
            fd.append('kp_online_order_from_application_signature', this.$('.kp_online_order_from_application_signature').jqSignature('getDataURL'));
            fd.append('kp_online_order_personal_guarantee_signature', this.$('.kp_online_order_personal_guarantee_signature').jqSignature('getDataURL'));
            fd.append('kp_online_order_client_initials', this.$('.kp_online_order_client_initials').jqSignature('getDataURL'));
            fd.append('kp_online_order_client_business_principle_signature', this.$('.kp_online_order_client_business_principle_signature').jqSignature('getDataURL'));
            fd.append('kp_online_order_signature', this.$('.kp_online_order_signature').jqSignature('getDataURL'));

            if ($('#menu').get(0).files.length != 0) {
                fd.append('menu', $('#menu')[0].files[0]);
            }
            if ($('#owner_id').get(0).files.length != 0) {
                fd.append('owner_id', $('#owner_id')[0].files[0]);
            }
            if ($('#irs_document').get(0).files.length != 0) {
                fd.append('irs_document', $('#irs_document')[0].files[0]);
            }
            if ($('#void_check').get(0).files.length != 0) {
                fd.append('void_check', $('#void_check')[0].files[0]);
            }
            fd.append('from_application_signature_date', $('#from_application_signature_date').val());
            fd.append('personal_guarantee_signature_date', $('#personal_guarantee_signature_date').val());
            fd.append('print_client_business_legal_name', $('#print_client_business_legal_name').val());
            fd.append('print_name_of_signer', $('#print_name_of_signer').val());
            fd.append('client_business_principle_title', $('#client_business_principle_title').val());
            fd.append('client_business_principle_sign_date', $('#client_business_principle_sign_date').val());
            fd.append('date', $('#date').val());

            const p1 = new Promise((resolve, reject) => {
              // or
              // reject(new Error("Error!"));
              $.ajax({url: "/online/kwickpos_ordering",
                    type: 'POST',
                    data: fd,
                    processData: false,
                    contentType: false,
                    success: function(result){
                        if (result.results.code=="201"){
                            resolve("kwickpos online order creation succeeded!");
                        }
                        else{
                            reject(new Error("Kwickpos online order creation failed!"));
                        }
              }});
            });
            p1.then(
              (value) => {
                    this._rpc({
                    route: "/online/ordering",
                    params: {
                            'partner_id': parseInt(partner_id),
                            // 'name': name,
                             'need_website': need_website,
                             'website_address': website_address,
                             'menu_other': menu_other,
                            // 'website_option': website_option,
                            // 'preferred_website1': website1,
                            // 'preferred_website2': website2,
                            // 'preferred_website3': website3,
                            'monday': monday,
                            'tuesday': tuesday,
                            'wednesday': wednesday,
                            'thursday': thursday,
                            'friday': friday,
                            'saturday': saturday,
                            'sunday': sunday,
                            'monday_shift2': monday_shift2,
                            'tuesday_shift2': tuesday_shift2,
                            'wednesday_shift2': wednesday_shift2,
                            'thursday_shift2': thursday_shift2,
                            'friday_shift2': friday_shift2,
                            'saturday_shift2': saturday_shift2,
                            'sunday_shift2': sunday_shift2,
                            'sale_tax': sale_tax,
                            'email_address':email_address,
                            'backup_phone_number':backup_phone_number,
                            'do_delivery':do_delivery,
                            'need_chinese': need_chinese,
                            'order_notification': order_notification,
                            'min_order_amount': min_order_amount,
                            'payment_option': payment_option,
                            'sale_order_id': parseInt(sale_order_id),
                            'delivery_free' : delivery_free,
                            'delivery_distance':delivery_distance,
                            'pickup_order_time':pickup_order_time,
                            'delivery_order_time': delivery_order_time,
                            'use_google_business':use_google_business,
                            'notes':notes
                        },
                    }).then(function (data) {
                        if(data.order_id){
                            $("#ordering").prop("disabled", false);
                            $("#ordering").prop("checked", true);

                        }else{
                             console.log("Online order creation failed!");
                        }
                         // Success!
                    });
              },
              (reason) => {
                    console.error(reason); // Error!
              },
            );
        },
    });
});