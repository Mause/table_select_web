define(['ember'], function(Ember){
    'use strict';
    var Router = Ember.Router;

    Router.reopen({
        location: 'history'
    });

    Router.map(function(){
        this.resource('index', {path: '/'});
        this.resource('info', {path: '/info'});
        this.resource('admin', {path: '/admin'});
    });

    return Router;
});
