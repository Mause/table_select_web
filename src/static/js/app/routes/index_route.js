TableSelectWeb.IndexRoute = Ember.Route.extend(TableSelectWeb.ApplicationRouteMixin, {
    model: function () {
        return this.store.find('ball_table');
    }
});
