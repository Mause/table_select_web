TableSelectWeb.AddAttendeeController = Ember.Controller.extend({
    needs: ['index'],

    addAttendeeEvent: function(){
        'use strict';
        // control content is set by the control helper, second arg to helper
        var ball_table = this.get('content');

        var attendee_name = this.get('attendee_name');
        this.set('attendee_name', '');

        if (!attendee_name.trim()) { return; }

        var attendee = TableSelectWeb.Attendee.createRecord({
            'attendee_name': attendee_name,
            'show': true,
            'ball_table': ball_table
        });

        console.log('Saving');

        debugger;

        var prom = attendee.save();

        prom.then(function(){
            console.log('then success:', arguments);
        }, function(){
            console.log('then failure:', arguments);
        });

        var _this = this;

        prom.on('promise:resolved', function(event){
            // success
            console.log('success:', event);
            _this.get('controllers.index').rerender();
        });

        var error_handlers = {
            attendee_name: function (error){
                if (error === "attendee_exists") {
                    console.error('attendee_exists: %@'.fmt(attendee_name));
                } else {
                    throw new Error('"attendee_name": %@'.fmt(error));
                }
            },
            ball_table_id: function(error) {
                console.log('"ball_table_id": %@, with table name "%@"'.fmt(
                    error,
                    ball_table.get('ball_table_name')));
            },
            show: Ember.K
        };

        prom.on('promise:failed', function(event){
            // failure
            console.log('promise:failed');

            // this errors attribute is set when i reopened
            // the RESTAdapter in store.js
            var errors = event.detail.errors;
            debugger;

            for (var key in errors) {
                if (Ember.keys(error_handlers).contains(key)){
                    errors[key].forEach(error_handlers[key]);
                } else {
                    console.warn('An unknown error for "%@" occured: %@'.fmt(
                        key, errors[key]));
                }
            }
        });
    },

    becameError: function() {
        console.log('standalone becameError:', arguments);
    },

    becameInvalid: function() {
        console.log('becameInvalid:', arguments);
    },

    error: function() {
        console.log('error:', arguments);
    }
});
