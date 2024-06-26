odoo.define('thimesheet_grid.timesheet_uom_timer', function (require) {
"use strict";

const fieldRegistry = require('web.field_registry');
const fieldUtils = require('web.field_utils');
const TimesheetUom = require('hr_timesheet.timesheet_uom');
const { _lt } = require('web.core');
const session = require('web.session');

const Timer = require('timer.Timer');

/**
 * Extend float time widget to add the using of a timer for duration
 * (unit_amount) field.
 */
const FieldTimesheetTimeTimer = TimesheetUom.FieldTimesheetTime.extend({
    init: function () {
        this._super.apply(this, arguments);
        this.isTimerRunning = this.record.data.is_timer_running;
        this.rendererIsSample = arguments[0].state.isSample; // This only works with list_views.
    },

    willstart() {
        const timePromise = this._rpc({
            model: 'timer.timer',
            method: 'get_server_time',
            args: []
        }).then((time) => {
            this.serverTime = time;
        });
        return Promise.all([
            this._super(...arguments),
            timePromise,
        ]);
    },

    _render: async function () {
        await this._super.apply(this, arguments);
        const my_timesheets = this.record.getContext().my_timesheet_display_timer;
        const display_timer = this.record.data.display_timer;
        if (my_timesheets && display_timer && this.record.viewType === 'list') {
            const title = this.isTimerRunning ? _lt('Stop') : _lt('Play');
            const name = this.isTimerRunning ? 'action_timer_stop' : 'action_timer_start';
            const label = this.isTimerRunning ? _lt('Stop') : _lt('Start');

            const button = $('<button>', {
                'class': 'o_icon_button o-timer-button mr8',
                'title': title,
                'name': name,
                'aria-label': label,
                'aria-pressed': this.isTimerRunning,
                'type': 'button',
                'role': 'button',
            });
            button.html('<i/>');
            button.find('i')
                .addClass('fa')
                .toggleClass('fa-stop-circle o-timer-stop-button', this.isTimerRunning)
                .toggleClass('fa-play-circle o-timer-play-button', !this.isTimerRunning)
                .attr('title', title);
            button.on('click', this._onToggleButton.bind(this));
            this.$el.prepend(button);
        }
        // Check if the timer_start exists and it's not false
        // In other word, when user clicks on play button, this button
        // launches the "action_timer_start".
        if (this.recordData.timer_start && !this.recordData.timer_pause && !this.rendererIsSample) {
            this.time = Timer.createTimer(this.recordData.unit_amount, this.recordData.timer_start, this.serverTime);
            this._startTimeCounter();
        }
    },

    _onToggleButton: async function (event) {
        const context = this.record.getContext();
        event.stopPropagation();
        const result = await this._rpc({
            model: this.model,
            method: this._getActionButton(),
            context: context,
            args: [this.res_id]
        });

        this.trigger_up('field_changed', {
            dataPointID: this.dataPointID,
            changes: {
                'is_timer_running': !this.isTimerRunning,
            },
        });
        this.trigger_up('timer_changed', {
            id: this.res_id,
            is_timer_running: !this.isTimerRunning
        });
    },

    _getActionButton: function () {
        return this.isTimerRunning ? 'action_timer_stop' : 'action_timer_start';
    },

    /**
     * @override
     */
    destroy: function () {
        clearTimeout(this.timer);
        this._super.apply(this, arguments);
    },
    _startTimeCounter: function () {
        if (this.time) {
            this.timer = setInterval(() => {
                this.time.addSecond();
                if (this.$el.children().length) {
                    this.$el.contents()[1].replaceWith(this.time.toString());
                } else {
                    this.$el.text(this.time.toString());
                }
                this.$el.addClass('font-weight-bold text-danger');
            }, 1000);
        } else {
            clearTimeout(this.timer);
            this.$el.removeClass('font-weight-bold text-danger');
        }
    },

});

/**
 * Binding depending on Company Preference
 *
 * determine wich widget will be the timesheet one.
 * Simply match the 'timesheet_uom' widget key with the correct
 * implementation (float_time, float_toggle, ...). The default
 * value will be 'float_factor'.
**/
const widgetName = 'timesheet_uom' in session ?
         session.timesheet_uom.timesheet_widget : 'float_factor';

let FieldTimesheetUom = null;

if (widgetName === 'float_toggle') {
    FieldTimesheetUom = TimesheetUom.FieldTimesheetToggle;
} else if (widgetName === 'float_time') {
    FieldTimesheetUom = FieldTimesheetTimeTimer;
} else {
    FieldTimesheetUom = (
            fieldRegistry.get(widgetName) &&
            fieldRegistry.get(widgetName).extend({})
        ) || TimesheetUom.FieldTimesheetFactor;
}
fieldRegistry.add('timesheet_uom_timer', FieldTimesheetUom);

// bind the formatter and parser method, and tweak the options
const _tweak_options = function(options) {
    if (!_.contains(options, 'factor')) {
        options.factor = session.timesheet_uom_factor;
    }
    return options;
};

fieldUtils.format.timesheet_uom_timer = function(value, field, options) {
    options = _tweak_options(options || {});
    const formatter = fieldUtils.format[FieldTimesheetUom.prototype.formatType];
    return formatter(value, field, options);
};

fieldUtils.parse.timesheet_uom_timer = function(value, field, options) {
    options = _tweak_options(options || {});
    const parser = fieldUtils.parse[FieldTimesheetUom.prototype.formatType];
    return parser(value, field, options);
};


return {
    FieldTimesheetTimeTimer,
};

});
