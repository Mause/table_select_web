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

function check(){
    'use strict';
    var keys = function(i){
        Ember.keys(i).forEach(function(elem){
            if (typeof(elem) == "string"){
                console.log('*', elem);
            }
        });
    };

    console.log('Routes;');
    keys(TableSelectWeb.Router.router.recognizer.names);
    console.log('Templates;');
    keys(Ember.TEMPLATES);
}

function check_records(){
    'use strict';

    function get_records(sub_map){
        var records = {};
        for (var key in sub_map.idToReference) {
            records[key] = sub_map.idToReference[key].record;
        }
        return records;
    }

    var store = TableSelectWeb.__container__.lookup('store:main');
    var types = [];
    for (var key in store.typeMaps) {
        types.push(get_records(
            store.typeMaps[key]));
    }
    return types;
}


function run() {
    var attendee = check_records()[1][42];
    debugger;
    attendee.get('content');
    // var table = check_records()[0][46];
    // var attendees = table.get('attendees');
    // attendees.get('content');
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


TableSelectWeb.ErrorHandlerMixin = Ember.Mixin.create({
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
