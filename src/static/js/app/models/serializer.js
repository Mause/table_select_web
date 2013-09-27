var ApplicationSerializer = DS.RESTSerializer.extend({
    // taken from the TRANSITION.md file for Ember.js
    normalize: function(type, hash, property) {
        'use strict';
        var normalized = {}, normalizedProp;
        console.assert(this.primaryKey);

        for (var prop in hash) {
            if (prop === this.primaryKey) {
                // primary key for model
                normalizedProp = prop;

            } else if (prop.substr(-3) === '_id') {
                // belongsTo relationships
                normalizedProp = prop.slice(0, -3);
            } else if (prop.substr(-4) === '_ids') {
                // hasMany relationship
                normalizedProp = Ember.String.pluralize(prop.slice(0, -4));
            } else {
                // regualarAttribute
                normalizedProp = prop;
            }

            normalized[normalizedProp] = hash[prop];
        }

        return this._super(type, normalized, property);
    },

    serializeBelongsTo: function(record, json, relationship) {
        'use strict';
        var key = relationship.key,
            get = Ember.get,
            isNone = Ember.isNone;

        var belongsTo = get(record, key);

        if (Ember.isNone(belongsTo)) { return; }

        var keyMap = get(this.relationshipKeyMap, key);
        key = keyMap || key;

        json[key] = get(belongsTo, 'id');

        if (relationship.options.polymorphic) {
            json[key + "_type"] = belongsTo.constructor.typeKey;
        }
    },

    serializeHasMany: function(){
        'use strict';
        debugger;
        return this._super.apply(this, arguments);
    }
});


TableSelectWeb.RemovalRequestSerializer = ApplicationSerializer.extend({
    primaryKey: 'request_id',
    alias: 'removal_request',

    relationshipKeyMap: {
        'ball_table': 'ball_table_id',
        'attendee': 'attendee_id'
    }
});

TableSelectWeb.BallTableSerializer = ApplicationSerializer.extend({
    primaryKey: 'ball_table_id',
    attendees: { embedded: 'load' },

    relationshipKeyMap: {
        'attendees': 'attendee_ids'
    }
});

TableSelectWeb.AttendeeSerializer = ApplicationSerializer.extend({
    primaryKey: 'attendee_id',
    relationshipKeyMap: {
        'ball_table': 'ball_table_id'
    }
});
