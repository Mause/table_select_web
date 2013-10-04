TableSelectWeb.ErrorHandlerMixin = Ember.Mixin.create({
    handle_errors: function(errors, context, error_handlers){
        if (arguments.length != 3){
            error_handlers = this.error_handlers;
        } else {
            console.log("YOGO");
        }

        errors = this.reformat_errors(errors, error_handlers);
        var self = this;

        return new Ember.RSVP.Promise(function(resolve, reject){
            try {
                self.handle_errors_recurse(errors, context, resolve);
            } catch (e) {
                // reject the promise. poor promise :(
                reject();

                // stacktrace is preserved, right?
                throw e;
            }
        });
    },

    reformat_errors: function(errors, error_handlers) {
        var valid_errors = [];

        var _reformat_error = function(error){
            valid_errors.push({
                type: key,
                error: error,
                handler: error_handlers[key]
            });
        };

        for (var key in errors) {
            if (!errors.hasOwnProperty(key)) continue;

            if (Ember.keys(error_handlers).contains(key)){
                errors[key].forEach(_reformat_error);
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
            closed_callback,
            error = errors.pop();

        closed_callback = function(){
            self.handle_errors_recurse(errors, context, resolve);
        };

        result = error.handler(error.error, context);

        if (result.notification) {
            sendNotification(result.notification, closed_callback);
        } else {
            handle_errors_recurse(errors, context);
        }
    }
});
