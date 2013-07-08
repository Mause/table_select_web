TableSelectWeb.Router.map(function(){
    this.resource('index', {path: '/'});
    this.resource('info', {path: '/info'});
});

TableSelectWeb.Router.reopen({
    location: 'history'
});
