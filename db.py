# stdlib

# third-party
from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
    Boolean)
from sqlalchemy.ext.declarative import declarative_base

from fuzzywuzzy import fuzz
from sqlalchemy.orm import sessionmaker, relationship

# application specific
from settings import settings
from utils import dict_from_query


Base = declarative_base()


class BaseMixin(object):
    def items(self):
        for key in self.__mapper__.attrs.keys():
            yield (key, getattr(self, key))


class BallTable(Base, BaseMixin):
    __tablename__ = 'ball_table'

    # our stuff
    ball_table_id = Column(Integer, primary_key=True)
    ball_table_name = Column(String)
    ball_table_num = Column(Integer)

    # other guys stuff
    attendees = relationship("AttendeeTable", backref="BallTable")


class AttendeeTable(Base, BaseMixin):
    __tablename__ = 'attendee'

    # our stuff
    attendee_id = Column(Integer, primary_key=True)
    attendee_name = Column(String)
    show = Column(Boolean, default=True)

    # other guys stuff
    ball_table_id = Column(Integer, ForeignKey('ball_table.ball_table_id'))


class RemovalRequestTable(Base, BaseMixin):
    __tablename__ = 'removal_request'

    request_id = Column(Integer, primary_key=True)
    attendee_id = Column(Integer, ForeignKey('attendee.attendee_id'))
    ball_table_id = Column(Integer, ForeignKey('ball_table.ball_table_id'))
    remover_ident = Column(String)
    state = Column(String)


# ball_table = Table(
#     'ball_table', metadata,
#     Column('ball_table_id', Integer, primary_key=True),
#     Column('ball_table_name', String),
#     Column('ball_table_num', Integer),
#     Column('attendees', HasMany(
#         own='ball_table.ball_table_id',
#         theirs='attendee.ball_table_id'))
# )

# attendee_table = Table(
#     'attendee', metadata,
#     Column('attendee_id', Integer, primary_key=True),
#     Column('attendee_name', String),
#     Column('show', Boolean, default=True),
#     Column('ball_table_id', ForeignKey('ball_table.ball_table_id'))
# )

# removal_request_table = Table(
#     'removal_request', metadata,
#     Column('request_id', Integer, primary_key=True),
#     Column('attendee_id', ForeignKey('attendee.attendee_id')),
#     Column('ball_table_id', ForeignKey('ball_table.ball_table_id')),
#     Column('remover_ident', String),
#     Column('state', String)
# )

Session = sessionmaker()


def does_attendee_exist_dumb(session, attendee_name):
    "does a simple check if any other attendees have the same name"
    query = session.query(AttendeeTable).filter_by(
        attendee_name=attendee_name, show=True)
    query = query.all()
    return dict_from_query(query)


def does_attendee_exist_smart(session, attendee_name):
    """uses fuzzy matching to determine
    whether someone is trying to dupe the app"""
    attendee_name = attendee_name.lower().strip()

    query = session.query(AttendeeTable.__table__)
    query = query.filter_by(show=True).all()
    query = dict_from_query(query)
    for attendee in query:

        cur_attendee_name = attendee['attendee_name'].lower().strip()
        if fuzz.ratio(cur_attendee_name, attendee_name) > 85:
            return attendee

    return False


def wipe(engine):
    import contextlib
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()


def main():
    # do some stuff to ensure that there are enough ball_entry's in the db

    import os
    import sys
    from sqlalchemy import create_engine

    default_url = settings.get('DATABASE_URL')
    db_url = os.environ.get("DATABASE_URL", default_url)

    engine = create_engine(db_url)
    engine.echo = False

    if 'wipe' in sys.argv:
        print('Wiping')
        wipe(engine)
        print('Done wiping')

    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    conn = engine.connect()

    try:
        if 'interact' in sys.argv:
            from pprint import pprint as pp
            ppl = lambda x: pp(list(x))
            import code
            l = globals()
            l.update(locals())
            code.interact(local=l)

        else:
            existing_tables = engine.execute(BallTable.__table__.select())

            existing_table_ids = [table.ball_table_num for table in existing_tables]
            print('existing_table_ids:', existing_table_ids)

            for table_num in range(1, settings.get('table_num', 17) + 1):
                if table_num not in existing_table_ids:
                    print('added;', table_num)
                    ball_table_insert = BallTable.__table__.insert({
                        'ball_table_name': 'Table {}'.format(table_num),
                        'ball_table_num': table_num})
                    engine.execute(ball_table_insert)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
