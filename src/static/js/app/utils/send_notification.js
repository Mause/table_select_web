function sendNotification(text, callback) {
    var options, closed_callback, modalPane;

    closed_callback = typeof callback === 'undefined' ? Ember.K : callback;

    options = {
        defaultTemplate: Ember.TEMPLATES.modal,
        heading: text,
        callback: closed_callback
    };

    modalPane = Bootstrap.ModalPane.popup(options);

    return modalPane;
}
