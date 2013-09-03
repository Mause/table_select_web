TableSelectWeb.AdminView = Ember.View.extend({
    templateName: 'admin',

    actions: {
        deny: function(){
            // deny the removal request
            this.action('resolved', 'show');
        },
        allow: function(){
            // allow the removal request
            this.action('resolved', 'hide');
        },
    },

    action: function(state, sh){
        'use strict';
        var records = this.get_values();

        records.forEach(function(record){
            record.set('state', state);
            if (sh == 'show' && record.get('attendee.show') !== true) {
                record.set('attendee.show', true);
            } else if (sh == 'hide' && record.get('attendee.show') !== false) {
                record.set('attendee.show', false);
            }
        });

        var promises = [];

        records.forEach(function(record){
            var prom = record.save();
            promises.push(prom);
        });

        var prom = Ember.RSVP.all(promises);

        var self = this;
        var success = function(requested){
            debugger;
            self.clear_checkboxes();
            sendNotification(
                'Success');
        };
        var failure = function(){
            debugger;
            sendNotification(
                'Failure');
        };

        prom.then(success, failure);
        // prom.then(success);
    },

    get_checked: function() {
        var checkboxes = this.get_checkboxes(),
            checked = [];

        checkboxes.forEach(function(view){
            if (view.get('checked')) {
                checked.push(view);
            }
        });

        return checked;
    },

    clear_checkboxes: function(){
        var checkboxes = this.get_checkboxes();
        checkboxes.forEach(function(view){
            view.set('checked', false);
        });
    },

    get_checkboxes: function(){
        var children = this.get('childViews');
        return children;
    },

    get_values: function(){
        var checkboxes = this.get_checked(),
            removal_requests = [];

        checkboxes.forEach(function(view){
            removal_requests.push(view.value);
        });

        return removal_requests;
    }
});
