DS.RESTAdapter.registerTransform('integer', {
    deserialize: function(serialized){
        return serialized;
    },
    serialize: function(deserialized){
        return deserialized;
    }
});


TableSelectWeb.Store = DS.Store.extend({
    adapter: DS.RESTAdapter.create({
        namespace: 'api/v1',
        // bulkCommit: true,
        mappings: {
            ball_tables: TableSelectWeb.BallTable
        }
    }),
    revision: 12
});


