var ApplicationSerializer = DS.ActiveModelSerializer.extend({});

TableSelectWeb.RemovalRequestSerializer = ApplicationSerializer.extend({
    primaryKey: 'request_id',
    alias: 'removal_request',
});

TableSelectWeb.BallTableSerializer = ApplicationSerializer.extend({
    primaryKey: 'ball_table_id',
    attendees: { embedded: 'load' },
});

TableSelectWeb.AttendeeSerializer = ApplicationSerializer.extend({
    primaryKey: 'attendee_id',
});
