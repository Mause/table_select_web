function get_keys(obj) {
    'use strict';
    // Helpers that operate with 'this' within an #each
    var keys = [];

    function filter_for_own(obj) {
        var own = [];
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) { own.push(key); }
        }
        return own;
    }

    // var meta = obj[META_KEY], desc = meta && meta.descs[keyName], ret;
    // if (obj.hasOwnProperty('get')) keys = merge(filter_for_own(obj.get(obj)), keys);
    // keys = merge(filter_for_own(meta.values), keys);
    keys = Ember.merge(keys, filter_for_own(obj));

    return Ember.keys(keys);
}


function notif(element, text, timeout) {
    "use strict";
    // convenience function \o/
    $('#myModalLabel').text(text);
    $('#myModal').modal();
}

TableSelectWeb.ModalControllerMixin = Ember.Mixin.create({
    close: function() {
        this.willClose();
        this.get('view').destroy();
        this.destroy();
    },
    willClose: Em.K
});


Ember.Handlebars.registerHelper('control_smart', function(path, modelPath, options) {
    // to make sure each table has a unique controller,
    // and hence a controller that has the right info,
    // we give it a new controlID each time.
    // not ideal, but w/e
    options.hash.controlID = 'control-smart-' + String(options.data.keywords.ball_table.id);

    Ember.Handlebars.helpers.control.call(this, path, modelPath, options);
});
