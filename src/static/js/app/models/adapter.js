(function(Ember){
    'use strict';
    var acceptable = [
        422,
        400
    ];

    DS.RESTAdapter.reopen({
        ajaxError: function(jqXHR) {
            var error = this._super(jqXHR);

            if (jqXHR && acceptable.contains(jqXHR.status)) {
                console.log('Acceptable!', jqXHR.status);
                var json = JSON.parse(jqXHR.responseText);
                return new DS.InvalidError(json["errors"]);
            } else {
                return error;
            }
        },
        headers: {}
    });

    TableSelectWeb.ApplicationAdapter = DS.RESTAdapter.extend({
        namespace: 'api/v1',

        mappings: {
            ball_tables: TableSelectWeb.BallTable,
            removal_request: TableSelectWeb.RemovalRequest
        }
    });
})(Ember);
