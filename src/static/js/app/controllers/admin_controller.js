TableSelectWeb.AdminController = Ember.ArrayController.extend(Ember.Evented, {
    success_submit: function(requested){
        debugger;
        var attendees = [],
            proms;

        requested.forEach(function(removal_request){
            var attendee = removal_request.get('attendee');
            attendees.push(
                attendee.set('removal_request_exists', true)
            );
        });

        proms = attendees.invoke('save');
        Ember.RSVP.all(proms).then(
            this.success_note, this.failure
        );
    },

    success_note: function(attendees){
        debugger;
        this.trigger('clear_checkboxes');
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

            var promises;

            records.forEach(function(record){
                record.set('state', state);
                record.set('attendee.show', sh == 'show');
            });

            console.assert(this.success_submit);
            console.assert(this.failure);
            console.assert(this.success_note);

            promises = records.invoke('save');
            Ember.RSVP.all(promises).then(
                this.success_submit, this.failure
            );
        }
    }
});
