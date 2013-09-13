TableSelectWeb.ApplicationRoute = Ember.Route.extend({
    actions: {
        logout: function(){
            TableSelectWeb.AuthManager.reset();
            this.transitionTo('/');
        }
    }
});
