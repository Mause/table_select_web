function traverse_mixin(mixin){
    for (var i=0; i<mixin.mixins.length; i++){
        traverse_mixin(mixin.mixins[i]);
    }

    if (mixin.hasOwnProperty('ownerConstructor')) {
        console.log(mixin.ownerConstructor.toString());

    } else {
        return 'END';
    }
}

function get_keys(obj) {
    'use strict';
    // Helpers that operate with 'this' within an #each
    var keys = [];

    function filter_for_own(obj) {
        var own = [];
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) { own.push(key); }
        }
        return own;
    }

    return Ember.keys(Ember.merge(keys, filter_for_own(obj)));
}

TableSelectWeb.sendNotification = function (text, callback) {
    "use strict";
    var options, closed_callback, modalPane;

    closed_callback = typeof callback === 'undefined' ? function () {} : callback;

    options = {
        defaultTemplate: Ember.TEMPLATES.modal,
        heading: text,
        callback: closed_callback
    };

    modalPane = Bootstrap.ModalPane.popup(options);

    return modalPane;
};

Ember.Handlebars.registerHelper('log_content', function(property, options) {
  var context = (options.contexts && options.contexts[0]) || this,
      normalized = Ember.Handlebars.normalizePath(context, property, options.data),
      pathRoot = normalized.root,
      path = normalized.path,
      value = (path === 'this') ? pathRoot : Ember.Handlebars.get(pathRoot, path, options);

    // console.log(value.get('isLoaded'), value.get('content'));
    console.log(value.get('isLoaded'), value.get('content').length);
});

Ember.Handlebars.registerHelper('control_smart', function(path, modelPath, options) {
    // to make sure each table has a unique controller,
    // and hence a controller that has the right info,
    // we give it a new controlID each time.
    // not ideal, but w/e
    options.hash.controlID = 'control-smart-' + String(options.data.keywords.ball_table.id);

    Ember.Handlebars.helpers.control.call(this, path, modelPath, options);
});

TableSelectWeb.ErrorHandlerMixin = Ember.Mixin.create({
    init: function(){
        // console.log('Initialising error handler mixin');
    },

    handle_errors: function(errors, error_handlers, context) {
        'use strict';
        for (var key in errors) {
            if (Ember.keys(error_handlers).contains(key)){
                for (var i=0; i<errors[key].length; i++) {
                    error_handlers[key](errors[key][i], context);
                }
            } else {
                console.warn('An unknown error for "%@" occured: %@'.fmt(
                    key, errors[key]));
            }
        }
    }
});
