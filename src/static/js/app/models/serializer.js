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

        var attributes = Ember.get(type, 'attributes').copy();
        // attributes = attributes.keys.list;
        var relationships = Ember.get(type, 'relationshipsByName').copy();
        attributes = merge(attributes.keys.list, relationships.keys.list);

        function get_error(name) {
            var key = _this._keyForAttributeName(type, name);
            if (json.errors.hasOwnProperty(key)) {
                errors[name] = json.errors[key];
            }
        }

        function get_errors(name) {
            get_error.call(_this, name);
            get_error.call(_this, name + '_id');
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

// we create it here so that we can configure
// it for models in their definition files

TableSelectWeb.RemovalRequestSerializer = DS.RESTSerializer.extend({
    primaryKey: 'request_id',
    alias: 'removal_request'
});

TableSelectWeb.BallTableSerializer = DS.RESTSerializer.extend({
    primaryKey: 'ball_table_id',
    attendees: { embedded: 'load' }
    // attendees: {embedded: 'always'},

    // extractSingle: function(store, primaryType, payload, recordId, requestType) {
    //     debugger;
    //     return this._super.apply(this, arguments);
    // }
});

TableSelectWeb.AttendeeSerializer = DS.RESTSerializer.extend({
    primaryKey: 'attendee_id'
});
