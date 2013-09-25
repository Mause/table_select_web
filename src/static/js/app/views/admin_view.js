TableSelectWeb.AdminView = Ember.View.extend({
    templateName: 'admin',

    actions: {
        deny: function(){
            // deny the removal request
            var controller = this.get('controller');

            controller.send('action', 'resolved', 'show');
        },
        allow: function(){
            // allow the removal request
            var controller = this.get('controller');

            controller.send('action', 'resolved', 'hide');
        }
    }
});
