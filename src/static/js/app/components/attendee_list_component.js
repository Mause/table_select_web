TableSelectWeb.AttendeeListComponent = Ember.Component.extend({
    actions: {
        requestRemoveAttendee: function(attendee) {
            'use strict';
            var ball_table = attendee.get('ball_table_id'),
                store = this.get('parentView.targetObject.store'),
                record;

            // ensure we are getting valid objects from Ember
            Ember.assert('Not a ball_table object',
                store.modelFor('ball_table').detectInstance(ball_table));
            Ember.assert('Not an attendee object',
                store.modelFor('attendee').detectInstance(attendee));

            // create the record...
            record = store.createRecord('removal_request', {
                attendee_id: attendee,
                ball_table_id: ball_table,
                remover_ident: 'unknown',
                state: 'unresolved'
            });

            // save it...
            record.save().then(function(event){
                // and when it is saved, mark the attendee
                attendee.set('removal_request_exists', true);
                attendee.save();
            });
        }
    }
});
