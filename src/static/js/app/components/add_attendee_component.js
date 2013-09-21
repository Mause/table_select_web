TableSelectWeb.AddAttendeeComponent = Ember.Component.extend({
    templateName: 'addAttendee',
    attendee_name: '',

    actions: {
        addAttendeeFormEvent: function(attendee_name){
            'use strict';
            var store = this.get('store'),
                ball_table = this.get('ball_table'),
                record_data,
                record,
                self = this;

            this.set('attendee_name', '');
            if (!(attendee_name = attendee_name.trim())) { return; }

            Ember.assert('Not a ball_table instance',
                store.modelFor('ball_table').detectInstance(ball_table));
            Ember.assert('Bad ball_table id', !!ball_table.id);

            record_data = {
                'attendee_name': attendee_name,
                'show': true,
                'ball_table': ball_table
            };

            record = store.createRecord('attendee', record_data);
            record.save().then(
                function(){
                    return self.success.apply(self, arguments);
                },
                function(){
                    return self.failure.apply(self, arguments);
                }
            );
        },
    },

    success: function(attendee) {
        var ball_table = attendee.get('ball_table');
        ball_table.get('attendees').pushObject(attendee);

        sendNotification(Ember.String.loc('attendee_add_success'));
    },

    failure: function(event) {
        var json = event.responseJSON;
        console.log('failed, handling errors', json.errors);

        this.handle_errors(
            json.errors,
            this.error_handlers,
            record_data);
    },

    error_handlers: {
        attendee_name: function (error, context) {
            if (error === "attendee_exists") {
                console.error('attendee_exists: %@'.fmt(context.attendee_name));
                return {
                    notification: Ember.String.loc(error, [context.attendee_name])
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
