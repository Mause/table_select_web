TableSelectWeb.Attendee = TableSelectWeb.Model.extend({
    attendee_name: DS.attr('string'),
    show: DS.attr('boolean'),
    ball_table: DS.belongsTo('TableSelectWeb.BallTable'),
    removal_request_exists: DS.attr('boolean')
});

TableSelectWeb.Serializer.configure('TableSelectWeb.Attendee', {
    primaryKey: 'attendee_id'
});
