var $;
var console;
var document;

$(document).ready(function(){
    "use strict";
    var base_url = '/api';

    var get_request_ids = function(checked){
        var element = null,
            selected = [];

        for (var i=0; i<checked.length; i++){
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
            for (var i=0; i<checked.length; i++){
                console.log(checked[i]);
                checked[i].parent.hide();
            }
        };

        $.ajax({
            type: 'POST',
            url: base_url + '/admin/attendee/' + action + '_bulk',
            data: JSON.stringify(selected_requests),
            success: success
            // failure: failure
        });
    };

    var do_action = function(action){
        var checked = get_checked();
        var request_ids = get_request_ids(checked);
        commit_action(action, request_ids, checked);
    };

    $('#deny_button').click(function(){
        do_action('deny');
    });

    $('#allow_button').click(function(){
        do_action('allow');
    });
});
