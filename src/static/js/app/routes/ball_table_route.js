TableSelectWeb.BallTableRoute = Ember.Route.extend(TableSelectWeb.ApplicationRouteMixin, {
    model: function (params) {
        return this.store.find('ball_table', params.ball_table_id);
    }
});
