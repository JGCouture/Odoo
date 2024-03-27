odoo.define('bista_webclient.KanbanView', function (require) {
    "use strict";

    const KanbanView = require('web.KanbanView');

    KanbanView.include({
        /**
         * @override
         */
        init: function (viewInfo, params) {

            this._super.apply(this, arguments);
            let attrs = this.arch.attrs;
            console.log("!!!!!!!!!!!", this);
            this.controllerParams.onDragPopup = 'on_drag_popup' in attrs ? attrs.on_drag_popup : false;
        },
    });
});
