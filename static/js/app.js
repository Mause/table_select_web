// Handlebars.log = function(level, object) {console.log(level, object);};
var $;
var window;
var console;
var Handlebars;

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

API.prototype.request_remove_attendee = function(attendee_id, table_id, success, failure){
    "use strict";
    $.ajax({
        type: 'POST',
        url: this.base_url + '/attendee/remove',
        data: {
            'attendee_id': attendee_id,
            'table_id': table_id},
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

var App = function() {
    "use strict";
    this.data = new Data();
    var _this = this;

    _this.data.updateFromServer(function() {
        // We've now got new data to show
        _this.render();
        _this.hideLoadingSpinner();
        _this.setupListeners();
    });

};

// compiling on the fly aint the best, but its good enough for what we're doing
// if this was a fully fledged webapp, i would consider pre-compiling the templates though :P
templates = {
    add_attendee_form: '#add_attendee_form_template',
    attendee_list: '#attendee_list_template',
    single_attendee: '#single_attendee_template'
};

for (var template_name in templates){
    var source = $(templates[template_name]).html();
    Handlebars.registerPartial(template_name, source);
}

App.prototype.templates = {};
App.prototype.templates.tables = Handlebars.compile(
    $('#table_template').html());


App.prototype.render = function() {
    "use strict";
    var _this = window.app;

    var tables = _this.data.tables;
    for (var key in tables){
        tables[key].row = tables[key].table_id % 2 === 0;
    }

    var data = {"tables": tables};
    $('#tableContainer').html(_this.templates.tables(data));
};

App.prototype.request_remove_attendee = function(element){
    element = $(element);
    var attendee_id = element.data('attendeeId');
    var table_id = element.data('tableId');
    console.log(
        'removal request sent for attendee with attendee_id', attendee_id + ',',
        'on table with table_id', table_id);

    var win = function(data){
        _this = window.app;
        _this.tooltip(element, 'removal request successfully submitted');
        console.log('win');
    };

    var fail = function(data){
        console.log('fail');
        _this.tooltip(element, 'removal request submission failed');
    };

    this.data.api.request_remove_attendee(attendee_id, table_id, win, fail);
};

App.prototype.setupListeners = function() {
    "use strict";
    var _this = this;

    // Reload the data from the server
    $('a.refresh').on('click', function(event) {
        _this.refresh();
    });

    $('a.request_remove_attendee').on('click', function(event){
        var element = $(event.target);
        var attendee_id = element.data('id');
        _this.request_remove_attendee(attendee_id);
    });

    $('.submit_attendee').submit(_this.submit_attendee);
    $('.submit_attendee').tooltip({
        placement: 'right',
        trigger: 'manual'
    });

    $('.spec_close').tooltip({
        placement: 'right',
        trigger: 'manual'
    });
};

App.prototype.refresh = function () {
    "use strict";
    var _this = this;

    _this.showLoadingSpinner();

    _this.data.updateFromServer(function() {
        // We've now got new data to show
        _this.render();
        _this.setupListeners();
        _this.hideLoadingSpinner();
    });
};

App.prototype.tooltip = function(element, text, timeout) {
    "use strict";
    element.attr('title', text);
    console.dir(element);
    element.tooltip('show');

    window.setTimeout(function(){
        element.tooltip('hide');
        element.attr('title', '');
    }, timeout || 1500);
};


App.prototype.submit_attendee = function(event) {
    "use strict";
    var _this = window.app;

    var element = $(event.target);
    var attendee_name = $(event.target.attendee_name).val();
    if (attendee_name){
        var table_id = $(event.target.table_id).val();
        console.log(
            'adding', attendee_name,
            'to table with id', table_id);

        _this.data.api.add_attendee(attendee_name, table_id,
            function(data){
                console.log(data);
                if (data.success === true){
                    _this.hideLoadingSpinner();
                    _this.refresh();

                    _this.tooltip(element, 'attendee add was successful');
                } else {
                    console.log('Add attendee failed');
                    _this.tooltip(element, data.human_error);
                }
                return false;
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
