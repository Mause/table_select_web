TableSelectWeb.AuthController = Ember.ArrayController.extend(Ember.Evented, {
    username: '',
    password: '',

    actions: {
        submitAuthFormEvent: function(){
            var username = this.get('username'),
                password = this.get('password'),
                adapter = this.store.adapterFor({typeKey: 'me'}),
                url = adapter.buildURL('me'),
                self = this;

            var data = {
                username: username,
                password: password
            };

            adapter.ajax(url, 'POST', {data: data}).then(function(data){
                TableSelectWeb.AuthManager.authenticate(
                    data.api_key.access_token,
                    data.api_key.user_id);
                self.transitionToRoute('/');

            }, function(xhr){
                debugger;
                if (xhr.status === 401) {
                    this.set('password', '');
                    sendNotification('Invalid login credentials');
                } else {
                    sendNotification('Unknown login error');
                    TableSelectWeb.AuthManager.reset();
                    console.log(arguments);
                }
            });
        }
    }
});
