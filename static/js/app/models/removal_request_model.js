TableSelectWeb.RemovalRequest = TableSelectWeb.Model.extend({
    attendee: DS.belongsTo('TableSelectWeb.Attendee'),
    ball_table: DS.belongsTo('TableSelectWeb.BallTable'),
    remover_ident: DS.attr('string'),
    state: DS.attr('string')
});
