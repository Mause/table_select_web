TableSelectWeb.AddAttendeeController = Ember.Controller.extend({
    needs: ['index'],

    addAttendeeEvent: function(){
        'use strict';
        var self = this,
            ball_table,
            attendee_name,
            record_data,
            attendee,
            prom;

        // control content is set by the control helper, second arg to helper
        ball_table = self.get('content');

        Ember.assert('Not a ball_table instance', TableSelectWeb.BallTable.detectInstance(ball_table));
        Ember.assert('Bad ball_table id', !!ball_table.id);

        attendee_name = self.get('attendee_name');
        this.set('attendee_name', '');

        attendee_name = attendee_name.trim();

        if (!attendee_name) { return; }

        record_data = {
            'attendee_name': attendee_name,
            'show': true,
            'ball_table': ball_table
        };
        attendee = TableSelectWeb.Attendee.createRecord(record_data);

        console.log('Saving');
        prom = attendee.save();


        var success_handler = function(event) {
            console.log('success:', event);
            TableSelectWeb.sendNotification('Attendee add was successful');
        },
        failure_handler = function(event) {
            console.log('failed, handling errors', event.detail.errors);
            self.handle_errors(
                event.detail.errors,
                self.error_handlers,
                record_data);
        };

        prom.then(success_handler, failure_handler);
    },

    error_handlers: {
        attendee_name: function (error, context) {
            if (error.machine === "attendee_exists") {
                console.info('attendee_exists: %@'.fmt(context.attendee_name));
                TableSelectWeb.sendNotification(error.human.fmt(context.attendee_name));
            } else {
                throw new Error('"attendee_name": %@'.fmt(error));
            }
        },

        ball_table_id: function(error, context) {
            if (error.machine === "table_full") {
                TableSelectWeb.sendNotification(error.human);
            } else {
                throw new Error('"ball_table_id": %@'.fmt(error));
            }
        },

        show: Ember.K
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

console.assert(!Ember.isNone(TableSelectWeb.ErrorHandlerMixin));
TableSelectWeb.AddAttendeeController.reopen(TableSelectWeb.ErrorHandlerMixin);
