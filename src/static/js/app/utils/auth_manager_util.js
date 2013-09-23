var AuthManager = Ember.Object.extend({
    // Load the current user if the cookies exist and is valid
    init: function() {
        this._super();
        var accessToken = Ember.$.cookie('access_token');
        var authUserId  = Ember.$.cookie('auth_user');
        if (!Ember.isEmpty(accessToken) && !Ember.isEmpty(authUserId)) {
            this.authenticate(accessToken, authUserId);
        }
    },

    // Determine if the user is currently authenticated.
    isAuthenticated: function() {
        return !Ember.isEmpty(this.get('apiKey.accessToken')) && !Ember.isEmpty(this.get('apiKey.user'));
    },

    // Authenticate the user. Once they are authenticated, set the access token to be submitted with all
    // future AJAX requests to the server.
    authenticate: function(accessToken, userId) {
        var adapter = TableSelectWeb.__container__.lookup('adapter:application');
        adapter.set('headers.Authorization', 'Bearer ' + accessToken);

        // var user = User.find(userId);
        this.set('apiKey', TableSelectWeb.ApiKey.create({
            accessToken: accessToken,
            user: {Id: userId}
        }));
    },

    // Log out the user
    reset: function() {
        // TableSelectWeb.__container__.lookup("route:application").transitionTo('sessions.new');
        Ember.run.sync();
        Ember.run.next(this, function(){
            this.set('apiKey', null);

            var adapter = TableSelectWeb.__container__.lookup('adapter:application');
            adapter.set('headers.Authorization', 'Bearer none');
        });
    },

    // Ensure that when the apiKey changes, we store the data in cookies in order for us to load
    // the user when the browser is refreshed.
    apiKeyObserver: function() {
        if (Ember.isEmpty(this.get('apiKey'))) {
            Ember.$.removeCookie('access_token');
            Ember.$.removeCookie('auth_user');
        } else {
            Ember.$.cookie('access_token', this.get('apiKey.accessToken'));
            Ember.$.cookie('auth_user', this.get('apiKey.user.Id'));
        }
    }.observes('apiKey')
});

// Reset the authentication if any ember data request returns a 401 unauthorized error
DS.rejectionHandler = function(reason) {
    if (reason.status === 401) {
        TableSelectWeb.AuthManager.reset();
    }
    throw reason;
};

TableSelectWeb.ApiKey = Ember.Object.extend({
  access_token: '',
  user: null
});
