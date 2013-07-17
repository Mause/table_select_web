// these tend to spam :/
// Ember.LOG_BINDINGS = true;
// Ember.STRUCTURED_PROFILE = true;

Ember.LOG_VERSION = true;
Ember.ENV.RAISE_ON_DEPRECATION = true;
Ember.LOG_STACKTRACE_ON_DEPRECATION = true;
Ember.DEBUG = true;

function check(){
    'use strict';
    var keys = function(i){
        Ember.keys(i).forEach(function(elem){
            if (typeof(elem) == "string"){
                console.log('*', elem);
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

// App = function () {};
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
