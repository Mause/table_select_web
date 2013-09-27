TableSelectWeb.BallTableRoute = Ember.Route.extend(TableSelectWeb.ApplicationRouteMixin, {
    model: function (params) {
        'use strict';
        return this.store.find('ball_table', params.ball_table_id);
    }
});
