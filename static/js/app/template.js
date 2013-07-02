// compiling on the fly aint the best, but its good enough for what we're doing
// if this was a fully fledged webapp, i would consider pre-compiling the templates though :P
templates = [
    '_attendee_list',
    '_single_attendee'
];

for (var i=0; i<templates.length; i++){
    var source = $('[data-template-name="' + templates[i] + '"]').html();
    console.assert(source, 'Not found: ' + templates[i]);

    Ember.TEMPLATES[templates[i]] = Ember.Handlebars.compile(source);
}

// {
//     getResources: function (path, callback) {
//         $.ajax({
//             dataType: 'jsonp text',
//             crossDomain: true,
//             url: path,
//             success: function (data) {
//                 utils.async(function () {
//                     callback(data)
//                 });
//             },
//             error: function (jqXHR, textStatus, errorThrown) {
//                 console.log("Can't complete request. error: " + textStatus);
//                 throw errorThrown;
//             }
//         });
//     },
//     injectWidgetTemplate: function (templateName, callback) {
//         if (Ember.TEMPLATES[templateName]) {
//             console.log("template " + templateName + " already injected to the page");
//             return callback(templateName);
//         }
//         this.getResources("http://something.myserver.com/template/" + templateName, function (template) {
//             Ember.TEMPLATES[templateName] = Ember.Handlebars.compile(template);
//             callback(templateName);
//         });
//     }
// }
