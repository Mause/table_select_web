TableSelectWeb.Attendee = DS.Model.extend({
    attendee_name: DS.attr('string'),
    show: DS.attr('boolean'),
    ball_table: DS.belongsTo('TableSelectWeb.BallTable')
});
