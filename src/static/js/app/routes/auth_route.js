TableSelectWeb.AuthRoute = Ember.Route.extend({
    beforeModel: function(){
        'use strict';
        if (TableSelectWeb.AuthManager.isAuthenticated()) {
            this.transitionTo('/');
        }
    }
});
