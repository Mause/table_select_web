TableSelectWeb.BallTable = DS.Model.extend({
    // ball_table_id: DS.attr('integer'),
    ball_table_name: DS.attr('string'),
    full: DS.attr('boolean'),
    ball_table_num: DS.attr('number'),
    attendees: DS.hasMany('TableSelectWeb.Attendee'),

    row_end: function() {
        // this is for display purposes only
        var ball_table_num = this.get('ball_table_num');
        row_end = ball_table_num % 2 === 0;

        return row_end;
    }.property('ball_table_num').cacheable()
});

// DS.RESTAdapter.map("TableSelectWeb.BallTable", {
//     name: { key: 'ball_table_id' }
// });
