TableSelectWeb.AdminRoute = Ember.Route.extend({
    beforeModel: function (){
        'use strict';
        if (!TableSelectWeb.AuthManager.isAuthenticated()){
            this.transitionTo('index');
        }
    },

    model: function () {
        'use strict';
        return this.store.findQuery('removalRequest', {
            'state': 'unresolved'
        });
    }
});
