TableSelectWeb.IndexRoute = Ember.Route.extend({
    model: function () {
        'use strict';
        return this.store.find('ball_table');
    }
});
