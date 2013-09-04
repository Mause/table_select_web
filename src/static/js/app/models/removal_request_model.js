TableSelectWeb.RemovalRequest = DS.Model.extend({
    attendee: DS.belongsTo('attendee'),
    ball_table: DS.belongsTo('ball_table'),
    remover_ident: DS.attr('string'),
    state: DS.attr('string')
});
