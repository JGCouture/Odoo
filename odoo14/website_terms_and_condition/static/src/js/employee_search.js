odoo.define('wt_zbspos.employeesearch', function (require) {
"use strict";

	var core = require('web.core');
    var wSaleUtils = require('website_sale.utils');
    const wUtils = require('website.utils');
    var publicWidget = require('web.public.widget');
    var _t = core._t;

    publicWidget.registry.wt_website_tricsa_contact = publicWidget.Widget.extend({
    	selector: '.checkout_autoformat',
    	events: {
        	'keypress .x_studio_agent_cl': '_onKeypressAgent',
        	'click input.previous': '_onClickPrevious',
	    },

	    start: function () {
            this.$agent = this.$('select[name="x_studio_agent"]');
            this.$agentOptions = this.$agent.filter(':enabled').find('option:not(:first)');
            this._onKeypressAgent();
        },


       	_onKeypressAgent: function (ev) {
       		this.$agentOptions.detach();
       		var $displayedagents = this.$stateOptions.filter('[data-start=' + countryID + ']');
            var nb = $displayedagents.appendTo(this.$agent).show().length;
        },
    });
});
