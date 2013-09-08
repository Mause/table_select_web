TableSelectWeb.AttendeeListComponent = Ember.Component.extend({
    actions: {
        requestRemoveAttendee: function(attendee) {
            'use strict';
            var ball_table = attendee.get('ball_table'),
                store = this.get('parentView.targetObject.store'),
                record_data,
                record;

            // ensure we are getting valid objects from Ember
            Ember.assert('Not a ball_table object',
                store.modelFor('ball_table').detectInstance(ball_table));
            Ember.assert('Not an attendee object',
                store.modelFor('attendee').detectInstance(attendee));


            record_data = {
                attendee_id: attendee,
                ball_table: ball_table,
                remover_ident: 'unknown',
                state: 'unresolved'
            };

            console.log(record_data);

            // create the record...
            record = store.createRecord('removal_request', record_data);

            // save it...
            record.save().then(function(event){
                // and when it is saved, mark the attendee
                attendee.set('removal_request_exists', true);
                attendee.save();
                sendNotification('Removal request successfully submitted');
            });
        }
    }
});
