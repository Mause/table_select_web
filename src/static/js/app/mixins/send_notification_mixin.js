function sendNotification(text, callback) {
    'use strict';
    debugger;
    var options,
        modalPane,
        callbacks,
        manualButtons;

    callbacks = {
        success_callback: function(){
            var returned = Bootstrap.ModalManager.close('manualModal');

            callback.apply(this, arguments);
            return returned;

        },
        failure_callback: function(){
            var returned = Bootstrap.ModalManager.close('manualModal');

            callback.apply(this, arguments);
            return returned;

        },
    };

    manualButtons = [
        Ember.Object.create({title: 'Submit', clicked: "success_callback"}),
        Ember.Object.create({title: 'Cancel', dismiss: "failure_callback"})
    ];

    var x = Bootstrap.ModalManager.open(
        'manualModal',
        text,
        Ember.TEMPLATES.modal,
        manualButtons,
        'lol'
    );

    return modalPane;
}

function sendNotificationLoc(text, callback) {
    'use strict';
    text = Ember.String.loc(text);
    return sendNotification(text, callback);
}
