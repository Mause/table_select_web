TableSelectWeb.RemovalRequest = DS.Model.extend({
    attendee_id: DS.belongsTo('attendee'),
    ball_table_id: DS.belongsTo('ball_table'),
    remover_ident: DS.attr('string'),
    state: DS.attr('string')
});
