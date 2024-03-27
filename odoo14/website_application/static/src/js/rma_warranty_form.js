odoo.define('website_application.rma_warranty_form', function (require) {
'use strict';
	var core = require('web.core');
	var _t = core._t;
	var ajax = require('web.ajax');
	var currentUrl = location.href;

    $(document).ready(function() {

        $('.js-signature-rma').jqSignature({autoFit: true});
        var emptyUrl = $('.js-signature-rma').jqSignature('getDataURL');
        $("#clearCanvasRma").click(function( e ) {
    		$('.js-signature-rma').jqSignature('clearCanvas');
    		e.preventDefault();
		});

        $('#rma_submit').on('click', function(e) {
            $('#hidden_canvas').val($('.js-signature-rma').jqSignature('getDataURL'));
            if (emptyUrl == $('.js-signature-rma').jqSignature('getDataURL')){
                alert("Please sign your name!");
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='service_type']").is(":checked")){
                alert('Check the agree service type !');
                e.preventDefault();
                return
            }
            if (!$('#dba').val()) {
                alert('Enter your Business Name!');
                e.preventDefault();
                return
            }
            if (!$('#contact_name').val()) {
                alert('Enter your Contact Name!');
                e.preventDefault();
                return
            }
            if (!$('#email').val()) {
                alert('Enter your Email!');
                e.preventDefault();
                return
            }
            if (!$('#contact_phone').val()) {
                alert('Enter your contact phone!');
                e.preventDefault();
                return
            }
            if (!$('#restaurant_address').val()) {
                alert('Enter your Restaurant Address!');
                e.preventDefault();
                return
            }
            if (!$('#restaurant_city').val()) {
                alert('Enter your City!');
                e.preventDefault();
                return
            }
            if (!$('#restaurant_zipcode').val()) {
                alert('Enter your zip code!');
                e.preventDefault();
                return
            }
            if (!$("#country_id").val()) {
                alert('Enter your country !');
                e.preventDefault();
                return
              }
              if ( !$("#state_id").val()) {
                alert('Enter your state !');
                e.preventDefault();
                return
              }
            if (!$('#model_number').val()) {
                alert('Enter your Model Number!');
                e.preventDefault();
                return
            }
            if (!$('#serial_number').val()) {
                alert('Enter your Serial Number!');
                e.preventDefault();
                return
            }
            if (!$('#date_of_purchase').val()) {
                alert('Select your Date of Purchase!');
                e.preventDefault();
                return
            }

            if (!$('#detailed_fault_description').val()) {
                alert('Enter your Detailed Fault Description !');
                e.preventDefault();
                return
            }
            if ($('#picture_of_faulty_device').get(0).files.length === 0) {
                alert('Upload the faulty picture!');
                e.preventDefault();
                return
            }
            if (!$("input:radio[name='is_agree']").is(":checked")){
                alert('Check the agree button !');
                e.preventDefault();
                return
            }

            const fd = new FormData();
            fd.append('signature', $('.js-signature-rma').jqSignature('getDataURL'));
            fd.append('picture_of_faulty_device', $('#picture_of_faulty_device')[0].files[0]);

            fd.append('service_type', $('input[name="service_type"]:checked').val());
            fd.append('dba', $('#dba').val());
            fd.append('lead_id', $('#lead_id').val());
            fd.append('email', $('#email').val());
            fd.append('contact_name', $('#contact_name').val());
            fd.append('contact_phone', $('#contact_phone').val());
            fd.append('restaurant_address', $('#restaurant_address').val());
            fd.append('restaurant_city', $('#restaurant_city').val());
            fd.append('restaurant_zipcode', $('#restaurant_zipcode').val());
            fd.append('country_id', $('#country_id').val());
            fd.append('state_id', $('#state_id').val());
            fd.append('model_number', $('#model_number').val());
            fd.append('serial_number', $('#serial_number').val());
            fd.append('date_of_purchase', $('#date_of_purchase').val());
            fd.append('detailed_fault_description', $('#detailed_fault_description').val());
            fd.append('csrf_token', $('#csrf_token').val());
//            console.log("\n\n\n------", fd)


            $.ajax({url: "/application_rma_warranty/submit",
                    type: 'POST',
                    data: fd,
                    processData: false,
                    contentType: false,
                    success: function(result) {

                        $("html").html(result);
                   }

            });
           e.preventDefault();
//            console.log("\n\n\n------", data_dict)
        });
    });
});
