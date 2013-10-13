TableSelectWeb.AdminController = Ember.ArrayController.extend({
    checked_removal_requests: [],

    success_submit: function(requested){
        'use strict';
        var attendees = [],
            proms;

        requested.forEach(function(removal_request){
            var attendee = removal_request.get('attendee');
            attendees.push(
                attendee.set('removal_request_exists', false)
            );
        });

        Ember.assert('Bad function', this.success_attendee);
        Ember.assert('Bad function', this.failure);

        proms = attendees.invoke('save');
        Ember.RSVP.all(proms).then(
            Ember.$.proxy(this.success_attendee, this, requested),
            Ember.$.proxy(this.failure, this)
        );
    },

    success_attendee: function(requested){
        'use strict';
        TableSelectWeb.Router.router.getHandler('admin').model();

        var route = TableSelectWeb.__container__.lookup('route:admin');
        currentModel = route.get('currentModel');
        currentModel.arrayContentWillChange();
        requested.forEach(function(removal_request){
            currentModel.removeRecord(removal_request);
        });
        currentModel.arrayContentDidChange();

        debugger;
        this.sendNotificationLoc('Success');
    },

    failure: function(source){
        debugger;
        this.sendNotificationLoc('Failure');
    },

    action: function(show_attendee){
        'use strict';
        var promises,
            records=this.checked_removal_requests.copy();
        this.checked_removal_requests.clear();

        records.forEach(function(record){
            record.set('state', 'resolved');
            record.set('attendee.show', show_attendee);
        });

        Ember.assert('Bad function', this.success_attendee);
        Ember.assert('Bad function', this.failure);

        promises = records.invoke('save');
        Ember.RSVP.all(promises).then(
            Ember.$.proxy(self.success_submit, self),
            Ember.$.proxy(self.failure, self)
        );
    },

    actions: {
        deny: function(){
            return this.action('show');
        },
        allow: function(){
            return this.action('hide');
        }
    }
});

TableSelectWeb.AdminController.reopen(
    Ember.Evented,
    TableSelectWeb.NotificationMixin
);
