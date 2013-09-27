TableSelectWeb.AdminView = Ember.View.extend({
    templateName: 'admin',

    actions: {
        deny: function(){
            'use strict';
            // deny the removal request
            var controller = this.get('controller');

            controller.send('action', 'resolved', 'show');
        },
        allow: function(){
            'use strict';
            // allow the removal request
            var controller = this.get('controller');

            controller.send('action', 'resolved', 'hide');
        }
    }
});
