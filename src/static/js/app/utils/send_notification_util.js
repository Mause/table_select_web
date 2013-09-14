function sendNotification(text, callback) {
    var options,
        closed_callback,
        modalPane,
        default_callback;

    default_callback = function(){
        // default callback does nothing; derp :P
    };

    closed_callback = (
        typeof callback === 'undefined' ?
        default_callback : callback
    );

    options = {
        defaultTemplate: Ember.TEMPLATES.modal,
        heading: text,
        callback: closed_callback
    };

    modalPane = Bootstrap.ModalPane.popup(options);

    return modalPane;
}
