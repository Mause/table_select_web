TableSelectWeb.Attendee = DS.Model.extend({
    attendee_name: DS.attr('string'),
    show: DS.attr('boolean'),
    ball_table: DS.belongsTo('ball_table'),
    removal_request_exists: DS.attr('boolean')
});
