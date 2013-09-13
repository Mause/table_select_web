TableSelectWeb.AuthRoute = Ember.Route.extend(TableSelectWeb.ApplicationRouteMixin, {
    beforeModel: function(){
        if (TableSelectWeb.AuthManager.isAuthenticated()) {
            this.transitionTo('/');
        }
    }
});
