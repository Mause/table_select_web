TableSelectWeb.BallTablesRoute = Ember.Route.extend({
    model: function () {
        return TableSelectWeb.BallTable.find();
    }//,

    // events: {
    //     addAttendee: function(event){
    //         console.log('In route;', event);
    //     }
    // }
});
