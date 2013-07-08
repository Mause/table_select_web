TableSelectWeb.RemovalRequest = DS.Model.extend({
    attendee_id: DS.belongsTo('TableSelectWeb.Attendee'),
    ball_table_id: DS.belongsTo('TableSelectWeb.BallTable'),
    remover_ident: DS.attr('string'),
    state: DS.attr('string')
});
