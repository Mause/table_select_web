TableSelectWeb.BallTableRoute = Ember.Route.extend({
    model: function (params) {
        'use strict';
        return this.store.find('ballTable', params.ball_table_id);
    }
});
