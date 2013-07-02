TableSelectWeb.BallTable = DS.Model.extend({
    table_name: DS.attr('string'),
    full: DS.attr('boolean'),
    table_num: DS.attr('integer'),
    attendees: DS.hasMany('TableSelectWeb.Attendee'),

    row: function() {
        // this is for display purposes only
        var table_num = this.get('table_num');
        row = table_num % 2 === 0;

        return row;
    }.property('table_num').cacheable()
});
