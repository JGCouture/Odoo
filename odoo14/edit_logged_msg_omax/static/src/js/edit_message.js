odoo.define("edit_logged_msg_omax/static/src/js/edit_messages.js", function (require) {
    "use strict";
    var rpc = require("web.rpc");
    const { QWeb } = owl;
    const patchMixin = require("web.patchMixin");
    const components = {
      Message: require("mail/static/src/components/message/message.js"),
    };
    const PatchableMessage = patchMixin(components.Message);
    const MessageList = require("mail/static/src/components/message_list/message_list.js");

    PatchableMessage.patch(
      "edit_logged_msg_omax/static/src/js/edit_messages.js",
      (T) => {
        class MessagePatched extends T {
            async willStart() {
                 if (!this.message.author) {
                    this.useracc = {};
                }
                if (this.message.author && this.message.author.user) {
                    var user_id = this.message.author.user.id;
                    var messageId = this.message.localId.split('_')[1];
                    if (messageId > 0) {
                        this.useracc = await rpc.query({
                                    model: 'res.users',
                                    method: "action_user_edit_message",
                                    args: [[]],
                                    kwargs: {
                                        user_id: user_id,
                                        message_id : parseInt(messageId),
                                    },
                                    context: {},
                                }).then(result => {
                                    return Promise.resolve(result);
                                });
                    }
                }
            }
            //--------------------------------------------------------------------------
            // Public
            //--------------------------------------------------------------------------
            
            /**
            * @returns {boolean}
            */
            get hasAuthorGroup() {
                var self = this;
                if(this.useracc && this.useracc['edit']) {
                    return true;
                } else {
                    return false;
                }
            }
            
            /**
            * @returns {boolean}
            */
            get hasModified() {
                var self = this;
                if (this.useracc && this.useracc['history'] > 0) {
                    return true;
                } else {
                    return false;
                }
            }
            
            _onClickEdit(ev) {
                ev.stopPropagation();
                var messageId = ($(ev.currentTarget).data('message-chatter-id').split('_')[1]);
                var user_id = this.message.author.user.id;
                var self = this;
                rpc.query({
                    model: 'res.users',
                    method: "action_user_edit_message_view",
                    args: [[]],
                    kwargs: {
                        user_id : user_id,
                    },
                    context: {},
                }).then(function (res) {
                    if (res['custom_view_id']) {
                        var res_model = 'mail.message';
                        var view_id = parseInt(res['custom_view_id']);
                        if (res_model && messageId) {
                            self.env.bus.trigger('do-action', {
                                action: {
                                    type: 'ir.actions.act_window',
                                    res_model: res_model,
                                    res_id: parseInt(messageId),
                                    views: [[view_id || false, 'form']],
                                    context: {'chatter_message_id': true},
                                    target: 'new'
                                },
                                options: { on_close: () => self.fetchAndUpdate() },
                            });
                        }
                    }
                });
            }
            async fetchAndUpdate() {
                window.location.reload();
            }
            
            /**
            * @returns {boolean}
            */
            get hasDeletor() {
                var self = this;
                if (this.useracc && this.useracc['deletor']) {
                    return true;
                } else {
                    return false;
                }
            }
            
            _onClickDelete(ev) {
                ev.stopPropagation();
                var messageId = ($(ev.currentTarget).data('message-chatter-id').split('_')[1]);
                var self = this;
                if (!confirm("Do you want to delete this message!")){
                  return false;
                } else {
                    rpc.query({
                        model: 'res.users',
                        method: "action_user_delete_message",
                        args: [[]],
                        kwargs: {
                            message_id : parseInt(messageId),
                        },
                        context: {},
                    }).then(function () {
                        self.fetchAndUpdate();
                    });
                }
            }
        }
        return MessagePatched;
      }
    );
    MessageList.components.Message = PatchableMessage;
});
