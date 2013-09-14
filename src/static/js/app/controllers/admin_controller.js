TableSelectWeb.AdminController = Ember.ArrayController.extend(Ember.Evented, {
    success_submit: function(requested){
        debugger;
        var attendees = [],
            proms;

        requested.forEach(function(removal_request){
            var attendee = removal_request.get('attendee');
            attendees.push(
                attendee.set('removal_request_exists', false)
            );
        });

        proms = attendees.invoke('save');
        Ember.RSVP.all(proms).then(
            this.success_notif, this.failure
        );
    },

    success_notif: function(attendees){
        debugger;
        sendNotification('Success');
    },

    failure: function(){
        debugger;
        sendNotification('Failure');
    },

    actions: {
        action: function(records, state, sh){
            'use strict';
            debugger;

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
