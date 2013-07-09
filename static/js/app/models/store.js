var acceptable = [
    422,
    400
];

DS.RESTSerializer.reopen({
    extractExtendedValidationErrors: function(type, json) {
        var errors = {};
        var _this = this;

        function merge(original, updates) {
            for (var i=0; i<updates.length; i++) {
                if ('function' === typeof updates[i]) { continue; }
                original.push(updates[i]);
            }
            return original;
        }

        var attributes = Ember.copy(Ember.get(type, 'attributes'));
        // attributes = attributes.keys.list;
        var relationships = Ember.copy(Ember.get(type, 'relationshipsByName'));
        attributes = merge(attributes.keys.list, relationships.keys.list);

        function get_error(name) {
            var key = _this._keyForAttributeName(type, name);
            if (json['errors'].hasOwnProperty(key)) {
                errors[name] = json['errors'][key];
            }
        }

        function get_errors(name) {
            get_error.call(_this, name);
            // get_error.call(_this, name + '_id');
        }

        try {
            attributes.forEach(get_errors, _this);
        } catch (e) {
            console.log(e);
            debugger;
        }

        return errors;
    }
});


DS.RESTAdapter.reopen({
    didError: function(store, type, record, xhr) {
        if (acceptable.contains(xhr.status)) {

            // debugger;
            var json = JSON.parse(xhr.responseText),
                serializer = Ember.get(this, 'serializer'),
                // errors = serializer.extractValidationErrors(type, json);
                errors = serializer.extractExtendedValidationErrors(type, json);

            // record.errors = errors;

            // debugger;
            store.recordWasInvalid(record, errors);
        } else {
            console.log('oh?');
            this._super.apply(this, arguments);
        }
    }
});


TableSelectWeb.Adapter = DS.RESTAdapter.create({
    namespace: 'api/v1',

    mappings: {
        ball_tables: TableSelectWeb.BallTable,
        errors: TableSelectWeb.Error
    }
}),

TableSelectWeb.Store = DS.Store.extend({
    adapter: TableSelectWeb.Adapter,
    revision: 12
});
