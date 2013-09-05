TableSelectWeb.AddAttendeeComponent = Ember.Component.extend({
    templateName: 'addAttendee',
    attendee_name: '',

    actions: {
        addAttendeeFormEvent: function(attendee_name){
            var controller = this.get('controller');

            // tell the controller the attendee_name
            controller.set('attendee_name', attendee_name);

            // clear the input field
            this.set('attendee_name', '');

            debugger;
            // tell the controller to get its act together
            controller.send('addAttendeeEvent');
        }
    }
});
