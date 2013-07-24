TableSelectWeb.IndexRoute = Ember.Route.extend({
    model: function () {
        var records = TableSelectWeb.BallTable.find({});

        // records.then(function(records){
        //     console.log('then:', records.get('content'));
        // });

        return records;
    },

    renderTemplate: function(controller, model){
        this.render({
            outlet: 'application'
        });
    }
});
