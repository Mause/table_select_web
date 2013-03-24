import os
import json

from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    Integer,
    String,
    Column,
    ForeignKey)
from sqlalchemy.orm import sessionmaker
from fuzzywuzzy import fuzz

with open('settings.json') as fh:
    settings = json.load(fh)


def wipe(engine, meta):
    import contextlib
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()


def setup():
    engine = create_engine(os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:pass@localhost"))
    engine.echo = False  # Try changing this to True and see what happens

    conn = engine.connect()
    metadata = MetaData(engine)

    ball_table = Table('ball_table', metadata,
        Column('table_id', Integer, primary_key=True),
        # Column('name', String(40))
    )

    results = ball_table.select()
    if not results.execute():
        tables = [
            {'table_id': id}
            for id in range(1, settings.get('table_num', 17) + 1)]
        ball_table.insert().execute(tables)

    attendee_table = Table('attendee', metadata,
        Column('attendee_id', Integer, primary_key=True),
        Column('attendee_name', String),
        Column('table_id', ForeignKey('ball_table.table_id')))

    removal_request_table = Table('removal_request', metadata,
        Column('request_id', Integer, primary_key=True),
        Column('attendee_id', ForeignKey('attendee.attendee_id')),
        Column('table_id', ForeignKey('ball_table.table_id')),
        Column('remover_ident', String))

    metadata.create_all()

    Session = sessionmaker(bind=engine)

    return (metadata, engine, conn, Session,
        ball_table, attendee_table, removal_request_table)

(metadata, engine, conn, Session,
    ball_table, attendee_table, removal_request_table) = setup()


def get_tables(session):
    fields = ['attendee_id', 'attendee_name', 'table_id']

    # these next two lines really shouldn't be here
    # but w/e. they basically create a framework for the tables to slot into
    # and at the same time create empty tables
    tables = {
        table_id: {'table_id': table_id}
        for table_id in range(1, settings.get('table_num', 17) + 1)}

    ball_tables = ball_table.select()
    result = ball_tables.execute()
    for row in result:
        table_id = row['table_id']

        query = session.query(attendee_table).filter_by(
            table_id=table_id)

        attendees = [dict(zip(fields, x)) for x in query.all()]

        tables[table_id]['attendees'] = attendees

    return tables


def does_attendee_exist_dumb(session, attendee_name):
    "does a simple check if any other attendees have the same name"
    fields = ['attendee_id', 'attendee_name', 'table_id']

    query = session.query(attendee_table).filter_by(
        attendee_name=attendee_name)
    query = query.all()
    return [dict(zip(fields, x)) for x in query]


def does_attendee_exist(session, attendee_name):
    """uses fuzzy matching to determine
    whether someone is trying to dupe the app"""
    fields = ['attendee_id', 'attendee_name', 'table_id']

    query = session.query(attendee_table).all()
    # logging.info('{} attendees'.format(len(query)))

    for attendee in query:
        _, cur_attendee_name, _ = attendee
        if fuzz.ratio(cur_attendee_name, attendee_name) > 85:
            return dict(zip(fields, attendee))

    return False


if __name__ == '__main__':
    wipe(engine, metadata)
    # from pprint import pprint
    import json

    with open('names.json') as fh:
        names = json.load(fh)

    ball_table_insert = ball_table.insert()
    attendee_insert = attendee_table.insert()
    for id in range(1, 11):
        ball_table_insert.execute({'table_id': id})

        att = []
        for x in range(10):
            att.append({
                'attendee_name': names.pop(),
                'table_id': id})
        attendee_insert.execute(att)

    s = ball_table.select()
    rs = s.execute()
    for row in rs:
        print(dict(row))
