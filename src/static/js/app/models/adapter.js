DS.RESTAdapter.reopen({
    ajaxError: function(jqXHR) {
        var error = this._super(jqXHR);

        if (jqXHR && this.acceptable.contains(jqXHR.status)) {
            var json = JSON.parse(jqXHR.responseText);

            return new DS.InvalidError(json["errors"]);
        } else {
            return error;
        }
    },
    headers: {},
    acceptable: [
        422,
        400
    ]
});

TableSelectWeb.ApplicationAdapter = DS.RESTAdapter.extend({
    namespace: 'api/v1',

    mappings: {
        ball_tables: TableSelectWeb.BallTable,
        removal_request: TableSelectWeb.RemovalRequest
    }
});
