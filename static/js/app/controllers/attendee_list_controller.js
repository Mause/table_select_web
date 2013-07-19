TableSelectWeb.AttendeeListController = Ember.Controller.extend({
    render: function(){
        console.log('Attendee list Model:', this.get('model'));
        return this._super(arguments);
    },

    RequestRemoveAttendee: function() {
        'use strict';
        console.log(this.get('target').toString());
        console.log('Attendee name;', this.get('attendee_name'));
        console.log('Table num;', this.get('table_num'));
    }
});
