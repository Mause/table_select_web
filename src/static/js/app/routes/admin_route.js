TableSelectWeb.AdminRoute = Ember.Route.extend({
    model: function () {
        return this.store.find('removal_request');
    },

    renderTemplate: function(controller, model){
        this.render({
            outlet: 'application'
        });
    }
});
