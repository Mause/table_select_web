TableSelectWeb.AdminRoute = Ember.Route.extend(TableSelectWeb.ApplicationRouteMixin, {
    beforeModel: function (){
        'use strict';
        if (!TableSelectWeb.AuthManager.isAuthenticated()){
            this.transitionTo('index');
        }
    },

    model: function () {
        'use strict';
        return this.store.findQuery('removal_request', {
            'state': 'unresolved'
        });
    }
});
