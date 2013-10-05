TableSelectWeb.NotificationMixin = Ember.Mixin.create({
    manualModalButtons: [
        Ember.Object.create({title: 'Submit', clicked: "success_callback"}),
        Ember.Object.create({title: 'Cancel', dismiss: "failure_callback"})
    ],

    sendNotification: function(text, callback) {
        'use strict';
        var options,
            modalPane,
            callbacks,
            manualButtons;

        var callback_wrapper = function(){
            var returned = Bootstrap.ModalManager.close('manualModal');

            callback.apply(this, arguments);

            return returned;
        };

        callbacks = {
            success_callback: callback_wrapper,
            failure_callback: callback_wrapper,
        };

        Bootstrap.ModalManager.open(
            'manualModal',
            text,
            Ember.TEMPLATES.modal,
            this.manualModalButtons,
            this
        );
    },

    sendNotificationLoc: function(text, callback) {
        'use strict';
        text = Ember.String.loc(text);
        return this.sendNotification(text, callback);
    }
});
