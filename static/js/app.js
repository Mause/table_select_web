var API = function() {};

API.prototype.base_url = '/api';

API.prototype.getContacts = function(success, failure) {
    var win = function(data) {
        if(success)
            success(data);
    };

    var fail = function() {
        if(failure)
            failure();
    };

    $.ajax(this.base_url + '/contacts', {
        success: win,
        failure: fail
    });
};

var Data = function() {
    this.api = new API();
    this.contacts = this.readFromStorage();
    this.indexData();
};

Data.prototype.indexData = function() {
    // Do indexing task (e.g. store contact via email)
};

/* -- API Updating -- */

Data.prototype.updateFromServer = function(callback) {
    var _this = this;

    var win = function(data) {
        _this.contacts = data;
        _this.indexData();

        if(callback)
            callback();
    };

    var fail = function() {
        if(callback)
            callback();
    };

    this.api.getContacts(win, fail);
};

/* -- Data serialisation -- */

Data.prototype.readFromStorage = function() {
    var c = JSON.parse(window.localStorage.getItem('appData'));

    // Ensure a sensible default
    return c || [];
};

Data.prototype.writeToStorage = function() {
    window.localStorage.setItem('appData', JSON.stringify(this.contacts));
};

/* -- Standard getters/setters -- */

Data.prototype.getContacts = function() {
    return this.contacts;
};

// App specific data request
Data.prototype.getContactWithEmail = function(email) {
    var contact;
    // Retrieve the contact from our index datastructure
    return contact;
};

var App = function() {
    this.data = new Data();
    this.template = '...';

    this.render();
    this.setupListeners();
};

App.prototype.render = function() {
    var html;
    // Use this.template && this.data.getContacts() to render HTML
    return html;
};

App.prototype.setupListeners = function() {
    var _this = this;

    // Reload the data from the server
    $('button.refresh').on('click', function(event) {
        _this.refresh();
    });
};

App.prototype.refresh = function () {
    _this.showLoadingSpinner();

    _this.data.updateFromServer(function() {
        // We've now got new data to show
        _this.render();
        _this.hideLoadingSpinner();
    });
};

App.prototype.showLoadingSpinner = function() {
    // show spinner
};

App.prototype.hideLoadingSpinner = function() {
    // hide spinner
};


app = new App();
