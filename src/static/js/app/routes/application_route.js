TableSelectWeb.ApplicationRoute = Ember.Route.extend(TableSelectWeb.NotificationMixin, {
    manualModalButtons: [
        Ember.Object.create({title: 'OK'})
    ],

    actions: {
        logout: function(){
            'use strict';
            // remove the authentication data
            TableSelectWeb.AuthManager.reset();

            // remove all the removal_request's from memory
            this.store.unloadAll('removal_request');

            // and redirect to the homepage
            this.transitionTo('/');
        },
        error: function(error, transition){
            console.log('Error has occured:', error);
            this.sendNotificationLoc('unknown_error');
        }
    }
});
