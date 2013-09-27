TableSelectWeb.AuthRoute = Ember.Route.extend(TableSelectWeb.ApplicationRouteMixin, {
    beforeModel: function(){
        'use strict';
        if (TableSelectWeb.AuthManager.isAuthenticated()) {
            this.transitionTo('/');
        }
    }
});
