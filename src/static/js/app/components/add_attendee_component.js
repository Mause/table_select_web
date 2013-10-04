TableSelectWeb.AddAttendeeComponent = Ember.Component.extend(TableSelectWeb.ErrorHandlerMixin, {
    attendee_name: '',

    actions: {
        addAttendeeFormEvent: function(attendee_name){
            'use strict';
            var store = this.get('store'),
                ball_table = this.get('ball_table'),
                record_data,
                record;

            this.set('attendee_name', '');
            if (!(attendee_name = attendee_name.trim())) { return; }

            Ember.assert('Not a ball_table instance',
                store.modelFor('ball_table').detectInstance(ball_table));
            Ember.assert('Bad ball_table id', !!ball_table.id);

            record_data = {
                'attendee_name': attendee_name,
                'ball_table': ball_table
            };

            record = store.createRecord('attendee', record_data);
            record.save().then(
                Ember.$.proxy(this.success, this),
                Ember.$.proxy(this.failure, this, record_data)
            );
        }
    },

    success: function(attendee) {
        'use strict';
        var ball_table = attendee.get('ball_table');
        ball_table.get('attendees').pushObject(attendee);

        sendNotificationLoc('attendee_add_success');
    },

    failure: function(record_data, event) {
        'use strict';
        var errors = event.errors;
        console.log('failed, handling errors', errors);

        this.handle_errors(
            errors,
            record_data);
    },

    error_handlers: {
        attendee_name: function (error, context) {
            'use strict';

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
            'use strict';

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
