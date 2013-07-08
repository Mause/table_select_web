var $;
var console;
var Handlebars;

// Ember.LOG_BINDINGS = true;
Ember.LOG_VERSION = true;
Ember.ENV.RAISE_ON_DEPRECATION = true;
Ember.LOG_STACKTRACE_ON_DEPRECATION = true;

function check(){
    'use strict';
    var keys = function(i){
        Ember.keys(i).forEach(function(elem){
            if (typeof(elem) == "string"){
                console.log(elem);
            }
        });
    };

    console.log('Routes;');
    keys(TableSelectWeb.Router.router.recognizer.names);
    console.log('Templates;');
    keys(Ember.TEMPLATES);
}

// Em.View.reopen({
//     templateForName: function(name, type) {
//         if (!name) { return; }
//         // console.log('Get;', name);
//         Em.assert("templateNames are not allowed to contain periods: "+name, name.indexOf('.') === -1);

//         var templates = Em.get(this, 'templates'),
//             template = Em.get(templates, name);

//         if (!template) {
//             $.ajax({
//                 url: 'static/templates/%@.hbs'.fmt(name),
//                 async: false,
//                 success: function(data) {
//                     template = Em.Handlebars.compile(data);
//                     console.log('Got from remote;', name);
//                 },
//                 failure: function(){
//                     console.warning('Get Error');
//                 }
//             });
//         }

//         if (!template) {
//             throw new Em.Error('%@ - Unable to find %@ "%@".'.fmt(this, type, name));
//         }

//         if (typeof Em.TEMPLATES[name] === 'undefined') {
//             Em.TEMPLATES[name] = template;
//         }

//         return template;
//     }
// });

window.TableSelectWeb = Ember.Application.create({
    title: 'Ball Table Select',
    author: 'Dominic May (http://mause.me)',
    LOG_TRANSITIONS: true,
    LOG_ACTIVE_GENERATION: true,
    LOG_TRANSITIONS_INTERNAL: true,
    LOG_VIEW_LOOKUPS: true,
    rootElement: 'body'
});


// API.prototype.request_remove_attendee = function(attendee_id, table_id, success, failure){
//     "use strict";
//     $.ajax({
//         type: 'POST',
//         url: this.base_url + '/attendee/remove',
//         data: {
//             'attendee_id': attendee_id,
//             'table_id': table_id},
//         success: success,
//         failure: failure
//     });
// };

// App.prototype.request_remove_attendee = function(element){
//     element = $(element);
//     var attendee_id = element.data('attendeeId');
//     var table_id = element.data('tableId');

//     var win = function(data){
//         console.log(
//             'removal request sent for attendee with attendee_id', attendee_id + ',',
//             'on table with table_id', table_id);
//         _this = window.app;
//         _this.notif(element, 'Removal request successfully submitted');
//         window.setTimeout(app.refresh, 10);
//     };

//     var fail = function(data){
//         console.log('fail');
//         _this.notif(element, 'Removal request submission failed');
//     };

//     this.data.api.request_remove_attendee(attendee_id, table_id, win, fail);
// };

// App.prototype.setupListeners = function() {
//     "use strict";
//     var _this = this;

//     // Reload the data from the server
//     $('a.refresh').on('click', function(event) {
//         _this.refresh();
//     });

//     $('a.request_remove_attendee').on('click', function(event){
//         var element = $(event.target);
//         var attendee_id = element.data('id');
//         _this.request_remove_attendee(attendee_id);
//     });

//     $('.submit_attendee').submit(_this.submit_attendee);

//     $('.removal_request_notif').tooltip({placement: 'bottom'});
// };

// App.prototype.notif = function(element, text, timeout) {
//     "use strict";
//     // convenience function \o/
//     $('#myModalLabel').text(text);
//     $('#myModal').modal();
// };


// App.prototype.submit_attendee = function(event) {
//     "use strict";
//     var _this = window.app;

//     var win = function(data){
//         console.log('successfully added', attendee_name, 'to table with id', table_id);
//         if (data.success === true){
//             _this.hideLoadingSpinner();
//             _this.refresh();

//             _this.notif(element, 'Attendee add was successful');
//         } else {
//             console.log('Add attendee failed');
//             _this.notif(element, data.human_error);
//         }
//         return false;
//     };

//     var element = $(event.target);
//     var attendee_name = $(event.target.attendee_name).val();
//     var table_id = $(event.target.table_id).val();
//     if (attendee_name && table_id){
//         _this.data.api.add_attendee(attendee_name, table_id, win);
//         window.setTimeout(app.refresh, 10);
//     } else {

//     }
//     // return false to ensure that the browser does not continue posting the
//     // results of the form itself
//     return false;
// };

// App.prototype.showLoadingSpinner = function() {
//     // show spinner
//     // (may implement if we end up spending enough time that the user gets frustrated)
// };

// App.prototype.hideLoadingSpinner = function() {
//     // hide spinner
//     // (may implement if we end up spending enough time that the user gets frustrated)
// };

// var app;
// $(document).ready(function(){
//     "use strict";
//     // when the document is ready, start the app :D
//     app = new App();
// });
