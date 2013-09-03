TableSelectWeb.AddAttendeeView = Ember.View.extend({
    templateName: 'addAttendee',
    attendee_name: '',

    actions: {
        addAttendeeFormEvent: function(attendee_name){
            var controller = this.get('controller');

            // tell the controller the attendee_name
            controller.set('attendee_name', attendee_name);

            // clear the input field
            this.set('attendee_name', '');

            // tell the controller to get its act together
            controller.send('addAttendeeEvent');
        }
    }
});
