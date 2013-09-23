TableSelectWeb.AdminView = Ember.View.extend({
    templateName: 'admin',

    didInsertElement: function() {
        this.get('controller').on('clear_checkboxes',
            $.proxy(this.clear_checkboxes, this));
    },

    actions: {
        deny: function(){
            // deny the removal request
            var controller = this.get('controller'),
                records = this.get_values();

            controller.send('action', records, 'resolved', 'show');
        },
        allow: function(){
            // allow the removal request
            var controller = this.get('controller'),
                records = this.get_values();

            controller.send('action', records, 'resolved', 'hide');
        }
    },

    get_values: function(){
        return this.get_checked().getEach('value');
    },

    get_checked: function() {
        return this.get_checkboxes().filterBy('checked');
    },

    get_checkboxes: function(){
        return this.get('childViews');
    }
});
