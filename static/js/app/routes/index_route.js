TableSelectWeb.IndexRoute = Ember.Route.extend({
    model: function () {
        return TableSelectWeb.BallTable.find();
    },

    renderTemplate: function(controller, model){
        this.render({
            outlet: 'application'
        });
    }
});
