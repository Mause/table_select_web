TableSelectWeb.AuthController = Ember.ArrayController.extend(Ember.Evented, {
    username: '',
    password: '',

    actions: {
        submitAuthFormEvent: function(){
            'use strict';
            var adapter = this.store.adapterFor({}),
                url = adapter.buildURL('me'),
                username = this.get('username'),
                password = this.get('password');

            // clear the form
            this.set('username', '');
            this.set('password', '');

            // cleanup the values
            if (!(username = username.trim())) { return; }
            if (!(password = password.trim())) { return; }

            // record ftw
            var data = {
                username: username,
                password: password
            };

            adapter.ajax(url, 'POST', {data: data}).then(
                this.auth_success,
                this.auth_failure
            );
        }
    },

    auth_success: function(data){
        // on success, setup the appropriate internal variables
        TableSelectWeb.AuthManager.authenticate(
            data.api_key.access_token,
            data.api_key.user_id
        );

        // and transtion to the admin page
        self.transitionToRoute('admin');
    },

    auth_failure: function(xhr){
        if (xhr.status === 401) {
            sendNotificationLoc('invalid_login');
        } else {
            debugger;
            sendNotificationLoc('unknown_login_error');
            TableSelectWeb.AuthManager.reset();
        }
    }
});

Ember.Inflector.inflector.uncountable('me');
