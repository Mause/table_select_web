function check(){
    'use strict';
    var keys = function(i){
        Ember.keys(i).forEach(function(elem){
            if (typeof(elem) == "string"){
                console.log('*', elem);
            }
        });
    };

    console.log('Routes;');
    keys(TableSelectWeb.Router.router.recognizer.names);
    console.log('Templates;');
    keys(Ember.TEMPLATES);
}
