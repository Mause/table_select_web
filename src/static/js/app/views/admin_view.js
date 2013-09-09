TableSelectWeb.AdminView = Ember.View.extend({
    templateName: 'admin',

    actions: {
        deny: function(){
            // deny the removal request
            var controller = this.get('controller'),
                records = this.get_values();

            controller.send('action', records, 'resolved', 'show');
        },
        allow: function(){
            debugger;
            // allow the removal request
            var controller = this.get('controller'),
                records = this.get_values();

            controller.send('action', records, 'resolved', 'hide');
        },

        clear_checkboxes: function(){
            var checkboxes = this.get_checkboxes();
            checkboxes.forEach(function(view){
                view.set('checked', false);
            });
        },
    },

    get_values: function(){
        var checkboxes = this.get_checked(),
            removal_requests = [];

        checkboxes.forEach(function(view){
            removal_requests.push(view.value);
        });

        return removal_requests;
    },

    get_checked: function() {
        var checkboxes = this.get_checkboxes(),
            checked = [];

        checkboxes.forEach(function(view){
            if (view.get('checked')) {
                checked.push(view);
            }
        });

        return checked;
    },

    get_checkboxes: function(){
        return this.get('childViews');
    },

});
