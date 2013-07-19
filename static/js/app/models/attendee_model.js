TableSelectWeb.Attendee = TableSelectWeb.Model.extend({
    attendee_name: DS.attr('string'),
    show: DS.attr('boolean'),
    ball_table: DS.belongsTo('TableSelectWeb.BallTable')
});

// DS.RESTAdapter.map('TableSelectWeb.Attendee', {
//     primaryKey: 'attendee_id'
// });
