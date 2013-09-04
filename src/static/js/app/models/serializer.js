// taken from the TRANSITION.md file for Ember.js
var ApplicationSerializer = DS.RESTSerializer.extend({
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

TableSelectWeb.RemovalRequestSerializer = ApplicationSerializer.extend({
    primaryKey: 'request_id',
    alias: 'removal_request'
});

TableSelectWeb.BallTableSerializer = ApplicationSerializer.extend({
    primaryKey: 'ball_table_id',
    attendees: { embedded: 'load' }
});

TableSelectWeb.AttendeeSerializer = ApplicationSerializer.extend({
    primaryKey: 'attendee_id'
});
