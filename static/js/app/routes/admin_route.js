TableSelectWeb.AdminRoute = Ember.Route.extend({
    model: function () {
        return TableSelectWeb.RemovalRequest.find({});
    },

    renderTemplate: function(controller, model){
        this.render({
            outlet: 'application'
        });
    }
});
