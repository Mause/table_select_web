Ember.Handlebars.registerHelper('log_content', function(property, options) {
    var context = (options.contexts && options.contexts[0]) || this,
        normalized = Ember.Handlebars.normalizePath(context, property, options.data),
        pathRoot = normalized.root,
        path = normalized.path,
        value = (path === 'this') ? pathRoot : Ember.Handlebars.get(pathRoot, path, options);

    console.log(value.get('isLoaded'), value.get('content').length);
});

Ember.Handlebars.registerHelper('log_label', function(label, property, options) {
  var context = (options.contexts && options.contexts[0]) || this,
      normalized = Ember.Handlebars.normalizePath(context, property, options.data),
      pathRoot = normalized.root,
      path = normalized.path,
      value = (path === 'this') ? pathRoot : Ember.Handlebars.get(pathRoot, path, options);
  Ember.Logger.log('%@:'.fmt(label), value);
});

Ember.Handlebars.registerHelper('bs-link-to', function(name, options){
  options.hash['class'] = 'btn';
   // btn-default';
  options.hash['tag'] = 'button';

  return Ember.Handlebars.helpers['link-to'](name, options);
});
