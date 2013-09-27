TableSelectWeb.ApplicationRoute = Ember.Route.extend({
    actions: {
        logout: function(){
            'use strict';
            TableSelectWeb.AuthManager.reset();
            this.transitionTo('/');
        }
    }
});
