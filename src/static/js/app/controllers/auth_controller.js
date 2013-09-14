TableSelectWeb.AuthController = Ember.ArrayController.extend(Ember.Evented, {
    username: '',
    password: '',

    actions: {
        submitAuthFormEvent: function(){
            var adapter = this.store.adapterFor({typeKey: 'me'}),
                url = adapter.buildURL('me'),
                self = this,
                username = this.get('username'),
                password = this.get('password');

            // clear the form
            this.set('username', '');
            this.set('password', '');

            // cleanup the values
            username = username.trim();
            if (!username) { return; }

            // cleanup the values
            password = password.trim();
            if (!password) { return; }

            // record ftw
            var data = {
                username: username,
                password: password
            };

            adapter.ajax(url, 'POST', {data: data}).then(function(data){
                // on success, setup the appropriate internal variables
                TableSelectWeb.AuthManager.authenticate(
                    data.api_key.access_token,
                    data.api_key.user_id);

                // and transtion to the admin page
                self.transitionToRoute('admin');

            }, function(xhr){
                if (xhr.status === 401) {
                    sendNotification('Invalid login credentials');
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
