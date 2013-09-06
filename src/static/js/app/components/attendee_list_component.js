TableSelectWeb.AttendeeListComponent = Ember.Component.extend({
    render: function(){
        console.log('Attendee list Model:', this.get('model'));
        return this._super.apply(this, arguments);
    },

    RequestRemoveAttendee: function(attendee) {
        'use strict';

        var ball_table = attendee.get('ball_table');

        console.assert(
            this.get('store').modelFor('ball_table').detectInstance(ball_table));

        var prom = this.get('store').push('removal_request', {
            attendee: attendee,
            ball_table: ball_table,
            remover_ident: 'unknown',
            state: 'unresolved'
        });

        prom.then(function(event){
            console.assert(attendee.id);
            debugger;
            console.log('p1 done');
            attendee.set('removal_request_exists', true);

            attendee.save().then(function(event){
                console.log('p2 done');
            });
        });
    }
});
