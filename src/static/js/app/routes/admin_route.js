TableSelectWeb.AdminRoute = Ember.Route.extend({
    model: function () {
        return this.get('store').findQuery('removal_request', {
            'state': 'unresolved'
        });
    },

    renderTemplate: function(controller, model){
        this.render({
            outlet: 'application'
        });
    }
});
