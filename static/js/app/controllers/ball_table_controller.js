TableSelectWeb.BallTableController = Ember.Controller.extend({
    model_with_attendees: function(){
        var model = this.get('model'),
            ball_table_id = model.get('id'),
            attendees = TableSelectWeb.Attendee.find({ball_table_id: ball_table_id});

        attendees.then(function(records){
            console.log('Content length:', records.get('content').length);
            // if (records.get('content').length === 0) {
            //     records = [];
            // } else {
            //     records = records.get('content');
            // }
            // console.log('attendees:', records);
        });

        model.set('_data.attributes.attendees', attendees);

        return model;
    }.property(['model'])
});
