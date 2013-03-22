from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    Integer,
    String,
    Column,
    ForeignKey)
from sqlalchemy.orm import sessionmaker


def wipe(engine, meta):
    import contextlib
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()

engine = create_engine("postgresql+pg8000://postgres:pass@localhost")
engine.echo = False  # Try changing this to True and see what happens

conn = engine.connect()
metadata = MetaData(engine)


ball_table = Table('ball_table', metadata,
    Column('table_id', Integer, primary_key=True),
    # Column('name', String(40))
)

attendee = Table('attendee', metadata,
    Column('attendee_id', Integer, primary_key=True),
    Column('attendee_name', String),
    Column('table_id', ForeignKey('ball_table.table_id')))

metadata.create_all()

Session = sessionmaker(bind=engine)


def get_tables(session):
    fields = ['attendee_id', 'attendee_name', 'table_id']

    tables = []

    ball_tables = ball_table.select()
    result = ball_tables.execute()
    for row in result:
        table_id = row['table_id']

        query = session.query(attendee).filter_by(
            table_id=table_id)

        attendees = [dict(zip(fields, x)) for x in query.all()]

        tables.append({
            'table_id': table_id,
            'attendees': attendees
        })
    return tables


if __name__ == '__main__':
    wipe(engine, metadata)
    # from pprint import pprint
    import json

    with open('names.json') as fh:
        names = json.load(fh)

    ball_table_insert = ball_table.insert()
    attendee_insert = attendee.insert()
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
        # print(row.name, 'is', row.age, 'years old')

    # row = rs.fetchone()
    # print('Id:', row[0])
    # print('Name:', row['name'])
    # print('Age:', row.age)
    # print('Password:', row[users.c.password])
