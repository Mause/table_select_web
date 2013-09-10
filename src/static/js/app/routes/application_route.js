TableSelectWeb.ApplicationRoute = Ember.Route.extend({
    actions: {
        login: function(data) {
            var adapter = this.store.adapterFor({typeKey: 'me'}),
                url = adapter.buildURL('me'),
                deferred = Ember.RSVP.defer(),
                self = this;

            adapter.ajax(url, 'POST', {data: data}).then(function(){
                debugger;
                self.set('is_authorized', true);
                console.log(arguments);
            }, function(){
                debugger;
                self.set('is_authorized', false);
                console.log(arguments);
            });
        },

        logout: function(){

        }
    },

    is_authorized: false

    // is_authorized: function(){
    //     var adapter = this.store.adapterFor({typeKey: 'me'}),
    //         url = adapter.buildURL('me'),
    //         deferred = Ember.RSVP.defer();

    //     adapter.ajax(url).then(function(data){
    //         deferred.resolve(data);
    //     }, function(){
    //         deferred.reject({state: 'logged_out'});
    //     });

    //     return deferred.promise;
    // }.property()
});
