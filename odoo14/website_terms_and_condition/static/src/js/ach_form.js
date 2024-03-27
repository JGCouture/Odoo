

odoo.define('website_term_and_condition.ach_form', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var VariantMixin = require('sale.VariantMixin');

publicWidget.registry.website_term_and_condition = publicWidget.Widget.extend(VariantMixin, {
    selector: '#ach_form',
    events: _.extend({}, VariantMixin.events || {}, {
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
        this.$('.js-signature').jqSignature({width:600,height:100});
        this.emptyUrl = this.$('.js-signature').jqSignature('getDataURL');
//        console.warn(this.emptyUrl);
        return def;
    },

    _clearCanvas: function () {
        this.$('.js-signature').jqSignature('clearCanvas');
    },
    _achSubmit:function(evt){
        console.log(this.$('.js-signature').jqSignature('getDataURL'));
        this.$('#hidden_canvas').val(this.$('.js-signature').jqSignature('getDataURL'))

        if (this.emptyUrl == this.$('.js-signature').jqSignature('getDataURL')){
            alert("Please sign your name!");
            evt.preventDefault();
            return
        }
        var bank_account_type = this.$("input[name='bank_account_type']:checked").val();
        var canvas = this.$('.js-signature').jqSignature('getDataURL');
        var BankName = this.$('#BankName').val();
        var Account = this.$('#Account').val();
        var Routing = this.$('#Routing').val();
        var BankBranch = this.$('#BankBranch').val();
        var nameSubscriptionStartDate = this.$('#SubscriptionStartDate').val();
        console.log(nameSubscriptionStartDate)
        if (!nameSubscriptionStartDate)
        {
            alert("Required start date missing. please ensure to fill it!");
            return false;
        }
        if (!BankName || !Account || !Routing || !bank_account_type || !BankBranch ){
            alert("Required fields missing. please ensure to fill fields which is marked as a '*'");
            return false;
         }
        if( !$('#terms').is(':checked') ){
            alert("Required  missing. please ensure to fill fields which is marked as a '*'");
            return false;
        }
        if ($('#ach_form_void_check').get(0).files.length === 0) {
            alert('Upload the void check!');
            evt.preventDefault();
            return
        }
        const fd = new FormData();
        if ($('#ach_form_void_check').get(0).files.length != 0) {
            fd.append('ach_form_void_check', $('#ach_form_void_check')[0].files[0]);
        }
        fd.append("canvas", canvas);
        fd.append("BankName", BankName);
        fd.append("Account", Account);
        fd.append("Routing", Routing);
        fd.append("bank_account_type", bank_account_type);
        fd.append("SubscriptionStartDate", SubscriptionStartDate);
        fd.append("BankBranch", BankBranch);
        fd.append("partner_id", this.$('#partner_id').val());
        fd.append("sale_order_id", this.$('#sale_order_id').val());
        fd.append("csrf_token", this.$('#csrf_token').val());

        $.ajax({url: "/website/ach_form",
                    type: 'POST',
                    data: fd,
                    processData: false,
                    contentType: false,
                    success: function(result){
                        if (result.code=="201"){
                            alert(result.message);
                            $("#ach").prop("disabled", false);
                            $("#ach").prop("checked", true);
                        }
                        else if (result.code=="202"){
                            alert(result.message);
                            $("#ach").prop("disabled", false);
                            $("#ach").prop("checked", true);
                        }else{
                            alert(result.message);
                        }
              }});
//        this._rpc({
//                    route: '/website/ach_form',
//                    params: {
//                        'canvas': canvas,
//                        'BankName':BankName,
//                        'Account':Account,
//                        'Routing':Routing,
//                        'bank_account_type':bank_account_type,
//                        'SubscriptionStartDate':nameSubscriptionStartDate,
//                        'BankBranch':BankBranch,
//                        'partner_id':this.$('#partner_id').val(),
//                        'sale_order_id':this.$('#sale_order_id').val(),
//                        'csrf_token':this.$('#csrf_token').val(),
//                    },
//                }).then(function(result) {
//                    if(result.code==201){
//                        alert("Thank you , you already submitted");
//                        $("#ach").prop("disabled", false);
//                        $("#ach").prop("checked", true);
//                    }else
//                    {
//                        alert("Sorry , something wrong "+ result.message);
//                        $("#ach").prop("disabled", false);
//                        $("#ach").prop("checked", true);
//                    }
//                });

    }

});

});
