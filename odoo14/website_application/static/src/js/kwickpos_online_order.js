odoo.define('website_application.kwickpos_online_order', function (require) {
'use strict';
	var core = require('web.core');
	var _t = core._t;
	var ajax = require('web.ajax');
	var currentUrl = location.href;
	function isInDesiredForm(str) {
        var n = Math.floor(Number(str));
        return n !== Infinity && String(n) === str && n >= 0;
    }
    $(document).ready(function() {

        $('.pricing_confirmation_signature').jqSignature({autoFit: true,lineWidth: 3});
        $('.from_application_signature').jqSignature({autoFit: true,lineWidth: 3});
        $('.personal_guarantee_signature').jqSignature({autoFit: true,lineWidth: 3});
        $('.client_initials').jqSignature({autoFit: true,lineWidth: 3});
        $('.client_business_principle_signature').jqSignature({autoFit: true,lineWidth: 3});
        $('.signature').jqSignature({autoFit: true,lineWidth: 3})

        var pricing_confirmation_signature_emptyUrl = $('.pricing_confirmation_signature').jqSignature('getDataURL');
        var from_application_signature_emptyUrl = $('.from_application_signature').jqSignature('getDataURL');
        var personal_guarantee_signature_emptyUrl = $('.personal_guarantee_signature').jqSignature('getDataURL');
        var client_initials_emptyUrl = $('.client_initials').jqSignature('getDataURL');
        var client_business_principle_signature_emptyUrl = $('.client_business_principle_signature').jqSignature('getDataURL');
        var signature_emptyUrl = $('.signature').jqSignature('getDataURL');

        $("#pricing_confirmation_signature_clear").click(function( e ) {
            $('.pricing_confirmation_signature').jqSignature('clearCanvas');
            e.preventDefault();
		});
        $("#from_application_signature_clear").click(function( e ) {
    		$('.from_application_signature').jqSignature('clearCanvas');
    		e.preventDefault();
		});
		$("#personal_guarantee_signature_clear").click(function( e ) {
    		$('.personal_guarantee_signature').jqSignature('clearCanvas');
    		e.preventDefault();
		});
		$("#client_initials_signature_clear").click(function( e ) {
    		$('.client_initials').jqSignature('clearCanvas');
    		e.preventDefault();
		});
		$("#client_business_principle_signature_clear").click(function( e ) {
    		$('.client_business_principle_signature').jqSignature('clearCanvas');
    		e.preventDefault();
		});
		$("#signature_clear").click(function( e ) {
    		$('.signature').jqSignature('clearCanvas');
    		e.preventDefault();
		});
        $( "input[name=need_website]" ).change(function() {
            if ($("input[name=need_website][value='2']").prop("checked"))
              {
                $("#div_need_website").removeAttr("hidden");
              }
            if ($("input[name=need_website][value='3']").prop("checked"))
              {
                $("#div_need_website").removeAttr("hidden");
              }
             if ($("input[name=need_website][value='1']").prop("checked"))
              {

                $("#div_need_website").attr("hidden",'hidden');
              }
        });
        $( "#service_type" ).change(function() {
            var selectVal = $("#service_type option:selected").val();
            if(selectVal == '1'){

                $("#delivery_zone_and_charges").attr("hidden",'hidden');

            }else{
                $("#delivery_zone_and_charges").removeAttr("hidden");

            }
        });
        $( "input[name=payment_option]" ).change(function() {
            if ($("input[name=payment_option][value='1']").prop("checked"))
              {
                $("#div_payment_setup").removeAttr("hidden");
              }
            if ($("input[name=payment_option][value='2']").prop("checked"))
              {
                $("#div_payment_setup").removeAttr("hidden");
              }
             if ($("input[name=payment_option][value='3']").prop("checked"))
              {
                $("#div_payment_setup").attr("hidden",'hidden');
              }
        });
        $('#kwickpos_online_order_submit').on('click', function(e) {
            if (from_application_signature_emptyUrl == $('.from_application_signature').jqSignature('getDataURL')){
                var from_application_signature = document.getElementsByClassName('from_application_signature')[0];
                from_application_signature.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert("Please sign your name in the from Application Signature!");
                e.preventDefault();
                return
            }
            if (personal_guarantee_signature_emptyUrl == $('.personal_guarantee_signature').jqSignature('getDataURL')){
                var personal_guarantee_signature = document.getElementsByClassName('personal_guarantee_signature')[0];
                personal_guarantee_signature.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert("Please sign your name in the Personal Guarantee Signature!");
                e.preventDefault();
                return
            }
            if (client_initials_emptyUrl == $('.client_initials').jqSignature('getDataURL')){
                var client_initials = document.getElementsByClassName('client_initials')[0];
                client_initials.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert("Please sign your name in the Client Initials!");
                e.preventDefault();
                return
            }
            if (client_business_principle_signature_emptyUrl == $('.client_business_principle_signature').jqSignature('getDataURL')){
                var client_business_principle_signature = document.getElementsByClassName('client_business_principle_signature')[0];
                client_business_principle_signature.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert("Please sign your name in the Client's Business Principle Signature!");
                e.preventDefault();
                return
            }
            if (signature_emptyUrl == $('.signature').jqSignature('getDataURL')){
                var signature = document.getElementsByClassName('signature')[0];
                signature.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert("Please sign your name in the from Application Signature!");
                e.preventDefault();
                return
            }
            if (!$('#customer_id').val()) {

                var customer_id = document.getElementById("customer_id");
                customer_id.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your customer id !');
                e.preventDefault();
                return
            }
            if (!$('#owner_name').val()) {

                var owner_name = document.getElementById("owner_name");
                owner_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner name !');
                e.preventDefault();
                return
            }
            if (!$('#cell_phone_number').val()) {

                var owner_name = document.getElementById("cell_phone_number");
                owner_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your cell phone number !');
                e.preventDefault();
                return
            }
            if (!$('#email').val()) {

                var email = document.getElementById("email");
                email.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your email !');
                e.preventDefault();
                return
            }
            if (!$('#dba').val()) {

                var dba = document.getElementById("dba");
                dba.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your dba !');
                e.preventDefault();
                return
            }
            if (!$('#business_phone_number').val()) {
                alert('Enter your business phone number !');
                var business_phone_number = document.getElementById("business_phone_number");
                business_phone_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                e.preventDefault();
                return
            }
            if (!$('#company_address').val()) {
                var company_address = document.getElementById("company_address");
                company_address.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your company address !');
                e.preventDefault();
                return
            }
            if (!$('#restaurant_city').val()) {
                var restaurant_city = document.getElementById("restaurant_city");
                restaurant_city.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your restaurant city !');
                e.preventDefault();
                return
            }
            if (!$('#restaurant_state').val()) {
                var restaurant_state = document.getElementById("restaurant_state");
                restaurant_state.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your restaurant state !');
                e.preventDefault();
                return
            }
            if (!$('#restaurant_zipcode').val()) {
                var restaurant_zipcode = document.getElementById("restaurant_zipcode");
                restaurant_zipcode.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your restaurant zipcode!');
                e.preventDefault();
                return
            }
            if (!$('#lunch_hours').val()) {
                var lunch_hours = document.getElementById("lunch_hours");
                lunch_hours.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your lunch hours!');
                e.preventDefault();
                return
            }

            if (!$('#sales_tax').val()) {
                var sales_tax = document.getElementById("sales_tax");
                sales_tax.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your sales tax!');
                e.preventDefault();
                return
            }

            if (!$("input:radio[name='plan_choice']").is(":checked")){
                var plan_choice1 = document.getElementById("plan_choice1");
                plan_choice1.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Check the plan choice !');
                e.preventDefault();
                return
            }
            if (!$('#backup_phone').val()) {
                var backup_phone = document.getElementById("backup_phone");
                backup_phone.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your backup phone!');
                e.preventDefault();
                return
            }
            if ($("input[name=payment_option][value='2']").prop("checked") || $("input[name=payment_option][value='1']").prop("checked"))
            {
                if (!$('#company_name').val()) {
                    var company_name = document.getElementById("company_name");
                    company_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Enter your company name!');
                    e.preventDefault();
                    return
                }
                if (!$('#ssn').val()) {
                    var ssn = document.getElementById("ssn");
                    ssn.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Enter your ssn!');
                    e.preventDefault();
                    return
                }
                if (!$('#tax_id').val()) {
                    var tax_id = document.getElementById("tax_id");
                    tax_id.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Enter your tax id!');
                    e.preventDefault();
                    return
                }
                if ($('#owner_id').get(0).files.length === 0) {
                    var owner_id = document.getElementById("owner_id");
                    owner_id.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Upload the owner id document!');
                    e.preventDefault();
                    return
                }
                 if ($('#irs_document').get(0).files.length === 0) {
                    var irs_document = document.getElementById("irs_document");
                    irs_document.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Upload the irs document !');
                    e.preventDefault();
                    return
                }
                if (pricing_confirmation_signature_emptyUrl == $('.pricing_confirmation_signature').jqSignature('getDataURL')){
                    var pricing_confirmation_signature = document.getElementsByClassName('pricing_confirmation_signature')[0];
                    pricing_confirmation_signature.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert("Please sign your name in the Pricing Confirmation Signature!");
                    e.preventDefault();
                    return
                }
                if (!$("input:radio[name='is_confirm']").is(":checked")){
                    var is_confirm = document.getElementById("is_confirm");
                    is_confirm.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Please confirm the pricing condition !');
                    e.preventDefault();
                    return
                }
            }
            if (!$('#account_number').val()) {
                var account_number = document.getElementById("account_number");
                account_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your account number!');
                e.preventDefault();
                return
            }
            if (!$('#routing_number').val()) {
                var routing_number = document.getElementById("routing_number");
                routing_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your routing number!');
                e.preventDefault();
                return
            }
            if ($('#menu').get(0).files.length === 0) {
                var menu = document.getElementById("menu");
                menu.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Upload the menu document !');
                e.preventDefault();
                return
            }
            if ($('#void_check').get(0).files.length === 0) {
                var void_check = document.getElementById("void_check");
                void_check.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Upload the void check document!');
                e.preventDefault();
                return
            }

            if (!$('#from_application_signature_date').val()) {
                var from_application_signature_date = document.getElementById("from_application_signature_date");
                from_application_signature_date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your from application signature date!');
                e.preventDefault();
                return
            }
            if (!$('#print_client_business_legal_name').val()) {
                var print_client_business_legal_name = document.getElementById("print_client_business_legal_name");
                print_client_business_legal_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your from print client business legal name!');
                e.preventDefault();
                return
            }
            if (!$('#personal_guarantee_signature_date').val()) {
                var personal_guarantee_signature_date = document.getElementById("personal_guarantee_signature_date");
                personal_guarantee_signature_date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your personal guarantee signature date!');
                e.preventDefault();
                return
            }
            if (!$('#client_business_principle_sign_date').val()) {
                var client_business_principle_sign_date = document.getElementById("client_business_principle_sign_date");
                client_business_principle_sign_date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your client business principle sign date!');
                e.preventDefault();
                return
            }
            if (!$('#client_business_principle_title').val()) {
                var client_business_principle_title = document.getElementById("client_business_principle_title");
                client_business_principle_title.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your client business principle title!');
                e.preventDefault();
                return
            }
            if (!$('#print_name_of_signer').val()) {
                var print_name_of_signer = document.getElementById("print_name_of_signer");
                print_name_of_signer.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your print name of signer!');
                e.preventDefault();
                return
            }
            if (!$('#date').val()) {
                var date = document.getElementById("date");
                date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your date!');
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='online_order_terms']").is(":checked")){
                var online_order_terms = document.getElementById("online_order_terms");
                online_order_terms.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Check the online order terms !');
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='need_chinese']").is(":checked")){
                var need_chinese1 = document.getElementById("need_chinese1");
                need_chinese1.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Check the weather need chinese !');
                e.preventDefault();
                return
            }
            const fd = new FormData();
            fd.append('pricing_confirmation_signature', $('.pricing_confirmation_signature').jqSignature('getDataURL'));
            fd.append('from_application_signature', $('.from_application_signature').jqSignature('getDataURL'));
            fd.append('personal_guarantee_signature', $('.personal_guarantee_signature').jqSignature('getDataURL'));
            fd.append('client_initials', $('.client_initials').jqSignature('getDataURL'));
            fd.append('client_business_principle_signature', $('.client_business_principle_signature').jqSignature('getDataURL'));
            fd.append('signature', $('.signature').jqSignature('getDataURL'));

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

            fd.append('customer_id', $('#customer_id').val());
            fd.append('pos_system', $('#pos_system').val());
            fd.append('need_website', $('input[name="need_website"]:checked').val());

            fd.append('website_address', $('#website_address').val());
            fd.append('owner_name', $('#owner_name').val());
            fd.append('cell_phone_number', $('#cell_phone_number').val());
            fd.append('email', $('#email').val());

            fd.append('wechat', $('#wechat').val());
            fd.append('dba', $('#dba').val());
            fd.append('business_phone_number', $('#business_phone_number').val());
            fd.append('company_address', $('#company_address').val());
            fd.append('restaurant_city', $('#restaurant_city').val());
            fd.append('restaurant_state', $('#restaurant_state').val());
            fd.append('restaurant_zipcode', $('#restaurant_zipcode').val());
            fd.append('lunch_hours', $('#lunch_hours').val());
            fd.append('sales_tax', $('#sales_tax').val());
            fd.append('need_chinese', $('input[name="need_chinese"]:checked').val());
            fd.append('language', $('#language').val());
            fd.append('service_type', $('#service_type').val());
            fd.append('plan_choice', $('input[name="plan_choice"]:checked').val());
            fd.append('backup_phone', $('#backup_phone').val());

            fd.append('delivery_zone', $('#delivery_zone').val());
            fd.append('delivery_fee', $('#delivery_fee').val());
            fd.append('minimum_order_amount', $('#minimum_order_amount').val());
            fd.append('free_delivering_minimum_amount', $('#free_delivering_minimum_amount').val());

            fd.append('payment_option', $('input[name="payment_option"]:checked').val());
            fd.append('if_cash_discount', $('input[name="if_cash_discount"]:checked').val());

            fd.append('company_name', $('#company_name').val());
            fd.append('ssn', $('#ssn').val());
            fd.append('tax_id', $('#tax_id').val());
            fd.append('is_confirm', $('input[name="is_confirm"]:checked').val());

            fd.append('account_number', $('#account_number').val());
            fd.append('routing_number', $('#routing_number').val());
            fd.append('note', $('#note').val());
            fd.append('agent_name', $('#agent_name').val());
            fd.append('agent_email', $('#agent_email').val());

            fd.append('from_application_signature_date', $('#from_application_signature_date').val());
            fd.append('personal_guarantee_signature_date', $('#personal_guarantee_signature_date').val());
            fd.append('print_client_business_legal_name', $('#print_client_business_legal_name').val());
            fd.append('print_name_of_signer', $('#print_name_of_signer').val());
            fd.append('client_business_principle_title', $('#client_business_principle_title').val());
            fd.append('client_business_principle_sign_date', $('#client_business_principle_sign_date').val());
            fd.append('date', $('#date').val());

            fd.append('csrf_token', $('#csrf_token').val());
            var arr = window.location.href.split('/');
            var id = arr[arr.length-1];
            if (isInDesiredForm(id)){
                fd.append('id', parseInt(id));
            }
            $("#loading").removeAttr("hidden");
            $.ajax({url: "/application_kwickpos_online_ordering/submit",
                    type: 'POST',
                    data: fd,
                    processData: false,
                    contentType: false,
                    success: function(result){
                        if (result.results.code=="201"){
                            alert(result.results.message);
                            location.href = currentUrl;
                        }
                        else{
                            alert(result.results.message);
                        }
            }});
//            console.log("\n\n\n------", data_dict)
            e.preventDefault();
        });

        $('#kwickpos_online_order_sharing_link').on('click', function(e) {

            if (!$('#customer_id').val()) {
                var customer_id = document.getElementById("customer_id");
                customer_id.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your customer id !');
                e.preventDefault();
                return
            }
            if (!$('#owner_name').val()) {
                var owner_name = document.getElementById("owner_name");
                owner_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner name !');
                e.preventDefault();
                return
            }
            if (!$('#cell_phone_number').val()) {
                var cell_phone_number = document.getElementById("cell_phone_number");
                cell_phone_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your cell phone number !');
                e.preventDefault();
                return
            }
            if (!$('#email').val()) {
                var email = document.getElementById("email");
                email.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your email !');
                e.preventDefault();
                return
            }
            if (!$('#dba').val()) {
                var dba = document.getElementById("dba");
                dba.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your dba !');
                e.preventDefault();
                return
            }
            if (!$('#business_phone_number').val()) {
                var business_phone_number = document.getElementById("business_phone_number");
                business_phone_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your business phone number !');
                e.preventDefault();
                return
            }
            if (!$('#company_address').val()) {
                var company_address = document.getElementById("company_address");
                company_address.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your company address !');
                e.preventDefault();
                return
            }
            if (!$('#restaurant_city').val()) {
                var restaurant_city = document.getElementById("restaurant_city");
                restaurant_city.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your restaurant city !');
                e.preventDefault();
                return
            }
            if (!$('#restaurant_state').val()) {
                var restaurant_state = document.getElementById("restaurant_state");
                restaurant_state.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your restaurant state !');
                e.preventDefault();
                return
            }
            if (!$('#restaurant_zipcode').val()) {
                var restaurant_zipcode = document.getElementById("restaurant_zipcode");
                restaurant_zipcode.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your restaurant zipcode!');
                e.preventDefault();
                return
            }
            if (!$('#lunch_hours').val()) {
                var lunch_hours = document.getElementById("lunch_hours");
                lunch_hours.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your lunch hours!');
                e.preventDefault();
                return
            }

            if (!$('#sales_tax').val()) {
                var sales_tax = document.getElementById("sales_tax");
                sales_tax.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your sales tax!');
                e.preventDefault();
                return
            }

            if (!$("input:radio[name='plan_choice']").is(":checked")){
                var plan_choice1 = document.getElementById("plan_choice1");
                plan_choice1.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Check the plan choice !');
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='need_chinese']").is(":checked")){
                var need_chinese1 = document.getElementById("need_chinese1");
                need_chinese1.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Check the weather need chinese !');
                e.preventDefault();
                return
            }

            if (!$("input:radio[name='is_confirm']").is(":checked")){
                var is_confirm = document.getElementById("is_confirm");
                is_confirm.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Check the  is confirm !');
                e.preventDefault();
                return
            }
            if (!$('#backup_phone').val()) {
                var backup_phone = document.getElementById("backup_phone");
                backup_phone.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your backup phone!');
                e.preventDefault();
                return
            }
            if ($("input[name=payment_option][value='2']").prop("checked"))
            {
                if (!$('#company_name').val()) {
                    var company_name = document.getElementById("company_name");
                    company_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Enter your company name!');
                    e.preventDefault();
                    return
                }
                if (!$('#ssn').val()) {
                    var ssn = document.getElementById("ssn");
                    ssn.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Enter your ssn!');
                    e.preventDefault();
                    return
                }
                if (!$('#tax_id').val()) {
                    var tax_id = document.getElementById("tax_id");
                    tax_id.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Enter your tax id!');
                    e.preventDefault();
                    return
                }
            }
            if (!$('#account_number').val()) {
                var account_number = document.getElementById("account_number");
                account_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your account number!');
                e.preventDefault();
                return
            }
            if (!$('#routing_number').val()) {
                var routing_number = document.getElementById("routing_number");
                routing_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your routing number!');
                e.preventDefault();
                return
            }

            if (!$('#print_client_business_legal_name').val()) {
                var print_client_business_legal_name = document.getElementById("print_client_business_legal_name");
                print_client_business_legal_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your from print client business legal name!');
                e.preventDefault();
                return
            }
            if (!$('#from_application_signature_date').val()) {
                var from_application_signature_date = document.getElementById("from_application_signature_date");
                from_application_signature_date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your from application signature date!');
                e.preventDefault();
                return
            }
            if (!$('#personal_guarantee_signature_date').val()) {
                var personal_guarantee_signature_date = document.getElementById("personal_guarantee_signature_date");
                personal_guarantee_signature_date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your personal guarantee signature date!');
                e.preventDefault();
                return
            }
            if (!$('#client_business_principle_sign_date').val()) {
                var client_business_principle_sign_date = document.getElementById("client_business_principle_sign_date");
                client_business_principle_sign_date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your client business principle sign date!');
                e.preventDefault();
                return
            }
            if (!$('#print_name_of_signer').val()) {
                var print_name_of_signer = document.getElementById("print_name_of_signer");
                print_name_of_signer.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your print name of signer!');
                e.preventDefault();
                return
            }
            if (!$('#client_business_principle_title').val()) {
                var client_business_principle_title = document.getElementById("client_business_principle_title");
                client_business_principle_title.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your client business principle title!');
                e.preventDefault();
                return
            }
            if (!$('#date').val()) {
                var date = document.getElementById("date");
                date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your date!');
                e.preventDefault();
                return
            }

            const fd = new FormData();
            fd.append('pricing_confirmation_signature', $('.pricing_confirmation_signature').jqSignature('getDataURL'));
            fd.append('from_application_signature', $('.from_application_signature').jqSignature('getDataURL'));
            fd.append('personal_guarantee_signature', $('.personal_guarantee_signature').jqSignature('getDataURL'));
            fd.append('client_initials', $('.client_initials').jqSignature('getDataURL'));
            fd.append('client_business_principle_signature', $('.client_business_principle_signature').jqSignature('getDataURL'));
            fd.append('signature', $('.signature').jqSignature('getDataURL'));
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


            fd.append('customer_id', $('#customer_id').val());
            fd.append('pos_system', $('#pos_system').val());
            fd.append('need_website', $('input[name="need_website"]:checked').val());

            fd.append('website_address', $('#website_address').val());
            fd.append('owner_name', $('#owner_name').val());
            fd.append('cell_phone_number', $('#cell_phone_number').val());
            fd.append('email', $('#email').val());

            fd.append('wechat', $('#wechat').val());
            fd.append('dba', $('#dba').val());
            fd.append('business_phone_number', $('#business_phone_number').val());
            fd.append('company_address', $('#company_address').val());
            fd.append('restaurant_city', $('#restaurant_city').val());
            fd.append('restaurant_state', $('#restaurant_state').val());
            fd.append('restaurant_zipcode', $('#restaurant_zipcode').val());
            fd.append('lunch_hours', $('#lunch_hours').val());
            fd.append('sales_tax', $('#sales_tax').val());
            fd.append('need_chinese', $('input[name="need_chinese"]:checked').val());
            if (!$('#language').val()) {
                fd.append('language', $('#language').val());
            }

            fd.append('service_type', $('#service_type').val());
            fd.append('plan_choice', $('input[name="plan_choice"]:checked').val());
            fd.append('backup_phone', $('#backup_phone').val());

            fd.append('delivery_zone', $('#delivery_zone').val());
            fd.append('delivery_fee', $('#delivery_fee').val());
            fd.append('minimum_order_amount', $('#minimum_order_amount').val());
            fd.append('free_delivering_minimum_amount', $('#free_delivering_minimum_amount').val());

            fd.append('payment_option', $('input[name="payment_option"]:checked').val());
            fd.append('if_cash_discount', $('input[name="if_cash_discount"]:checked').val());

            fd.append('company_name', $('#company_name').val());
            fd.append('ssn', $('#ssn').val());
            fd.append('tax_id', $('#tax_id').val());
            fd.append('is_confirm', $('input[name="is_confirm"]:checked').val());

            fd.append('account_number', $('#account_number').val());
            fd.append('routing_number', $('#routing_number').val());
            fd.append('note', $('#note').val());
            fd.append('agent_name', $('#agent_name').val());
            fd.append('agent_email', $('#agent_email').val());

            fd.append('from_application_signature_date', $('#from_application_signature_date').val());
            fd.append('personal_guarantee_signature_date', $('#personal_guarantee_signature_date').val());
            fd.append('print_client_business_legal_name', $('#print_client_business_legal_name').val());
            fd.append('print_name_of_signer', $('#print_name_of_signer').val());
            fd.append('client_business_principle_title', $('#client_business_principle_title').val());
            fd.append('client_business_principle_sign_date', $('#client_business_principle_sign_date').val());
            fd.append('date', $('#date').val());
            fd.append('csrf_token', $('#csrf_token').val());

            fd.append('sharing_link', '1');
            $.ajax({url: "/application_kwickpos_online_ordering/submit",
                    type: 'POST',
                    data: fd,
                    processData: false,
                    contentType: false,
                    success: function(result){
//                        $("html").html(result);
                        if (result.results.code=="200"){
                            navigator.clipboard.writeText(result.results.url);
                            alert('Share cart link copied to clipboard.');
                        }
                        else{
                            alert('Something went wrong...');
                        }
            }});

            e.preventDefault();
        });
    });
});
