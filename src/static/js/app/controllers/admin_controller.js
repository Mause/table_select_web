TableSelectWeb.AdminController = Ember.ArrayController.extend(Ember.Evented, {
    checked_removal_requests: [],

    success_submit: function(requested){
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
            Ember.$.proxy(this.success_attendee, this, requested),
            Ember.$.proxy(this.failure, this)
        );
    },

    success_attendee: function(requested){

        debugger;
        this.arrayContentWillChange();
        TableSelectWeb.Router.router.getHandler('admin').model();
        this.arrayContentDidChange();

        // var route = TableSelectWeb.__container__.lookup('route:admin');
        // currentModel = route.get('currentModel');
        // debugger;
        // if (currentModel.get('length') === 1) {
        //     currentModel.set('content', []);
        // } else {
        //     requested.forEach(function(removal_request){
        //         currentModel.removeRecord(removal_request);
        //     });
        // }

        sendNotification('Success');
    },

    failure: function(){
        sendNotification('Failure');
    },

    actions: {
        action: function(state, sh){
            'use strict';
            var promises,
                records=this.checked_removal_requests.copy();
            this.checked_removal_requests.clear();

            records.forEach(function(record){
                record.set('state', state);
                record.set('attendee.show', sh == 'show');
            });

            promises = records.invoke('save');
            Ember.RSVP.all(promises).then(
                Ember.$.proxy(self.success_submit, self),
                Ember.$.proxy(self.failure, self)
            );
        }
    }
});
