TableSelectWeb.Model = DS.Model.extend({

    // Primary key:
    primaryKey: 'id',

    // Toggles:
    hasBeenDeleted: false,
    hasBeenLoaded: false,

    // Events:
    didCreate: function() {
        console.log('didCreate');
        this.didLoad();
    },

    didDelete: function() {
        console.log('didDelete');
        if (!this.get('hasBeenDeleted')) {
            this.trigger('deleteContexts');
            this.toggleProperty('hasBeenDeleted');
        }
    },

    didInit: function() {
        console.log('didInit');
        var self = this;

        this.eachRelationship(function(name, meta) {
            if (meta.kind === 'hasMany') {
                console.log('loaded' + Em.String.classify(name));
                self.set('loaded' + Em.String.classify(name), Em.ArrayController.extend().create());
            }
        });
    },

    didLoad: function() {
        console.log('didLoad');
        if (!this.get('hasBeenLoaded')) {
            // Trigger init and load contexts:
            this.trigger('didInit');
            this.loadContexts();

            // Toggle the hasBeenLoaded property:
            this.toggleProperty('hasBeenLoaded');
        }
    },

    // Relations:
    addRelation: function(record, relation) {
        console.log('addRelation');
        this.handleRelation(record, relation, 'addObject');
    },

    deleteRelation: function(record, relation) {
        console.log('deleteRelation');
        this.handleRelation(record, relation, 'removeObject');
    },

    handleRelation: function(record, relation, type) {
        console.log('handleRelation');
        relation = 'loaded' + Em.String.classify(relation) + '.content';

        if (typeof record !== "undefined" && record !== null) {
            var self = this;

            if (record.get('isLoaded')) {
                record.get(relation)[type](self);
            } else {
                record.one('didLoad', function() { record.get(relation)[type](self); });
            }
        }
    },

    // Functions:
    deleteContexts: function() {
        console.log('deleteContexts');
        var self = this;

        this.eachRelationship(function(name, meta) {
            if (meta.kind === 'belongsTo') {
                self.deleteRelation(self.get(name), Em.String.decamelize(meta.parentType.toString().split('.')[1]));
            }
        });
    },

    loadContexts: function() {
        console.log('loadContexts');
        var self = this;

        this.eachRelationship(function(name, meta) {
            if (meta.kind === 'belongsTo') {
                self.addRelation(self.get(name), Em.String.decamelize(meta.parentType.toString().split('.')[1]));
            }
        });
  }

});
