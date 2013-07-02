
function db(event, self) {
    console.log('Controller:', self.get('controller').toString());
    console.log('Attendee name as reported;', self.get('attendee_name'));
    self.get('controller').send('addAttendee_event');
}

TableSelectWeb.AddAttendeeView = Ember.View.extend({
    templateName: 'addAttendee',
    attendee_name: '',

    addAttendee: function(event) { db(event, this); },
    click: function(event) { console.log('CLICK'); db(event, this); }
});
