define(['ember'], function(Ember){
    'use strict';
    var InfoRoute = Ember.Route.extend({
        renderTemplate: function(controller, model){
            this.render({
                outlet: 'application'
            });
        }
    });

    InfoRoute.toString = function(){return 'InfoRoute';};

    return InfoRoute;
});
