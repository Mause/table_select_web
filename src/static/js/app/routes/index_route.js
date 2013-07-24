define(['ember', 'models/ball_tables_model'],
    function(Ember, BallTable){
        'use strict';
        var IndexRoute = Ember.Route.extend({
            model: function () {
                return BallTable.find({});
            },

            renderTemplate: function(controller, model){
                this.render({
                    outlet: 'application'
                });
            }
        });

        IndexRoute.toString = function(){return 'IndexRoute';};

        return IndexRoute;
    }
);
