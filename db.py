# stdlib

# third-party
from sqlalchemy import (
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


metadata = MetaData()

ball_table = Table(
    'ball_table', metadata,
    Column('ball_table_id', Integer, primary_key=True),
    Column('ball_table_name', String),
    Column('ball_table_num', Integer)
)

attendee_table = Table(
    'attendee', metadata,
    Column('attendee_id', Integer, primary_key=True),
    Column('attendee_name', String),
    Column('show', Boolean),
    Column('ball_table_id', ForeignKey('ball_table.ball_table_id')))

removal_request_table = Table(
    'removal_request', metadata,
    Column('request_id', Integer, primary_key=True),
    Column('attendee_id', ForeignKey('attendee.attendee_id')),
    Column('ball_table_id', ForeignKey('ball_table.ball_table_id')),
    Column('remover_ident', String),
    Column('state', String)
)

Session = sessionmaker()


def wipe(engine, meta):
    import contextlib
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()


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
    query = dict_from_query(query)
    for attendee in query:

        cur_attendee_name = attendee['attendee_name'].lower().strip()
        if fuzz.ratio(cur_attendee_name, attendee_name) > 85:
            return attendee

    return False


if __name__ == '__main__':
    # wipe(engine, metadata)

    # do some stuff to ensure that there are enough ball_entry's in the db

    import os
    from sqlalchemy import create_engine

    default_url = settings.get('DATABASE_URL')
    db_url = os.environ.get("DATABASE_URL", default_url)

    engine = create_engine(db_url)
    engine.echo = False

    Session.configure(bind=engine)
    metadata.create_all(engine)

    conn = engine.connect()

    try:
        s = ball_table.select()
        rs = engine.execute(s)
        already_there = [
            int(x['table_name'].split()[-1])
            for x in rs]
        print('already_there:', already_there)

        for table_num in range(1, settings.get('table_num', 17) + 1):
            if table_num not in already_there:
                print('added;', table_num)
                ball_table_insert = ball_table.insert({
                    'ball_table_name': 'Table {}'.format(table_num),
                    'ball_table_num': table_num})
                engine.execute(ball_table_insert)
    finally:
        conn.close()
