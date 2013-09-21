function sendNotification(text, callback) {
    var options,
        closed_callback,
        modalPane,
        default_callback;

    // it will simply do nothing if no callback is provided

    options = {
        defaultTemplate: Ember.TEMPLATES.modal,
        heading: text,
        callback: closed_callback,
        primary: 'Okay'
    };

    modalPane = Bootstrap.ModalPane.popup(options);

    return modalPane;
}
