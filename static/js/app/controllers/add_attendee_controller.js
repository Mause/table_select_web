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
        console.assert(TableSelectWeb.BallTable.detectInstance(ball_table));

        attendee_name = self.get('attendee_name');
        this.set('attendee_name', '');

        if (!attendee_name.trim()) { return; }

        record_data = {
            'attendee_name': attendee_name,
            'show': true,
            'ball_table': ball_table
        };

        attendee = TableSelectWeb.Attendee.createRecord(record_data);

        console.log('Saving');

        prom = attendee.save();

        prom.then(function(){
            console.log('then success;', arguments);
        }, function(){
            console.log('then failure:', arguments);
        });

        prom.on('promise:resolved', function(event){
            console.log('success:', event);
            TableSelectWeb.sendNotification('Attendee add was successful');
        });

        prom.on('promise:failed', function(event){
            self.handle_errors(
                event.detail.errors,
                self.error_handlers,
                record_data);
        });
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
            console.warn('"ball_table_id": %@, with table name "%@"'.fmt(
                error,
                ball_table.get('ball_table_name')));
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
