odoo.define('website_application.merchant', function (require) {
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

        if ($("input[name=standalone_or_semi][value='1']").prop("checked"))
              {
                $("#div_standalone_or_semi").removeAttr("hidden");
                $("#div_specify_your_equipment_type").removeAttr("hidden");
              }
        if ($("input[name=standalone_or_semi][value='2']").prop("checked"))
          {
            $("#div_standalone_or_semi").attr("hidden",'hidden');
            $("#div_specify_your_equipment_type").removeAttr("hidden");
          }
        $('#completely_fill').click(function(e) {
            if (!$("input:radio[name='account_type']").is(":checked")){
                document.getElementById("account_type1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the account type!');
                e.preventDefault();
                return
            }

            if (!$("input:radio[name='standalone_or_semi']").is(":checked")){
                document.getElementById("standalone_or_semi1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the standalone or semi !');
                e.preventDefault();
                return
            }
            if ($("input[name=standalone_or_semi][value='1']").prop("checked")){
                if (!$("input:radio[name='bill_to']").is(":checked")){
                    document.getElementById("bill_to1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Choose the bill to !');
                    e.preventDefault();
                    return
                }
            }

            if (!$("input:radio[name='deployment_method']").is(":checked")){
                document.getElementById("deployment_method1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the deployment method !');
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='pricing_type']").is(":checked")){
                document.getElementById("pricing_type1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the pricing type !');
                e.preventDefault();
                return
            }
            if ($("#verify_information").is(':checked') && $("#completely_fill").is(':checked')) {
                $("#hidden_for_merchant").attr("hidden",'hidden');
            }
        });
        $('#verify_information').click(function(e) {
            if (!$("input:radio[name='account_type']").is(":checked")){
                document.getElementById("account_type1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the account type!');
                e.preventDefault();
                return
            }

            if (!$("input:radio[name='standalone_or_semi']").is(":checked")){
                document.getElementById("standalone_or_semi1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the standalone or semi !');
                e.preventDefault();
                return
            }
            if ($("input[name=standalone_or_semi][value='1']").prop("checked")){
                if (!$("input:radio[name='bill_to']").is(":checked")){
                    document.getElementById("bill_to1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Choose the bill to !');
                    e.preventDefault();
                    return
                }
            }
            if (!$("input:radio[name='deployment_method']").is(":checked")){
                document.getElementById("deployment_method1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the deployment method !');
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='pricing_type']").is(":checked")){
                document.getElementById("pricing_type1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the pricing type !');
                e.preventDefault();
                return
            }
            if ($("#verify_information").is(':checked') && $("#completely_fill").is(':checked')) {
                $("#hidden_for_merchant").attr("hidden",'hidden');
            }
        });

        $('.signature').jqSignature({autoFit: true,lineWidth: 3});
        $('.personal_guarantee_signature').jqSignature({autoFit: true,lineWidth: 3});
        $('.client_initials_signature').jqSignature({autoFit: true,lineWidth: 3});
        $('.client_business_principle_signature').jqSignature({autoFit: true,lineWidth: 3});

        var signature_emptyUrl = $('.signature').jqSignature('getDataURL');
        var personal_guarantee_signature_emptyUrl = $('.personal_guarantee_signature').jqSignature('getDataURL');
        var client_initials_signature_emptyUrl = $('.client_initials_signature').jqSignature('getDataURL');
        var client_business_principle_signature_emptyUrl = $('.client_business_principle_signature').jqSignature('getDataURL');

         $("#signature_clear").click(function( e ) {
            $('.signature').jqSignature('clearCanvas');
            e.preventDefault();
		});
        $("#personal_guarantee_signature_clear").click(function( e ) {
    		$('.personal_guarantee_signature').jqSignature('clearCanvas');
    		e.preventDefault();
		});
		$("#client_initials_signature_clear").click(function( e ) {
    		$('.client_initials_signature').jqSignature('clearCanvas');
    		e.preventDefault();
		});
		$("#client_business_principle_signature_clear").click(function( e ) {
    		$('.client_business_principle_signature').jqSignature('clearCanvas');
    		e.preventDefault();
		});
        $('#feature_ip').click(function() {
            $("#feature_ip_input").toggle();
        });
        $('#feature_auto_batch').click(function() {
            $("#feature_auto_batch_time_input").toggle();
        });
        $('#feature_tip_suggestions').click(function() {
            $("#feature_tip_suggestions_input").toggle();
        });
        $('#feature_other_feature').click(function() {
            $("#feature_other_feature_input").toggle();
        });
        $( "input[name=account_type]" ).change(function() {
            if ($("input[name=account_type][value='1']").prop("checked"))
              {
                $("#div_account_type").attr("hidden",'hidden');
              }
            if ($("input[name=account_type][value='2']").prop("checked"))
              {
                $("#div_account_type").removeAttr("hidden");
              }
             if ($("input[name=account_type][value='3']").prop("checked"))
              {
                $("#div_account_type").removeAttr("hidden");
              }
        });
        $( "input[name=standalone_or_semi]" ).change(function() {
            if ($("input[name=standalone_or_semi][value='1']").prop("checked"))
              {
                $("#div_standalone_or_semi").removeAttr("hidden");
                $("#div_specify_your_equipment_type").removeAttr("hidden");
              }
            if ($("input[name=standalone_or_semi][value='2']").prop("checked"))
              {
                $("#div_standalone_or_semi").attr("hidden",'hidden');
                $("#div_specify_your_equipment_type").removeAttr("hidden");
              }
        });
        $( "input[name=deployment_method]" ).change(function() {
            if ($("input[name=deployment_method][value='1']").prop("checked"))
              {
                $("#div_deployment_method_ship_to").attr("hidden",'hidden');
                $("#div_reprogram_old_mid").attr("hidden",'hidden');
              }
            if ($("input[name=deployment_method][value='2']").prop("checked"))
            {
                $("#div_deployment_method_ship_to").attr("hidden",'hidden');
                $("#div_reprogram_old_mid").attr("hidden",'hidden');
            }
            if ($("input[name=deployment_method][value='3']").prop("checked"))
            {
                $("#div_deployment_method_ship_to").attr("hidden",'hidden');
                $("#div_reprogram_old_mid").attr("hidden",'hidden');
            }
            if ($("input[name=deployment_method][value='4']").prop("checked"))
            {
                $("#div_deployment_method_ship_to").removeAttr("hidden");
                $("#div_reprogram_old_mid").attr("hidden",'hidden');
            }
            if ($("input[name=deployment_method][value='5']").prop("checked"))
            {
                $("#div_deployment_method_ship_to").removeAttr("hidden");
                $("#ship_out_address").attr("required","");
                $("#ship_out_city").attr("required","");
                $("#ship_out_zip").attr("required","");
                $("#ship_out_state").attr("required","");
                $("#div_reprogram_old_mid").attr("hidden",'hidden');

            }
            if ($("input[name=deployment_method][value='6']").prop("checked"))
            {
                $("#div_deployment_method_ship_to").attr("hidden",'hidden');
                $("#div_reprogram_old_mid").removeAttr("hidden");
            }

        });
        $( "input[name=pricing_type]" ).change(function() {
            if ($("input[name=pricing_type][value='1']").prop("checked"))
              {
                $("#div_pricing_type_1_2").removeAttr("hidden");
                $("#div_pricing_type_3_4").attr("hidden",'hidden');
                $('#monthly_fee').attr('value', '25');
              }
            if ($("input[name=pricing_type][value='2']").prop("checked"))
            {
                $("#div_pricing_type_1_2").removeAttr("hidden");
                $("#div_pricing_type_3_4").attr("hidden",'hidden');
                $('#monthly_fee').attr('value', '25');
            }
            if ($("input[name=pricing_type][value='3']").prop("checked"))
            {
                $("#div_pricing_type_1_2").attr("hidden",'hidden');
                $("#div_pricing_type_3_4").removeAttr("hidden");
                $('#monthly_fee').attr('value', '35');
            }
            if ($("input[name=pricing_type][value='4']").prop("checked"))
            {
                $("#div_pricing_type_1_2").attr("hidden",'hidden');
                $("#div_pricing_type_3_4").removeAttr("hidden");
                $('#monthly_fee').attr('value', '35');

            }

        });
        $( "input[name=if_want_free_cash_discount]" ).change(function() {
            if ($("input[name=if_want_free_cash_discount][value='1']").prop("checked"))
            {
                $("#div_if_want_free_cash_discount").removeAttr("hidden");

            }
            if ($("input[name=if_want_free_cash_discount][value='2']").prop("checked"))
            {
                $("#div_if_want_free_cash_discount").attr("hidden",'hidden');
            }

        });
        $('#sumit_merchant_application').on('click', function(e) {
             if (!$('#agent_name').val()) {
                var agent_name = document.getElementById("agent_name");
                agent_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your agent name!');
                e.preventDefault();
                return
            }
            if (!$('#agent_email').val()) {
                var agent_email = document.getElementById("agent_email");
                agent_email.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your agent email!');
                e.preventDefault();
                return
            }
            if (!$('#name_of_company').val()) {
                var name_of_company = document.getElementById("name_of_company");
                name_of_company.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your name of company!');
                e.preventDefault();
                return
            }
            if (!$('#dba').val()) {
                var dba = document.getElementById("dba");
                dba.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your Doing Business As!');
                e.preventDefault();
                return
            }
            if (!$('#address').val()) {
                var address = document.getElementById("address");
                address.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your address!');
                e.preventDefault();
                return
            }
            if (!$('#city').val()) {
                var city = document.getElementById("city");
                city.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your city!');
                e.preventDefault();
                return
            }
            if (!$('#state').val()) {
                var state = document.getElementById("state");
                state.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your state!');
                e.preventDefault();
                return
            }
            if (!$('#zip_code').val()) {
                var zip_code = document.getElementById("zip_code");
                zip_code.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your zip code!');
                e.preventDefault();
                return
            }
            if (!$('#business_phone_number').val()) {
                var business_phone_number = document.getElementById("business_phone_number");
                business_phone_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your business phone number!');
                e.preventDefault();
                return
            }

            if (!$('#federal_tax_id').val()) {
                var federal_tax_id = document.getElementById("federal_tax_id");
                federal_tax_id.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your federal tax id!');
                e.preventDefault();
                return
            }
            if (!$('#type_of_business').val()) {
                var type_of_business = document.getElementById("type_of_business");
                type_of_business.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your type of business!');
                e.preventDefault();
                return
            }
            if (!$('#open_date').val()) {
                var open_date = document.getElementById("open_date");
                open_date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your open date!');
                e.preventDefault();
                return
            }
            if (!$('#estimated_monthly_sale_volume').val()) {
                var estimated_monthly_sale_volume = document.getElementById("estimated_monthly_sale_volume");
                estimated_monthly_sale_volume.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your estimated monthly sale volume!');
                e.preventDefault();
                return
            }
            if (!$('#average_sales_account').val()) {
                var average_sales_account = document.getElementById("average_sales_account");
                average_sales_account.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your average sales account!');
                e.preventDefault();
                return
            }
            if (!$('#owner_name').val()) {
                var owner_name = document.getElementById("owner_name");
                owner_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner name!');
                e.preventDefault();
                return
            }
            if (!$('#owner_email').val()) {
                var owner_email = document.getElementById("owner_email");
                owner_email.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner email!');
                e.preventDefault();
                return
            }
            if (!$('#owner_title').val()) {
                var owner_title = document.getElementById("owner_title");
                owner_title.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner title!');
                e.preventDefault();
                return
            }
            if (!$('#owner_phone_number').val()) {
                var owner_phone_number = document.getElementById("owner_phone_number");
                owner_phone_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner phone number!');
                e.preventDefault();
                return
            }
            if (!$('#owner_home_address').val()) {
                var owner_home_address = document.getElementById("owner_home_address");
                owner_home_address.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner home address!');
                e.preventDefault();
                return
            }
            if (!$('#owner_home_city').val()) {
                var owner_home_city = document.getElementById("owner_home_city");
                owner_home_city.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner city!');
                e.preventDefault();
                return
            }
            if (!$('#owner_home_state').val()) {
                var owner_home_state = document.getElementById("owner_home_state");
                owner_home_state.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner home state!');
                e.preventDefault();
                return
            }
            if (!$('#owner_home_zip_code').val()) {
                var owner_home_zip_code = document.getElementById("owner_home_zip_code");
                owner_home_zip_code.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner home zip code!');
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
            if (!$('#owner_date_of_birth').val()) {
                var owner_date_of_birth = document.getElementById("owner_date_of_birth");
                owner_date_of_birth.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner date of birth!');
                e.preventDefault();
                return
            }
            if (!$('#owner_driver_license_number').val()) {
                var owner_driver_license_number = document.getElementById("owner_driver_license_number");
                owner_driver_license_number.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner driver license number!');
                e.preventDefault();
                return
            }
            if (!$('#owner_state_issued').val()) {
                var owner_state_issued = document.getElementById("owner_state_issued");
                owner_state_issued.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner state issued!');
                e.preventDefault();
                return
            }
            if (!$('#owner_bank_name').val()) {
                var owner_bank_name = document.getElementById("owner_bank_name");
                owner_bank_name.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner bank name!');
                e.preventDefault();
                return
            }
            if (!$('#owner_bank_routing').val()) {
                var owner_bank_routing = document.getElementById("owner_bank_routing");
                owner_bank_routing.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner bank routing!');
                e.preventDefault();
                return
            }
            if (!$('#owner_bank_account').val()) {
                var owner_bank_account = document.getElementById("owner_bank_account");
                owner_bank_account.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner bank account!');
                e.preventDefault();
                return
            }
            if (!$('#sign_date').val()) {
                var sign_date = document.getElementById("sign_date");
                sign_date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner sign date!');
                e.preventDefault();
                return
            }

            if (!$("#completely_fill").is(':checked')) {
                var completely_fill = document.getElementById("completely_fill");
                completely_fill.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('check the agreement!');
                e.preventDefault();
                return
            }
            if (!$("#verify_information").is(':checked')) {
                var verify_information = document.getElementById("verify_information");
                verify_information.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('check the agreement!');
                e.preventDefault();
                return
            }
            if (!$('#personal_guarantee_sign_date').val()) {
                var personal_guarantee_sign_date = document.getElementById("personal_guarantee_sign_date");
                personal_guarantee_sign_date.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner personal guarantee sign date!');
                e.preventDefault();
                return
            }
            if (!$('#print_client_business_legal_name').val()) {
                document.getElementById("print_client_business_legal_name").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner print client business legal name!');
                e.preventDefault();
                return
            }
            if (!$('#print_name_signer').val()) {
                document.getElementById("print_name_signer").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner print name signer!');
                e.preventDefault();
                return
            }
            if (!$('#business_principle_title').val()) {
                document.getElementById("business_principle_title").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner business principle title!');
                e.preventDefault();
                return
            }
            if (!$('#business_principle_sign_date').val()) {
                document.getElementById("business_principle_sign_date").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter business principle sign date!');
                e.preventDefault();
                return
            }
             if (!$("input:radio[name='standalone_or_semi']").is(":checked")){
                document.getElementById("standalone_or_semi1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the standalone or semi !');
                e.preventDefault();
                return
            }
            if ($("input[name=standalone_or_semi][value='1']").prop("checked")){
                if (!$("input:radio[name='bill_to']").is(":checked")){
                    document.getElementById("bill_to1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Choose the bill to !');
                    e.preventDefault();
                    return
                }
            }
            if (!$("input:radio[name='account_type']").is(":checked")){
                document.getElementById("account_type1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the account type !');
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='deployment_method']").is(":checked")){
                document.getElementById("deployment_method1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the deployment method !');
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='pricing_type']").is(":checked")){
                document.getElementById("pricing_type1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the pricing type !');
                e.preventDefault();
                return
            }

            if ($('input[name="if_want_free_cash_discount"]:checked').val()=='1'){
                if ($('#menu_document').get(0).files.length === 0) {
                    document.getElementById("menu_document").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Upload the menu document !');
                    e.preventDefault();
                    return
                }
            }
            if ($('#void_check_document').get(0).files.length === 0) {
                    document.getElementById("void_check_document").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Upload the void check document !');
                    e.preventDefault();
                    return
            }
            if ($('#owner_id_document').get(0).files.length === 0) {
                    document.getElementById("owner_id_document").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Upload the owner id document !');
                    e.preventDefault();
                    return
            }
            if ($('#irs_document').get(0).files.length === 0) {
                    document.getElementById("irs_document").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Upload the irs document !');
                    e.preventDefault();
                    return
            }
            if (signature_emptyUrl == $('.signature').jqSignature('getDataURL')){
                document.getElementsByClassName('signature')[0].scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert("Please sign your name in the Signature!");
                e.preventDefault();
                return
            }
            if (personal_guarantee_signature_emptyUrl == $('.personal_guarantee_signature').jqSignature('getDataURL')){
                document.getElementsByClassName('personal_guarantee_signature')[0].scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert("Please sign your name in the personal guarantee signature!");
                e.preventDefault();
                return
            }
            if (client_initials_signature_emptyUrl == $('.client_initials_signature').jqSignature('getDataURL')){
                document.getElementsByClassName('client_initials_signature')[0].scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert("Please sign your name in the client initials signature!");
                e.preventDefault();
                return
            }
            if (client_business_principle_signature_emptyUrl == $('.client_business_principle_signature').jqSignature('getDataURL')){
                document.getElementsByClassName('client_business_principle_signature')[0].scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert("Please sign your name in the client business principle signature!");
                e.preventDefault();
                return
            }
            const fd = new FormData();
            fd.append('signature', $('.signature').jqSignature('getDataURL'));
            fd.append('personal_guarantee_signature', $('.personal_guarantee_signature').jqSignature('getDataURL'));
            fd.append('client_initials_signature', $('.client_initials_signature').jqSignature('getDataURL'));
            fd.append('client_business_principle_signature', $('.client_business_principle_signature').jqSignature('getDataURL'));

            if ($('input[name="if_want_free_cash_discount"]:checked').val()=='1'){
                if ($('#menu_document').get(0).files.length != 0) {
                    fd.append('menu_document', $('#menu_document')[0].files[0]);
                }
            }
            if ($('#void_check_document').get(0).files.length != 0) {
                    fd.append('void_check_document', $('#void_check_document')[0].files[0]);
            }
            if ($('#owner_id_document').get(0).files.length != 0) {
                    fd.append('owner_id_document', $('#owner_id_document')[0].files[0]);
            }
            if ($('#other_document').get(0).files.length != 0) {
                    fd.append('other_document', $('#other_document')[0].files[0]);
            }

            fd.append('account_type', $('input[name="account_type"]:checked').val());
            fd.append('old_mid', $('#old_mid').val());
            fd.append('is_add_paper_plan', $('input[name="is_add_paper_plan"]:checked').val());
            fd.append('checkbook', $("#checkbook").is(':checked'));
            fd.append('tips_trays', $("#tips_trays").is(':checked'));
            fd.append('no_supply_order_needed', $("#no_supply_order_needed").is(':checked'));
            fd.append('standalone_or_semi', $('input[name="standalone_or_semi"]:checked').val());
            fd.append('equipment_type', $('#equipment_type').val());
            fd.append('equipment', $('#equipment').val());
            fd.append('bill_to', $('input[name="bill_to"]:checked').val());
            fd.append('equipment_quantity', $('#equipment_quantity').val());
            fd.append('feature_restaurant', $("#feature_restaurant").is(':checked'));
            fd.append('feature_retail', $("#feature_retail").is(':checked'));
            fd.append('feature_with_tips', $("#feature_with_tips").is(':checked'));
            fd.append('feature_dial', $("#feature_dial").is(':checked'));
            fd.append('feature_pin_debit', $("#feature_pin_debit").is(':checked'));
            fd.append('feature_server_id', $("#feature_server_id").is(':checked'));
            fd.append('feature_ip', $("#feature_ip").is(':checked'));
            fd.append('feature_auto_time_batch', $("#feature_auto_time_batch").is(':checked'));
            fd.append('feature_tip_suggestions', $("#feature_tip_suggestions").is(':checked'));
            fd.append('feature_other_feature', $("#feature_other_feature").is(':checked'));
            fd.append('feature_ip_input', $('#feature_ip_input').val());
            fd.append('feature_auto_batch_time_input', $('#feature_auto_batch_time_input').val());
            fd.append('feature_tip_suggestions_input', $('#feature_tip_suggestions_input').val());
            fd.append('feature_other_feature_input', $('#feature_other_feature_input').val());

            fd.append('deployment_method', $('input[name="deployment_method"]:checked').val());
            fd.append('is_ship_with_pos', $('input[name="is_ship_with_pos"]:checked').val());
            fd.append('ship_out_address', $('#ship_out_address').val());
            fd.append('ship_out_city', $('#ship_out_city').val());
            fd.append('ship_out_zip', $('#ship_out_zip').val());
            fd.append('ship_out_state', $('#ship_out_state').val());

            fd.append('reprogram_old_mid', $('#reprogram_old_mid').val());
            fd.append('pricing_type', $('input[name="pricing_type"]:checked').val());
            fd.append('visa_sales_discount_fee', $('#visa_sales_discount_fee').val());
            fd.append('visa_auth_fee', $('#visa_auth_fee').val());
            fd.append('amex_sales_discount_fee', $('#amex_sales_discount_fee').val());
            fd.append('amex_auth_fee', $('#amex_auth_fee').val());
            fd.append('cash_discount_rate', $('#cash_discount_rate').val());
            fd.append('if_want_free_cash_discount', $('input[name="if_want_free_cash_discount"]:checked').val());
            fd.append('monthly_fee', $('#monthly_fee').val());
            fd.append('other_comment', $('#other_comment').val());
            fd.append('Date', $('#Date').val());

            fd.append('agent_name', $('#agent_name').val());
            fd.append('agent_email', $('#agent_email').val());
            fd.append('name_of_company', $('#name_of_company').val());
            fd.append('dba', $('#dba').val());
            fd.append('address', $('#address').val());
            fd.append('city', $('#city').val());
            fd.append('state', $('#state').val());
            fd.append('zip_code', $('#zip_code').val());
            fd.append('business_phone_number', $('#business_phone_number').val());
            fd.append('fax_number', $('#fax_number').val());
            fd.append('federal_tax_id', $('#federal_tax_id').val());
            fd.append('type_of_business', $('#type_of_business').val());
            fd.append('company_type', $('input[name="company_type"]:checked').val());
            fd.append('open_date', $('#open_date').val());
            fd.append('estimated_monthly_sale_volume', $('#estimated_monthly_sale_volume').val());
            fd.append('average_sales_account', $('#average_sales_account').val());
            fd.append('amex', $('input[name="amex"]:checked').val());

            fd.append('owner_name', $('#owner_name').val());
            fd.append('owner_email', $('#owner_email').val());
            fd.append('owner_title', $('#owner_title').val());
            fd.append('owner_phone_number', $('#owner_phone_number').val());
            fd.append('owner_home_address', $('#owner_home_address').val());
            fd.append('owner_home_city', $('#owner_home_city').val());
            fd.append('owner_home_state', $('#owner_home_state').val());
            fd.append('owner_home_zip_code', $('#owner_home_zip_code').val());
            fd.append('ssn', $('#ssn').val());
            fd.append('owner_date_of_birth', $('#owner_date_of_birth').val());
            fd.append('owner_driver_license_number', $('#owner_driver_license_number').val());
            fd.append('owner_state_issued', $('#owner_state_issued').val());
            fd.append('owner_bank_name', $('#owner_bank_name').val());
            fd.append('owner_bank_routing', $('#owner_bank_routing').val());
            fd.append('owner_bank_account', $('#owner_bank_account').val());

            fd.append('sign_date', $('#sign_date').val());
            fd.append('personal_guarantee_sign_date', $('#personal_guarantee_sign_date').val());
            fd.append('print_client_business_legal_name', $('#print_client_business_legal_name').val());
            fd.append('print_name_signer', $('#print_name_signer').val());
            fd.append('business_principle_title', $('#business_principle_title').val());
            fd.append('business_principle_sign_date', $('#business_principle_sign_date').val());


            var arr = window.location.href.split('/');
            var id = arr[arr.length-1];
            if (isInDesiredForm(id)){
                fd.append('id', parseInt(id));
            }
            $("#loading").removeAttr("hidden");
             $.ajax({url: "/application_new_merchant/submit",
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

        $('#sumit_merchant_application_share_link').on('click', function(e) {

             if (!$('#agent_name').val()) {
                document.getElementById("agent_name").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your agent name!');
                e.preventDefault();
                return
            }
            if (!$('#agent_email').val()) {
                document.getElementById("agent_email").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your agent email!');
                e.preventDefault();
                return
            }
            if (!$('#name_of_company').val()) {
                document.getElementById("name_of_company").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your name of company!');
                e.preventDefault();
                return
            }
            if (!$('#dba').val()) {
                document.getElementById("dba").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your Doing Business As!');
                e.preventDefault();
                return
            }
            if (!$('#address').val()) {
                document.getElementById("address").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your address!');
                e.preventDefault();
                return
            }
            if (!$('#city').val()) {
                document.getElementById("city").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your city!');
                e.preventDefault();
                return
            }
            if (!$('#state').val()) {
                document.getElementById("state").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your state!');
                e.preventDefault();
                return
            }
            if (!$('#zip_code').val()) {
                document.getElementById("zip_code").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your zip code!');
                e.preventDefault();
                return
            }
            if (!$('#business_phone_number').val()) {
                document.getElementById("business_phone_number").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your business phone number!');
                e.preventDefault();
                return
            }

            if (!$('#federal_tax_id').val()) {
                document.getElementById("federal_tax_id").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your federal tax id!');
                e.preventDefault();
                return
            }
            if (!$('#type_of_business').val()) {
                document.getElementById("type_of_business").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your type of business!');
                e.preventDefault();
                return
            }
            if (!$('#open_date').val()) {
                document.getElementById("open_date").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your open date!');
                e.preventDefault();
                return
            }
            if (!$('#estimated_monthly_sale_volume').val()) {
                document.getElementById("estimated_monthly_sale_volume").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your estimated monthly sale volume!');
                e.preventDefault();
                return
            }
            if (!$('#average_sales_account').val()) {
                document.getElementById("average_sales_account").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your average sales account!');
                e.preventDefault();
                return
            }
            if (!$('#owner_name').val()) {
                document.getElementById("owner_name").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner name!');
                e.preventDefault();
                return
            }
            if (!$('#owner_email').val()) {
                document.getElementById("owner_email").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner email!');
                e.preventDefault();
                return
            }
            if (!$('#owner_title').val()) {
                document.getElementById("owner_title").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner title!');
                e.preventDefault();
                return
            }
            if (!$('#owner_phone_number').val()) {
                document.getElementById("owner_phone_number").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner phone number!');
                e.preventDefault();
                return
            }
            if (!$('#owner_home_address').val()) {
                document.getElementById("owner_home_address").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner home address!');
                e.preventDefault();
                return
            }
            if (!$('#owner_home_city').val()) {
                document.getElementById("owner_home_city").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner city!');
                e.preventDefault();
                return
            }
            if (!$('#owner_home_state').val()) {
                document.getElementById("owner_home_state").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner home state!');
                e.preventDefault();
                return
            }
            if (!$('#owner_home_zip_code').val()) {
                document.getElementById("owner_home_zip_code").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner home zip code!');
                e.preventDefault();
                return
            }
            if (!$('#ssn').val()) {
                document.getElementById("ssn").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your ssn!');
                e.preventDefault();
                return
            }
            if (!$('#owner_date_of_birth').val()) {
                document.getElementById("owner_date_of_birth").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner date of birth!');
                e.preventDefault();
                return
            }
            if (!$('#owner_driver_license_number').val()) {
                document.getElementById("owner_driver_license_number").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner driver license number!');
                e.preventDefault();
                return
            }
            if (!$('#owner_state_issued').val()) {
                document.getElementById("owner_state_issued").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner state issued!');
                e.preventDefault();
                return
            }
            if (!$('#owner_bank_name').val()) {
                document.getElementById("owner_bank_name").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner bank name!');
                e.preventDefault();
                return
            }
            if (!$('#owner_bank_routing').val()) {
                document.getElementById("owner_bank_routing").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter your owner bank routing!');
                e.preventDefault();
                return
            }
            if (!$('#owner_bank_account').val()) {
                document.getElementById("owner_bank_account").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner bank account!');
                e.preventDefault();
                return
            }
            if (!$('#sign_date').val()) {
                document.getElementById("sign_date").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner sign date!');
                e.preventDefault();
                return
            }

            if (!$("#completely_fill").is(':checked')) {
                document.getElementById("completely_fill").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('check the agreement!');
                e.preventDefault();
                return
            }
            if (!$("#verify_information").is(':checked')) {
                document.getElementById("verify_information").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('check the agreement!');
                e.preventDefault();
                return
            }
            if (!$('#personal_guarantee_sign_date').val()) {
                document.getElementById("personal_guarantee_sign_date").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner personal guarantee sign date!');
                e.preventDefault();
                return
            }
            if (!$('#print_client_business_legal_name').val()) {
                document.getElementById("print_client_business_legal_name").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner print client business legal name!');
                e.preventDefault();
                return
            }
            if (!$('#print_name_signer').val()) {
                document.getElementById("print_name_signer").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner print name signer!');
                e.preventDefault();
                return
            }
            if (!$('#business_principle_title').val()) {
                document.getElementById("business_principle_title").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter owner business principle title!');
                e.preventDefault();
                return
            }
            if (!$('#business_principle_sign_date').val()) {
                document.getElementById("business_principle_sign_date").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Enter business principle sign date!');
                e.preventDefault();
                return
            }
             if (!$("input:radio[name='standalone_or_semi']").is(":checked")){
                document.getElementById("standalone_or_semi1").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the standalone or semi !');
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='account_type']").is(":checked")){
                document.getElementById("account_type3").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                alert('Choose the account information !');
                e.preventDefault();
                return
            }
//            if (!$("input:radio[name='pricing_type']").is(":checked")){
//                alert('Choose the pricing type !');
//                e.preventDefault();
//                return
//            }

            if ($('input[name="if_want_free_cash_discount"]:checked').val()=='1'){
                if ($('#menu_document').get(0).files.length === 0) {
                    document.getElementById("menu_document").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
                    alert('Upload the menu document !');
                    e.preventDefault();
                    return
                }
            }
//            if ($('#void_check_document').get(0).files.length === 0) {
//                    document.getElementById("void_check_document").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
//                    alert('Upload the void check document !');
//                    e.preventDefault();
//                    return
//            }
//            if ($('#owner_id_document').get(0).files.length === 0) {
//                    document.getElementById("owner_id_document").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
//                    alert('Upload the owner id document !');
//                    e.preventDefault();
//                    return
//            }
//            if ($('#irs_document').get(0).files.length === 0) {
//                    document.getElementById("irs_document").scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
//                    alert('Upload the irs document !');
//                    e.preventDefault();
//                    return
//            }

            const fd = new FormData();
            if (signature_emptyUrl != $('.signature').jqSignature('getDataURL')){
                fd.append('signature', $('.signature').jqSignature('getDataURL'));
            }
            if (personal_guarantee_signature_emptyUrl != $('.personal_guarantee_signature').jqSignature('getDataURL')){
                fd.append('personal_guarantee_signature', $('.personal_guarantee_signature').jqSignature('getDataURL'));
            }
            if (client_initials_signature_emptyUrl != $('.client_initials_signature').jqSignature('getDataURL')){
                fd.append('client_initials_signature', $('.client_initials_signature').jqSignature('getDataURL'));
            }
            if (client_business_principle_signature_emptyUrl != $('.client_business_principle_signature').jqSignature('getDataURL')){
                fd.append('client_business_principle_signature', $('.client_business_principle_signature').jqSignature('getDataURL'));
            }
            if ($('input[name="if_want_free_cash_discount"]:checked').val()=='1'){
                if ($('#menu_document').get(0).files.length != 0) {
                    fd.append('menu_document', $('#menu_document')[0].files[0]);
                }
            }
            if ($('#void_check_document').get(0).files.length != 0) {
                    fd.append('void_check_document', $('#void_check_document')[0].files[0]);
            }
            if ($('#owner_id_document').get(0).files.length != 0) {
                    fd.append('owner_id_document', $('#owner_id_document')[0].files[0]);
            }
            if ($('#other_document').get(0).files.length != 0) {
                    fd.append('other_document', $('#other_document')[0].files[0]);
            }

            fd.append('account_type', $('input[name="account_type"]:checked').val());
            fd.append('old_mid', $('#old_mid').val());
            fd.append('is_add_paper_plan', $('input[name="is_add_paper_plan"]:checked').val());
            fd.append('checkbook', $("#checkbook").is(':checked'));
            fd.append('tips_trays', $("#tips_trays").is(':checked'));
            fd.append('no_supply_order_needed', $("#no_supply_order_needed").is(':checked'));
            fd.append('standalone_or_semi', $('input[name="standalone_or_semi"]:checked').val());
            fd.append('equipment_type', $('#equipment_type').val());
            fd.append('equipment', $('#equipment').val());
            fd.append('bill_to', $('input[name="bill_to"]:checked').val());
            fd.append('equipment_quantity', $('#equipment_quantity').val());
            fd.append('feature_restaurant', $("#feature_restaurant").is(':checked'));
            fd.append('feature_retail', $("#feature_retail").is(':checked'));
            fd.append('feature_with_tips', $("#feature_with_tips").is(':checked'));
            fd.append('feature_dial', $("#feature_dial").is(':checked'));
            fd.append('feature_pin_debit', $("#feature_pin_debit").is(':checked'));
            fd.append('feature_server_id', $("#feature_server_id").is(':checked'));
            fd.append('feature_ip', $("#feature_ip").is(':checked'));
            fd.append('feature_auto_time_batch', $("#feature_auto_time_batch").is(':checked'));
            fd.append('feature_tip_suggestions', $("#feature_tip_suggestions").is(':checked'));
            fd.append('feature_other_feature', $("#feature_other_feature").is(':checked'));
            fd.append('feature_ip_input', $('#feature_ip_input').val());
            fd.append('feature_auto_batch_time_input', $('#feature_auto_batch_time_input').val());
            fd.append('feature_tip_suggestions_input', $('#feature_tip_suggestions_input').val());
            fd.append('feature_other_feature_input', $('#feature_other_feature_input').val());

            fd.append('deployment_method', $('input[name="deployment_method"]:checked').val());
            fd.append('is_ship_with_pos', $('input[name="is_ship_with_pos"]:checked').val());
            fd.append('ship_out_address', $('#ship_out_address').val());
            fd.append('ship_out_city', $('#ship_out_city').val());
            fd.append('ship_out_zip', $('#ship_out_zip').val());
            fd.append('ship_out_state', $('#ship_out_state').val());

            fd.append('reprogram_old_mid', $('#reprogram_old_mid').val());
            fd.append('pricing_type', $('input[name="pricing_type"]:checked').val());
            fd.append('visa_sales_discount_fee', $('#visa_sales_discount_fee').val());
            fd.append('visa_auth_fee', $('#visa_auth_fee').val());
            fd.append('amex_sales_discount_fee', $('#amex_sales_discount_fee').val());
            fd.append('amex_auth_fee', $('#amex_auth_fee').val());
            fd.append('cash_discount_rate', $('#cash_discount_rate').val());
            fd.append('if_want_free_cash_discount', $('input[name="if_want_free_cash_discount"]:checked').val());
            fd.append('monthly_fee', $('#monthly_fee').val());
            fd.append('other_comment', $('#other_comment').val());
            fd.append('Date', $('#Date').val());

            fd.append('agent_name', $('#agent_name').val());
            fd.append('agent_email', $('#agent_email').val());
            fd.append('name_of_company', $('#name_of_company').val());
            fd.append('dba', $('#dba').val());
            fd.append('address', $('#address').val());
            fd.append('city', $('#city').val());
            fd.append('state', $('#state').val());
            fd.append('zip_code', $('#zip_code').val());
            fd.append('business_phone_number', $('#business_phone_number').val());
            fd.append('fax_number', $('#fax_number').val());
            fd.append('federal_tax_id', $('#federal_tax_id').val());
            fd.append('type_of_business', $('#type_of_business').val());
            fd.append('company_type', $('input[name="company_type"]:checked').val());
            fd.append('open_date', $('#open_date').val());
            fd.append('estimated_monthly_sale_volume', $('#estimated_monthly_sale_volume').val());
            fd.append('average_sales_account', $('#average_sales_account').val());
            fd.append('amex', $('input[name="amex"]:checked').val());

            fd.append('owner_name', $('#owner_name').val());
            fd.append('owner_email', $('#owner_email').val());
            fd.append('owner_title', $('#owner_title').val());
            fd.append('owner_phone_number', $('#owner_phone_number').val());
            fd.append('owner_home_address', $('#owner_home_address').val());
            fd.append('owner_home_city', $('#owner_home_city').val());
            fd.append('owner_home_state', $('#owner_home_state').val());
            fd.append('owner_home_zip_code', $('#owner_home_zip_code').val());
            fd.append('ssn', $('#ssn').val());
            fd.append('owner_date_of_birth', $('#owner_date_of_birth').val());
            fd.append('owner_driver_license_number', $('#owner_driver_license_number').val());
            fd.append('owner_state_issued', $('#owner_state_issued').val());
            fd.append('owner_bank_name', $('#owner_bank_name').val());
            fd.append('owner_bank_routing', $('#owner_bank_routing').val());
            fd.append('owner_bank_account', $('#owner_bank_account').val());

            fd.append('sign_date', $('#sign_date').val());
            fd.append('personal_guarantee_sign_date', $('#personal_guarantee_sign_date').val());
            fd.append('print_client_business_legal_name', $('#print_client_business_legal_name').val());
            fd.append('print_name_signer', $('#print_name_signer').val());
            fd.append('business_principle_title', $('#business_principle_title').val());
            fd.append('business_principle_sign_date', $('#business_principle_sign_date').val());

            fd.append('sharing_link', '1');
             $.ajax({url: "/application_new_merchant/submit",
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
//            console.log("\n\n\n------", data_dict)
            e.preventDefault();

        });
    });
});
