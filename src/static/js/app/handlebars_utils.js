(function(){
    Ember.Handlebars.registerHelper('log_content', function(property, options) {
        var context = (options.contexts && options.contexts[0]) || this,
            normalized = Ember.Handlebars.normalizePath(context, property, options.data),
            pathRoot = normalized.root,
            path = normalized.path,
            value = (path === 'this') ? pathRoot : Ember.Handlebars.get(pathRoot, path, options);

        console.log(value.get('isLoaded'), value.get('content').length);
    });


    var _control_smart_id = 0;
    Ember.Handlebars.registerHelper('control_smart', function(path, modelPath, options) {
        // to make sure each table has a unique controller,
        // and hence a controller that has the right info,
        // we give it a new controlID each time.
        // not ideal, but w/e
        options.hash.controlID = 'control-smart-' + String(_control_smart_id++);

        Ember.Handlebars.helpers.control.call(this, path, modelPath, options);
    });
})();
