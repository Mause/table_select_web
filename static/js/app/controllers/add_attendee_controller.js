TableSelectWeb.AddAttendeeController = Ember.ObjectController.extend({
    needs: ['ball_table', 'add_attendee'],
    // submit: function(event) { console.log(event); },
    // all: function(event) { console.log(event); },
    events: {
        addAttendee_event: function(event) {
            // get the attendee name
            console.log("HELLO");
        }
    }
});
