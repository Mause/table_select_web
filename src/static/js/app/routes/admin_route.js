define(['ember', 'models/removal_request_model'],
    function(Ember, RemovalRequest){
        'use strict';
        var AdminRoute = Ember.Route.extend({
            model: function () {
                return RemovalRequest.find({});
            },

            renderTemplate: function(controller, model){
                this.render({
                    outlet: 'application'
                });
            }
        });

        AdminRoute.toString = function(){return 'AdminRoute';};

        return AdminRoute;
    }
);
