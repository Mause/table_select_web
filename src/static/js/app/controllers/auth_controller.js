TableSelectWeb.AuthController = Ember.ArrayController.extend(Ember.Evented, {
    username: '',
    password: '',

    actions: {
        submitAuthFormEvent: function(){
            var username = this.get('username'),
                password = this.get('password');

            this.send('login', {
                username: username,
                password: password
            });
        }
    }
});
