TableSelectWeb.AdminController = Ember.ArrayController.extend(Ember.Evented, {
    success_submit: function(requested){
        var attendees = [],
            proms,
            self=this;

        requested.forEach(function(removal_request){
            var attendee = removal_request.get('attendee');
            attendees.push(
                attendee.set('removal_request_exists', false)
            );
        });

        proms = attendees.invoke('save');
        Ember.RSVP.all(proms).then(
            function(){
                return self.success_attendee.call(self, attendees);
            }, this.failure
        );
    },

    success_attendee: function(attendees){
        var ball_tables = [];
        attendees.forEach(function(attendee){
            ball_tables.push(attendee.get('ball_table'));
        });

        Ember.RSVP.all(ball_tables.invoke('save')).then(
            this.success_notif, this.failure
        );
    },

    success_notif: function(ball_tables){
        sendNotification('Success');
    },

    failure: function(){
        sendNotification('Failure');
    },

    actions: {
        action: function(records, state, sh){
            'use strict';

            var promises,
                self=this;

            records.forEach(function(record){
                record.set('state', state);
                record.set('attendee.show', sh == 'show');
            });

            promises = records.invoke('save');
            Ember.RSVP.all(promises).then(
                function(){
                    return self.success_submit.apply(self, arguments);
                }, self.failure
            );
        }
    }
});
