TableSelectWeb.AddAttendeeView = Ember.View.extend({
    templateName: 'addAttendee',
    attendee_name: '',

    addAttendeeFormEvent: function(){
        // tell the controller the attendee_name
        this.set('controller.attendee_name', this.get('attendee_name'));

        // clear the input field
        this.set('attendee_name', '');

        // tell the controller to get its act together
        this.get('controller').send('addAttendeeEvent');
    }
});
