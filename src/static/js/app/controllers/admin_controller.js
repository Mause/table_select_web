TableSelectWeb.AdminController = Ember.ArrayController.extend(Ember.Evented, {
    actions: {
        action: function(records, state, sh){
            'use strict';
            var view = this.get('view'),
                promises,
                success_note,
                success_submit,
                failure;

            records.forEach(function(record){
                record.set('state', state);
                if (sh == 'show' && record.get('attendee.show') !== true) {
                    record.set('attendee.show', true);
                } else if (sh == 'hide' && record.get('attendee.show') !== false) {
                    record.set('attendee.show', false);
                }
            });

            debugger;
            if (records.length == 1){
                records[0].save().then(
                    success_submit, failure);
            } else {
                promises = records.invoke('save');
                Ember.RSVP.all(promises).then(
                    success_submit, failure
                );
            }

            success_submit = function(requested){
                debugger;
                var attendees = [],
                    proms;
                requested.forEach(function(removal_request){
                    debugger;
                    var attendee = removal_request.get('attendee');
                    attendee.set('removal_request_exists', true);
                });
                proms = attendees.invoke('save');
                Ember.RSVP.all(proms).then(
                    success_note, failure
                );
            };

            success_note = function(attendees){
                debugger;
                this.trigger('clear_checkboxes');
                sendNotification('Success');
            };

            failure = function(){
                debugger;
                sendNotification('Failure');
            };
        }
    }
});
