odoo.define('bista_webclient.FieldStatus', function (require) {
"use strict";

var config = require('web.config');

/**
 * In this file, we override some relational fields to improve the UX in mobile.
 */

var core = require('web.core');
var relational_fields = require('web.relational_fields');
var pyUtils = require('web.py_utils');
var FieldStatus = relational_fields.FieldStatus;
var Domain = require('web.Domain');
var view_dialogs = require('web.view_dialogs');
const {_t} = require('web.core');
var qweb = core.qweb;

FieldStatus.include({
    init: function () {
        this._super.apply(this, arguments);
        this.onDragPopup = this.attrs.on_drag_popup;
        },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     */
   _onClickStage: function (e) {
        console.log("!!!!!!!!!!!!!!!!!!!!!!!--->", this.onDragPopup);
        if (!this.onDragPopup) {
            return this._super.apply(this, arguments);
        }
        let evalContext =  this.record.context,
            onDragPopup = pyUtils.py_eval(this.attrs.on_drag_popup, evalContext);
        let domain = onDragPopup.drag_forward_domain || [];
         if (!this.record.data.is_need_approval) {
                return this._super.apply(this, arguments);
            }
         if (this.record.data.is_need_approval && this.record.data.is_approval_user) {
                return this._super.apply(this, arguments);
            }
//        let shouldOpen = new Domain(domain, evalContext).compute(evalContext);
        let self = this;
            let _super = this._super;
            let _arguments = arguments;
            let record = $(e.currentTarget).data("value");
            return new Promise((resolve, reject) => {
                let context = {};
                _.extend(context, {form_view_ref: 'bista_task_sale_auto_invoice.apply_btn_message_project_task_wizard_form'});
                let isClickedSave = false,
                    pop = new view_dialogs.FormViewDialog(this, {
                    res_model: 'project.task',
                    title: _t("Warning"),
                    context:context,
                    res_id: this.res_id,
                    size: 'medium',
                    buttons: [
                        {
                            text: _t("YES"), classes: "btn-primary", click: function () {
                                pop._save().then(() => {
                                    _super.apply(self, _arguments)
                                    isClickedSave = true;
                                    pop.close();
                                });
                            }
                        },
                        {
                            text: _t("No"),
                            classes: "btn-secondary o_form_button_cancel",
                            close: true,
                            click: () => {
                                pop.form_view.model.discardChanges(pop.form_view.handle, {
                                    rollback: pop.shouldSaveLocally,
                                });
                            },
                        }],
                }).open();

                pop.on('closed', this, () => {
                    resolve();
                });
            });

        return this._super.apply(this, arguments);
        },

});
});
