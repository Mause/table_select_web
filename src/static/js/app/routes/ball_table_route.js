TableSelectWeb.BallTableRoute = Ember.Route.extend({
    model: function (params) {
        'use strict';
        return this.store.find('ball_table', params.ball_table_id);
    }
});
