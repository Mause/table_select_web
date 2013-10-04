TableSelectWeb.Router.reopen({
    location: 'history',

    init: function(){
        'use strict';
        TableSelectWeb.AuthManager = AuthManager.create();
        return this._super.apply(this, arguments);
    },

    isAuthenticated: function() {
        'use strict';
        return TableSelectWeb.AuthManager.isAuthenticated();
    }.property('TableSelectWeb.AuthManager.apiKey')
});

TableSelectWeb.Router.map(function(){
    this.resource('index', {path: '/'});
    this.resource('info');
    this.resource('admin');
    this.resource('auth');
    this.resource('ball_table', {path: '/table/:ball_table_id'});
});
