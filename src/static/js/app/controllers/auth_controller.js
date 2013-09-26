TableSelectWeb.AuthController = Ember.ArrayController.extend(Ember.Evented, {
    username: '',
    password: '',

    actions: {
        submitAuthFormEvent: function(){
            var adapter = this.store.adapterFor({}),
                url = adapter.buildURL('me'),
                username = this.get('username'),
                password = this.get('password'),
                self = this;

            // clear the form
            this.set('username', '');
            this.set('password', '');

            // cleanup the values
            if (!(username = username.trim())) { return; }

            // cleanup the values
            if (!(password = password.trim())) { return; }

            // record ftw
            var data = {
                username: username,
                password: password
            };

            adapter.ajax(url, 'POST', {data: data}).then(function(data){
                // on success, setup the appropriate internal variables
                TableSelectWeb.AuthManager.authenticate(
                    data.api_key.access_token,
                    data.api_key.user_id
                );

                // and transtion to the admin page
                self.transitionToRoute('admin');

            }, function(xhr){
                if (xhr.status === 401) {
                    sendNotification(Ember.String.loc('invalid_login'));
                } else {
                    debugger;
                    sendNotification('Unknown login error');
                    TableSelectWeb.AuthManager.reset();
                    console.log(arguments);
                }
            });
        }
    }
});

Ember.Inflector.inflector.uncountable('me');
