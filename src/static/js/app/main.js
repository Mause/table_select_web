require.config(
    {
        app_name: 'TableSelectWeb',
        baseUrl: 'static/js',
        shim: {
            'ember': {
                deps: ['handlebars', 'jquery'],
                exports: 'Ember'
            },
            'bootstrap': {
                deps: ['jquery']
            },
            'ember-data': {
                deps: ['ember'],
                exports: 'DS'
            },
            'ember-bootstrap': {
                deps: ['ember', 'bootstrap'],
                exports: 'Bootstrap'
            }
        },
        paths: {
            'TableSelectWeb': 'app/main',
            'models': 'app/models',
            'views': 'app/views',
            'controllers': 'app/controllers',
            'routes': 'app/routes',
            'mixins': 'app/mixins',
            'utils': 'app/utils',

            /* libs */
            'jquery': 'third-party/jquery',
            'handlebars': 'third-party/handlebars',
            'ember': 'third-party/ember',
            'ember-data': 'third-party/ember-data',
            'bootstrap': 'third-party/bootstrap',
            'ember-bootstrap': 'third-party/ember_plugins/ember-bootstrap_load'
    }
});

require(['app/main']);
