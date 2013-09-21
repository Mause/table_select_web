TableSelectWeb.AdminRoute = Ember.Route.extend(TableSelectWeb.ApplicationRouteMixin, {
    beforeModel: function (){
        if (!TableSelectWeb.AuthManager.isAuthenticated()){
            this.transitionTo('index');
        }
    },

    model: function () {
        return this.store.findQuery('removal_request', {
            'state': 'unresolved'
        });
    }
});
