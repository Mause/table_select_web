// Handlebars.log = function(level, object) {console.log(level, object);};

var API = function() {};

API.prototype.base_url = '/api';

API.prototype.getTables = function(success, failure) {
    var win = function(data) {
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
    var _this = this;

    _this.data.updateFromServer(function() {
        // We've now got new data to show
        _this.render();
        _this.hideLoadingSpinner();
    });

    this.setupListeners();
};

App.prototype.templates = {};
App.prototype.templates.tables = Handlebars.compile($('#tableTemplate').html());


App.prototype.render = function() {
    var html;
    var _this = this.app === undefined ? this : this.app;

    data = {tables: _this.data.tables};
    console.log(data);

        $('#tableContainer').html(_this.templates.tables(data));
};

    // function refresh_events(data){
    //     $('.h-feed').html(
    //         $("#eventTemplate").render(data)
    //     );
    // }


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

var app;
$(document).ready(function(){
    app = new App();
});
