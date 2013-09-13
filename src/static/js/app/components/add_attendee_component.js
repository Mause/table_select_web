TableSelectWeb.AddAttendeeComponent = Ember.Component.extend({
    templateName: 'addAttendee',
    attendee_name: '',

    actions: {
        addAttendeeFormEvent: function(attendee_name){
            'use strict';
            var self = this,
                store = this.get('parentView.targetObject.store'),
                ball_table = self.get('ball_table'),
                record_data,
                success_handler,
                failure_handler;

            this.set('attendee_name', '');

            attendee_name = attendee_name.trim();
            if (!attendee_name) { return; }

            Ember.assert('Not a ball_table instance',
                store.modelFor('ball_table').detectInstance(ball_table));
            Ember.assert('Bad ball_table id', !!ball_table.id);

            record_data = {
                'attendee_name': attendee_name,
                'show': true,
                'ball_table': ball_table
            };

            console.log('Saving');
            store.createRecord('attendee', record_data).save().then(
                success_handler, failure_handler
            );

            success_handler = function(event) {
                debugger;
                console.log('success:', event);
                sendNotification('Attendee add was successful');
            };

            failure_handler = function(event) {
                debugger;
                var record = event.hasOwnProperty('detail') ? event.detail : event;
                console.log('failed, handling errors', record.errors);

                self.handle_errors(
                    record.errors,
                    self.error_handlers,
                    record_data);
            };

        },
    },

    error_handlers: {
        attendee_name: function (error, context) {
            if (error === "attendee_exists") {
                console.error('attendee_exists: %@'.fmt(context.attendee_name));
                return {
                    notification: Ember.String.loc(error, context.attendee_name)
                };
            } else {
                throw new Error('"attendee_name": %@'.fmt(error));
            }
        },

        ball_table_id: function(error, context) {
            if (error === "table_full") {
                return {
                    notification: Ember.String.loc(error)
                };
            } else {
                throw new Error('"ball_table_id": %@'.fmt(error));
            }
        },

        show: Ember.K
    }
});


TableSelectWeb.AddAttendeeComponent.reopen(TableSelectWeb.ErrorHandlerMixin);
