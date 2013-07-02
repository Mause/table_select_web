TableSelectWeb.Attendee = DS.Model.extend({
    attendee_name: DS.attr('string'),
    show: DS.attr('boolean'),
    table_id: DS.belongsTo('TableSelectWeb.BallTable')
});
