TableSelectWeb.Router.reopen({
    location: 'history',

    init: function(){
        TableSelectWeb.AuthManager = AuthManager.create();
        return this._super.apply(this, arguments);
    },

    isAuthenticated: function() {
        return TableSelectWeb.AuthManager.isAuthenticated();
    }.property('TableSelectWeb.AuthManager.apiKey')
});

TableSelectWeb.Router.map(function(){
    this.resource('index', {path: '/'});
    this.resource('info', {path: '/info'});
    this.resource('admin', {path: '/admin'});
    this.resource('auth', {path: '/auth'});
});

TableSelectWeb.ApplicationRouteMixin = Ember.Mixin.create({
    renderTemplate: function(controller, model){
        this.render({
            outlet: 'application'
        });
    }
});
