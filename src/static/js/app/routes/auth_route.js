TableSelectWeb.AuthRoute = Ember.Route.extend({
    renderTemplate: function(controller, model){
        this.render({
            outlet: 'application'
        });
    }
});
