TableSelectWeb.AddAttendeeView = Ember.View.extend({
    templateName: 'addAttendee',
    attendee_name: '',

    addAttendeeFormEvent: function(){
        // tell the controller the attendee_name
        this.set('controller.attendee_name', this.get('attendee_name'));

        // clear the input field
        this.set('attendee_name', '');

        // // setup a connection to report back
        // this.get('controller').on('displayModal', $.proxy(this.displayModal, this));

        // tell the controller to get its act together
        this.get('controller').send('addAttendeeEvent');
    }
});
