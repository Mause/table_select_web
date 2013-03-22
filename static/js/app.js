var API = function() {};

API.prototype.base_url = '/api';

API.prototype.getTables = function(success, failure) {
    var win = function(data) {
        // console.log(data);
        if(success)
            success(data);
    };

    var fail = function() {
        if(failure)
            failure();
    };

    $.ajax({
        dataType: "json",
        url: this.base_url + '/tables',
        success: win,
        failure: fail
    });
};

API.prototype.request_remove_attendee = function(attendee_id, success, failure){
    var win = function(data){
        if (success){
            success(data);
        }
    };

    var fail = function(){
        if (failure){
            failure();
        }
    };

    $.ajax({
        url: this.base_url + '/attendee/remove',
        data: {'attendee_id': attendee_id},
        success: win,
        failure: fail
    });
};

var Data = function() {
    this.api = new API();

    // this.tables holds the current data representation of the tables
    this.tables = {};
};

/* -- API Updating -- */

Data.prototype.updateFromServer = function(callback) {
    var _this = this;

    var win = function(data) {
        _this.tables = data;
        // _this.indexData();

        if(callback)
            callback();
    };

    var fail = function() {
        if(callback)
            callback();
    };

    this.api.getTables(win, fail);
};

/* -- Standard getters/setters -- */

Data.prototype.getTables = function() {
    return this.tables;
};

// // App specific data request
// Data.prototype.getContactWithEmail = function(email) {
//     var contact;
//     // Retrieve the contact from our index datastructure
//     return contact;
// };

var App = function() {
    this.data = new Data();
    // this.template = '...';

    this.render();
    this.setupListeners();
};

App.prototype.render = function() {
    var html;
    console.log(this.data.getTables());
    // Use this.template && this.data.getContacts() to render HTML
    return html;
};

App.prototype.request_remove_attendee = function(attendee_id, success, failure){
    this.data.api.request_remove_attendee(attendee_id, success, failure);
};

App.prototype.setupListeners = function() {
    var _this = this;

    // Reload the data from the server
    $('button.refresh').on('click', function(event) {
        _this.refresh();
    });

    $('a.request_remove_attendee').on('click', function(event){
        var element = $(event.target);
        var attendee_id = element.data('id');
        _this.request_remove_attendee(attendee_id);
    });
};

App.prototype.refresh = function () {
    var _this = this;

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
