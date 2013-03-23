// Handlebars.log = function(level, object) {console.log(level, object);};
var $;
var gevent;
var console;
var window;

var API = function() {};

API.prototype.base_url = '/api';

API.prototype.getTables = function(success, failure) {
    "use strict";
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
    "use strict";
    $.ajax({
        type: 'POST',
        url: this.base_url + '/attendee/remove',
        data: {'attendee_id': attendee_id},
        success: success,
        failure: failure
    });
};


API.prototype.add_attendee = function(attendee_name, table_id, success, failure){
    "use strict";
    $.ajax({
        dataType: "json",
        type: "POST",
        url: this.base_url + '/attendee/add',
        data: {
            'attendee_name': attendee_name,
            'table_id': table_id
        },
        success: success,
        failure: failure
    });
};


var Data = function() {
    "use strict";
    this.api = new API();

    // this.tables holds the current data representation of the tables
    this.tables = {};
};

/* -- API Updating -- */

Data.prototype.updateFromServer = function(callback) {
    "use strict";
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
    "use strict";
    return this.tables;
};

// // App specific data request
// Data.prototype.getContactWithEmail = function(email) {
//     var contact;
//     // Retrieve the contact from our index datastructure
//     return contact;
// };

var App = function() {
    "use strict";
    this.data = new Data();
    // this.template = '...';
    var _this = this;

    _this.data.updateFromServer(function() {
        // We've now got new data to show
        _this.render();
        _this.hideLoadingSpinner();
        _this.setupListeners();
    });

};

App.prototype.templates = {};
App.prototype.templates.tables = Handlebars.compile($('#tableTemplate').html());


App.prototype.render = function() {
    "use strict";
    var html;
    var _this = this.app === undefined ? this : this.app;

    var data = {tables: _this.data.tables};
    $('#tableContainer').html(_this.templates.tables(data));
};

    // function refresh_events(data){
    //     $('.h-feed').html(
    //         $("#eventTemplate").render(data)
    //     );
    // }


// silly straight through methods -.-
App.prototype.request_remove_attendee = function(attendee_id, success, failure){
    this.data.api.request_remove_attendee(attendee_id, success, failure);
};

App.prototype.add_attendee = function(attendee_name, table_id, success, failure){
    this.data.api.add_attendee(attendee_name, table_id, success, failure);
};

App.prototype.setupListeners = function() {
    "use strict";
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

    $('.submit_attendee').submit(_this.submit_attendee);
};

App.prototype.refresh = function () {
    "use strict";
    var _this = this;

    _this.showLoadingSpinner();

    _this.data.updateFromServer(function() {
        // We've now got new data to show
        _this.render();
        _this.hideLoadingSpinner();
    });
};

App.prototype.submit_attendee = function(event) {
    "use strict";
    var _this = window.app;

    gevent = event;
    console.log(event);
    var attendee_name = $(gevent.target.attendee_name).val();
    if (attendee_name){
        var table_id = $(gevent.target.table_id).val();
        console.log(attendee_name, table_id);

        _this.add_attendee(
            attendee_name, table_id,
            function(data){
                if (data.success === true){
                    _this.hideLoadingSpinner();
                    _this.refresh();
                    // console.log(data);
                }
        });
    }
    return false;
};

App.prototype.showLoadingSpinner = function() {
    // show spinner
};

App.prototype.hideLoadingSpinner = function() {
    // hide spinner
};

var app;
$(document).ready(function(){
    "use strict";
    app = new App();
});
