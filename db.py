# stdlib
import os

# third-party
from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    Integer,
    String,
    Column,
    ForeignKey,
    Boolean)
from fuzzywuzzy import fuzz
from sqlalchemy.orm import sessionmaker

# application specific
from settings import settings
from utils import dict_from_query


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
        settings.get('DATABASE_URL')))
    engine.echo = False  # Try changing this to True and see what happens

    conn = engine.connect()
    metadata = MetaData(engine)

    ball_table = Table(
        'ball_table', metadata,
        Column('table_id', Integer, primary_key=True),
        Column('table_name', String),
        Column('table_num', Integer)
    )

    attendee_table = Table(
        'attendee', metadata,
        Column('attendee_id', Integer, primary_key=True),
        Column('attendee_name', String),
        Column('show', Boolean),
        Column('table_id', ForeignKey('ball_table.table_id')))

    removal_request_table = Table(
        'removal_request', metadata,
        Column('request_id', Integer, primary_key=True),
        Column('attendee_id', ForeignKey('attendee.attendee_id')),
        Column('table_id', ForeignKey('ball_table.table_id')),
        Column('remover_ident', String),
        Column('state', String)
    )

    metadata.create_all()

    Session = sessionmaker(bind=engine)

    return (
        metadata, engine, conn, Session,
        ball_table, attendee_table, removal_request_table)

(metadata, engine, conn, Session,
    ball_table, attendee_table, removal_request_table) = setup()


def get_tables(session):

    # tables = []

    raw_tables = dict_from_query(session.query(ball_table).all())
    return raw_tables
    # for row in raw_tables:
    #     tables.append({
    #         'table_id': row['table_id'],
    #         'table_name': row['table_name']})

    #     query = session.query(attendee_table).filter_by(
    #         table_id=row['table_id'], show=True)

    #     attendees = dict_from_query(query.all())

    #     tables[-1].update({
    #         'attendees': attendees,
    #         'attendee_num': len(attendees),
    #         'full': (len(attendees) >= settings.get('max_pax_per_table', 10))
    #     })

    # return tables


def does_attendee_exist_dumb(session, attendee_name):
    "does a simple check if any other attendees have the same name"
    query = session.query(attendee_table).filter_by(
        attendee_name=attendee_name, show=True)
    query = query.all()
    return dict_from_query(query)


def does_attendee_exist_smart(session, attendee_name):
    """uses fuzzy matching to determine
    whether someone is trying to dupe the app"""
    attendee_name = attendee_name.lower().strip()

    query = session.query(attendee_table).filter_by(show=True).all()
    for attendee in query:
        attendee = dict_from_query(attendee)

        cur_attendee_name = attendee['attendee_name'].lower().strip()
        if fuzz.ratio(cur_attendee_name, attendee_name) > 85:
            return attendee

    return False


if __name__ == '__main__':
    # wipe(engine, metadata)

    # do some stuff to ensure that there are enough ball_entry's in the db

    s = ball_table.select()
    rs = s.execute()
    already_there = [
        int(x['table_name'].split()[-1])
        for x in rs]
    print('already_there:', already_there)

    ball_table_insert = ball_table.insert()
    for table_num in range(1, settings.get('table_num', 17) + 1):
        if table_num not in already_there:
            print('added;', table_num)
            ball_table_insert.execute(
                {
                    'table_name': 'Table {}'.format(table_num),
                    'table_num': table_num})
