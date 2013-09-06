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
        var records = this.get_values(),
            self = this,
            promises,
            success,
            failure;

        records.forEach(function(record){
            record.set('state', state);
            if (sh == 'show' && record.get('attendee.show') !== true) {
                record.set('attendee.show', true);
            } else if (sh == 'hide' && record.get('attendee.show') !== false) {
                record.set('attendee.show', false);
            }
        });

        promises = records.invoke('save');
        Ember.RSVP.all(promises).then(
            success, failure
        );

        success = function(requested){
            debugger;
            self.clear_checkboxes();
            sendNotification('Success');
        };

        failure = function(){
            debugger;
            sendNotification('Failure');
        };
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
        return this.get('childViews');
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
