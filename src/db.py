# stdlib
from contextlib import closing

# third-party
from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
    Boolean)
from fuzzywuzzy import fuzz
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# application specific
from settings import settings
from utils import dict_from_query


Base = declarative_base()


class BaseMixin(object):
    def items(self):
        keys = (
            prop.key
            for prop in self.__mapper__.iterate_properties
        )

        for key in keys:
            yield (key, getattr(self, key))


class BallTable(Base, BaseMixin):
    __tablename__ = 'ball_table'

    # our stuff
    ball_table_id = Column(Integer, primary_key=True)
    ball_table_name = Column(String)
    ball_table_num = Column(Integer)

    # other guys stuff
    attendees = relationship("Attendee")


class Attendee(Base, BaseMixin):
    __tablename__ = 'attendee'

    # our stuff
    attendee_id = Column(Integer, primary_key=True)
    attendee_name = Column(String)
    show = Column(Boolean, default=True)
    removal_request_exists = Column(Boolean, default=False)

    # other guys stuff
    ball_table_id = Column(
        Integer,
        ForeignKey('ball_table.ball_table_id')
    )


class RemovalRequestTable(Base, BaseMixin):
    __tablename__ = 'removal_request'

    request_id = Column(Integer, primary_key=True)
    attendee_id = Column(Integer, ForeignKey('attendee.attendee_id'))
    ball_table_id = Column(Integer, ForeignKey('ball_table.ball_table_id'))
    remover_ident = Column(String)
    state = Column(String)

Session = sessionmaker()


def does_attendee_exist_dumb(session, attendee_name):
    "does a simple check if any other attendees have the same name"

    query = session.query(Attendee)
    query = query.filter_by(attendee_name=attendee_name, show=True)
    query = query.all()

    return dict_from_query(query)


def does_attendee_exist_smart(session, attendee_name):
    """
    uses fuzzy matching to determine
    whether someone is trying to dupe the app

    TODO: determine whether the overhead is worth it
    """
    attendee_name = attendee_name.lower().strip()

    query = session.query(Attendee)
    query = query.filter_by(show=True).all()
    query = dict_from_query(query)

    for attendee in query:
        cur_attendee_name = attendee['attendee_name'].lower().strip()
        if fuzz.ratio(cur_attendee_name, attendee_name) > 85:
            return attendee

    return False


def wipe(engine):
    with closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()


def main():
    # do some stuff to ensure that there are enough ball_tables in the db

    import sys
    from sqlalchemy import create_engine

    db_url = settings.get('DATABASE_URL')

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
        from pprint import pprint as pp
        if 'interact' in sys.argv:
            ppl = lambda x: pp(list(x))

            import code
            l = globals()
            l.update(locals())
            code.interact(local=l)

        else:
            table_num = settings.get('table_num', 17)

            session = Session()

            query = session.query(BallTable)
            query = query.all()

            pp(query)

            existing_table_ids = [
                table.ball_table_num
                for table in query
            ]
            print('existing_table_ids:', existing_table_ids)

            for table_num in range(1, table_num + 1):
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
