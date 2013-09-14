TableSelectWeb.ErrorHandlerMixin = Ember.Mixin.create({
    handle_errors: function(errors, error_handlers, context){
        errors = this.reformat_errors(errors, error_handlers);
        var _this = this;

        return new Ember.RSVP.Promise(function(resolve, reject){
            try {
                _this.handle_errors_recurse(errors, context, resolve);
            } catch (e) {
                console.error(e);
            }
        });
    },

    reformat_errors: function(errors, error_handlers) {
        var valid_errors = [];

        for (var key in errors) {
            if (!errors.hasOwnProperty(key)) continue;

            if (Ember.keys(error_handlers).contains(key)){
                for (var i=0; i<errors[key].length; i++) {
                    valid_errors.push({
                        type: key,
                        error: errors[key][i],
                        handler: error_handlers[key]
                    });
                }
            } else {
                console.warn('An unknown error for "%@" occured: %@'.fmt(
                    key, errors[key]));
            }
        }

        return valid_errors;
    },

    handle_errors_recurse: function(errors, context, resolve){
        if (Ember.isEmpty(errors)) {
            resolve();
            return;
        }

        var result,
            self = this,
            error = errors.pop();

        console.log(error);
        result = error.handler(error.error, context);

        var closed_callback = function(){
            self.handle_errors_recurse(errors, context, resolve);
        };

        if (result.notification) {
            sendNotification(result.notification, closed_callback);
        } else {
            handle_errors_recurse(errors, context);
        }
    }
});
