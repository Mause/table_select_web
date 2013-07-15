TableSelectWeb.BallTableController = Ember.Controller.extend({
    model_with_attendees: function(){
        var model = this.get('model');

        var ball_table_id = model.get('id');
        var attendees = TableSelectWeb.Attendee.find({ball_table_id: ball_table_id});

        model = model.get('_data.attributes');
        model['attendees'] = attendees;

        // console.log(attendees);

        return model;
    }.property(['model'])
});
