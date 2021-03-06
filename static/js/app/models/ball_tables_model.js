TableSelectWeb.BallTable = TableSelectWeb.Model.extend({
    primaryKey: 'ball_table_id',
    ball_table_name: DS.attr('string'),
    full: DS.attr('boolean'),
    ball_table_num: DS.attr('number'),
    attendees: DS.hasMany('TableSelectWeb.Attendee', {embedded: 'load'}),

    row_end: function() {
        // this is for display purposes only
        var ball_table_num = this.get('ball_table_num');
        row_end = ball_table_num % 2 === 0;

        return row_end;
    }.property('ball_table_num').cacheable()
});
