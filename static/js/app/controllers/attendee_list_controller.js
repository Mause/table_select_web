TableSelectWeb.AttendeeListController = Ember.Controller.extend({
    render: function(){
        console.log('Attendee list Model:', this.get('model'));
        return this._super(arguments);
    },

    RequestRemoveAttendee: function(attendee) {
        'use strict';
        // debugger;

        var ball_table = attendee.get('ball_table');

        console.assert(TableSelectWeb.BallTable.detectInstance(ball_table));

        var record_data = {
            attendee: attendee,
            ball_table: ball_table,
            remover_ident: 'unknown',
            state: 'unresolved'
        };

        var removal_request = TableSelectWeb.RemovalRequest.createRecord(
            record_data);
        var prom = removal_request.save();

        prom.then(function(event){
            console.assert(attendee.id);
            debugger;
            console.log('p1 done');
            attendee.set('removal_request_exists', true);
            var prom = attendee.save();
            prom.then(function(event){
                console.log('p2 done');
            });
        });
    }
});
