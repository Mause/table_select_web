TableSelectWeb.BallTableController = Ember.Controller.extend({
    // didLoad: function(){
    //     console.log("DUDLOAD");
    // }
    // model_with_attendees: function(){
    //     var model = this.get('model');
    //     var ball_table_id = model.get('id');

    //     var attendees = TableSelectWeb.Attendee.find(
    //         {ball_table_id: ball_table_id});

    //     attendees.on('didLoad', function(){
    //         console.log('attendees:', attendees.get('content'));
    //         // var store = TableSelectWeb.__container__.lookup('store:main');
    //         // console.log('Res:', store.load(attendees));
    //     });

    //     attendees.then(function(records){
    //         console.log('Content length:', records.get('content').length);
    //         // if (records.get('content').length === 0) {
    //         //     records = [];
    //         // } else {
    //         //     records = records.get('content');
    //         // }
    //         // console.log('attendees:', records);
    //     });

    //     return model;
    // }.property(['model'])
});
