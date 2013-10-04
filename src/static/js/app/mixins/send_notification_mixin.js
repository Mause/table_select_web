function sendNotification(text, callback) {
    'use strict';
    var options,
        modalPane;

    options = {
        defaultTemplate: Ember.TEMPLATES.modal,
        heading: text,
        callback: callback,
        primary: 'Okay'
    };

    modalPane = Bootstrap.ModalPane.popup(options);

    return modalPane;
}

function sendNotificationLoc(text, callback) {
    'use strict';
    text = Ember.String.loc(text);
    return sendNotification(text, callback);
}
