TableSelectWeb.RemovalRequest = DS.Model.extend({
    attendee: DS.belongsTo('TableSelectWeb.Attendee'),
    ball_table: DS.belongsTo('TableSelectWeb.BallTable'),
    remover_ident: DS.attr('string'),
    state: DS.attr('string')
});

TableSelectWeb.Serializer.configure('TableSelectWeb.RemovalRequest', {
    primaryKey: 'request_id',
    alias: 'removal_request'
});
