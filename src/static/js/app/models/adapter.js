(function(){
    'use strict';
    var acceptable = [
        422,
        400
    ];

    DS.RESTAdapter.reopen({
        didError: function(store, type, record, xhr) {
            if (acceptable.contains(xhr.status)) {
                console.log('Acceptable!', xhr.status);
                var json = JSON.parse(xhr.responseText),
                    serializer = Ember.get(this, 'serializer'),
                    errors = serializer.extractExtendedValidationErrors(type, json);

                store.recordWasInvalid(record, errors);
            } else {
                console.log('oh?', xhr.status);
                this._super.apply(this, arguments);
            }
        }
    });

    TableSelectWeb.Adapter = DS.RESTAdapter.extend({
        namespace: 'api/v1',

        mappings: {
            ball_tables: TableSelectWeb.BallTable,
            removal_request: TableSelectWeb.RemovalRequest
        }
    });
})();