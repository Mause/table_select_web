Ember.RSVP.configure('onerror', function(event){
    console.error(event);
});

// these tend to spam :/
// Ember.LOG_BINDINGS = true;
// Ember.STRUCTURED_PROFILE = true;

Ember.LOG_VERSION = true;
Ember.ENV.RAISE_ON_DEPRECATION = true;
Ember.LOG_STACKTRACE_ON_DEPRECATION = true;
Ember.DEBUG = true;

var TableSelectWeb = Ember.Application.create({
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
        container.register('store:main', TableSelectWeb.Store);
        container.injection('component', 'store', 'store:main');
    }
});
