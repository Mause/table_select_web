TableSelectWeb.AttendeeListController = Ember.Controller.extend({
    RequestRemoveAttendee: function() {
        'use strict';
        console.log(this.get('target').toString());
        console.log('Attendee name;', this.get('attendee_name'));
        console.log('Table num;', this.get('table_num'));
    }
});
