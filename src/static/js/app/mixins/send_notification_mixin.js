TableSelectWeb.NotificationMixin = Ember.Mixin.create({
    manualModalButtons: [
        Ember.Object.create({title: 'Submit', clicked: "modal_success_callback"}),
        Ember.Object.create({title: 'Cancel', dismiss: "modal_failure_callback"})
    ],

    send: function(eventName, args){
        var possible_diverts = this.manualModalButtons.mapBy('clicked');
        possible_diverts = possible_diverts.concat(this.manualModalButtons.mapBy('dismiss'));
        if (possible_diverts.contains(eventName)) {
            return this.get('_callbacks')[eventName](args);
        }

        return this._super(eventName, args);
    },

    sendNotification: function(text, callback) {
        'use strict';
        var options,
            modalPane,
            callbacks,
            manualButtons;

        var callback_wrapper = function(){
            var returned = Bootstrap.ModalManager.close('manualModal');

            if (!Em.isNone(callback))
                callback.apply(this, arguments);

            return returned;
        };

        this.set('_callbacks', {
            modal_success_callback: callback_wrapper,
            modal_failure_callback: callback_wrapper,
        });

        // hax :/
        TableSelectWeb.BsModalComponent = Bootstrap.BsModalComponent;

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
