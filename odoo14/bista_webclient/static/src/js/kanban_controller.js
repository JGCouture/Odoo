odoo.define('bista_webclient.KanbanController', function (require) {
    "use strict";

    const KanbanController = require('web.KanbanController');
    const pyUtils = require('web.py_utils');
    const Domain = require('web.Domain');
    const view_dialogs = require('web.view_dialogs');
    const {_t} = require('web.core');

    KanbanController.include({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this.onDragPopup = params.onDragPopup;
        },
        /**
         * @override
         */
        _onAddRecordToColumn: function (ev) {
            console.log("##########--->", ev.data.record.recordData.is_need_approval);
            console.log("##########-11-->", ev.data.record.recordData.is_approval_user);
            const recordData = ev.data.record.recordData
            if (!this.onDragPopup || !recordData.is_need_approval || (recordData.is_need_approval && recordData.is_approval_user)) {
                return this._super.apply(this, arguments);
            }
            let record = ev.data.record,
                element = this.model.localData[record.db_id],
                evalContext = this.model._getEvalContext(element),
                onDragPopup = pyUtils.py_eval(this.onDragPopup, evalContext),
                sourceColumnID = record.qweb_context.widget.getParent().db_id,
                destinationColumnID = ev.target.db_id,
                parentID = this.model.localData[destinationColumnID || sourceColumnID].parentID,
                parentElement = this.model.localData[parentID],
                sourceElement = this.model.localData[sourceColumnID],
                destinationElement = this.model.localData[destinationColumnID],
                parentData = parentElement.data,
                sourceColumnIndex = parentData.findIndex(v => v === sourceColumnID),
                destinationColumnIndex = parentData.findIndex(v => v === destinationColumnID),
                columnDBIds = [sourceColumnID, destinationColumnID],
                isDraggedForward = !sourceElement.value || destinationColumnIndex > sourceColumnIndex,
                context = _.extend({}, this.initialState.getContext(), {is_dragged_forward: isDraggedForward});
            let domain = isDraggedForward ? onDragPopup.drag_forward_domain || [] : onDragPopup.drag_backward_domain || [];
            let shouldOpen = new Domain(domain, evalContext).compute(evalContext);
            console.log("!!!!!!!!!!!", isDraggedForward, shouldOpen, domain);
            if (!shouldOpen || !isDraggedForward) {
                return this._super.apply(this, arguments);
            }

            let self = this;
            let _super = this._super;
            let _arguments = arguments;
            return new Promise((resolve, reject) => {
                if (isDraggedForward && onDragPopup.forward_form_view_ref) {
                    _.extend(context, {form_view_ref: onDragPopup.forward_form_view_ref});
                }
                if (!isDraggedForward && onDragPopup.backward_form_view_ref) {
                    _.extend(context, {form_view_ref: onDragPopup.backward_form_view_ref});
                }
                console.log("!!!!!!!!!", this.modelName)
                context['destinationColumnID'] =  destinationColumnID
                let isClickedSave = false,
                    pop = new view_dialogs.FormViewDialog(this, {
                    res_model: this.modelName,
                    context: context,
                    title: _t("Warning"),
                    res_id: record.id,
                    size: onDragPopup.form_dialog_size ? onDragPopup.form_dialog_size : 'medium',
                    buttons: [
                        {
                            text: _t("Yes"), classes: "btn-primary", click: function () {
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
                    if (!isClickedSave) {
                        _.each(columnDBIds, db_id => this.renderer.updateColumn(db_id, self.model.get(db_id)));
                    }
                    resolve();
                });
            });
        },
    });
});
