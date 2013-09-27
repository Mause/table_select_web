TableSelectWeb.RemovalRequestCheckboxView = Ember.Checkbox.extend({
    classNames: ["action_marker"],
    valueBinding: '',
    destinationBinding: '',

    observer: function(){
        var box = this.get('destination'),
            value = this.get('value');

        if (box.contains(value)) {
            box.removeObject(value);
        } else {
            box.addObject(value);
        }
    }.observes('checked')
});
