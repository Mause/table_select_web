TableSelectWeb.IndexRoute = Ember.Route.extend(TableSelectWeb.ApplicationRouteMixin, {
    model: function () {
        'use strict';
        return this.store.find('ball_table');
    }
});
