var $;
var console;
var document;

$(document).ready(function(){
    "use strict";
    var base_url = '/api';

    var get_request_ids = function(checked){
        var element = null,
            selected = [];

        for (var i; i<checked.length; i++){
            element = $(checked[i]);
            selected.push(element.data('requestId'));
        }
        return selected;
    };

    var get_checked = function(){
        return $('.action_marker:checked');
    };

    var commit_action = function(action, selected_requests, checked){
        var possible_actions = ['deny', 'allow'];
        if (possible_actions.indexOf(action) == -1){
            throw new Error('bad action');
        }

        var success = function(data){
            checked.forEach(function(element){
                element.parent.hide();
            });
        };

        $.ajax({
            type: 'POST',
            url: base_url + '/admin/attendee/' + action + '_bulk',
            data: JSON.stringify(selected_requests),
            success: success
            // failure: failure
        });
    };


    $('#deny_button').click(function(){
        var checked = get_checked();
        console.assert(checked.length);
        console.log(checked);
        var request_ids = get_request_ids(checked);
        console.log(request_ids);
        commit_action('deny', request_ids, checked);
    });

    $('#allow_button').click(function(){

    });
});
