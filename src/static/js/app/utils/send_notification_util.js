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
