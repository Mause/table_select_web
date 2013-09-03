TableSelectWeb.AddAttendeeController = Ember.Controller.extend({
    needs: ['index'],
    actions: {

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

            Ember.assert('Not a ball_table instance',
                this.store.modelFor('ball_table').detectInstance(ball_table));
            Ember.assert('Bad ball_table id', !!ball_table.id);

            attendee_name = self.get('attendee_name');
            this.set('attendee_name', '');

            attendee_name = attendee_name.trim();

            if (!attendee_name) { return; }

            record_data = {
                'attendee_name': attendee_name,
                'show': true,
                'ball_table_id': ball_table
            };

            attendee = this.store.createRecord('attendee', record_data);

            console.log(attendee.ball_table);

            console.log('Saving');
            // debugger;
            prom = attendee.save();


            var success_handler = function(event) {
                console.log('success:', event);
                sendNotification('Attendee add was successful');
            },
            failure_handler = function(event) {
                // debugger;
                var record;

                if (!event.hasOwnProperty('detail')) {
                    record = event;
                } else {
                    record = event.detail;
                }

                console.log('failed, handling errors', record.errors);
                self.handle_errors(
                    record.errors,
                    self.error_handlers,
                    record_data);
            };

            prom.then(success_handler, failure_handler);
        },
    },

    error_handlers: {
        attendee_name: function (error, context) {
            if (error.machine === "attendee_exists") {
                console.error('attendee_exists: %@'.fmt(context.attendee_name));
                return {
                    notification: (error.human.fmt(context.attendee_name))
                };
            } else {
                throw new Error('"attendee_name": %@'.fmt(error));
            }
        },

        ball_table_id: function(error, context) {
            if (error.machine === "table_full") {
                return {
                    notification: error.human
                };
            } else {
                throw new Error('"ball_table_id": %@'.fmt(error));
            }
        },

        show: Ember.K
    }
});

TableSelectWeb.AddAttendeeController.reopen(TableSelectWeb.ErrorHandlerMixin);
