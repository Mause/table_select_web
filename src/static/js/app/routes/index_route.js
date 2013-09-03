TableSelectWeb.IndexRoute = Ember.Route.extend({
    model: function () {
        return this.store.find('ball_table');
    },

    renderTemplate: function(controller, model){
        this.render({
            outlet: 'application'
        });
    }
});
