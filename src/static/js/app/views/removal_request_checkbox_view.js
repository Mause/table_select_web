TableSelectWeb.RemovalRequestCheckboxView = Ember.Checkbox.extend({
    classNames: ["action_marker"],
    valueBinding: '',

    observer: function(){
        var box = this.get('controller.checked_removal_requests');

        var value = this.get('value');

        if (box.contains(value)) {
            box.removeObject(value);
        } else {
            box.addObject(value);
        }
    }.observes('checked')
});
