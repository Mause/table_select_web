Ember.RSVP.configure('onerror', function(e) {
  console.log(e.message);
  console.log(e.stack);
});

Ember.RSVP.configure('async', function(func){
    // debugger;
    var args = Array.prototype.slice.call(arguments, 1);
    return func.apply(this, args);
});


// these tend to spam :/
// Ember.LOG_BINDINGS = true;
// Ember.STRUCTURED_PROFILE = true;

Ember.LOG_VERSION = true;
Ember.ENV.RAISE_ON_DEPRECATION = true;
Ember.LOG_STACKTRACE_ON_DEPRECATION = true;
Ember.DEBUG = true;

var TableSelectWeb = Ember.Application.createWithMixins(Bootstrap.Register, {
    title: 'Ball Table Select',
    author: 'Dominic May (http://mause.me)',
    // LOG_TRANSITIONS: true,
    // LOG_ACTIVE_GENERATION: true,
    // LOG_TRANSITIONS_INTERNAL: true,
    // LOG_VIEW_LOOKUPS: true,
    rootElement: 'body'
});

TableSelectWeb.initializer({
    name: 'injectStoreIntoComponents',
    before: 'registerComponents',
    initialize: function(container, application){
        'use strict';
        container.register('store:main', TableSelectWeb.Store);
        container.injection('component', 'store', 'store:main');
    }
});
