TableSelectWeb.Attendee = TableSelectWeb.Model.extend({
    primaryKey: 'attendee_id',
    attendee_name: DS.attr('string'),
    show: DS.attr('boolean'),
    ball_table: DS.belongsTo('TableSelectWeb.BallTable')
});
