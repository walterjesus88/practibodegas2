import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData

SQLITE_URL = 'sqlite:///db.sqlite3'
PG_URL = 'postgresql://walter:TuClave123@localhost:5432/ventas_db'

engine_sql = create_engine(SQLITE_URL)
engine_pg = create_engine(PG_URL)

meta = MetaData()
meta.reflect(bind=engine_sql)
meta.create_all(bind=engine_pg)

for table in meta.sorted_tables:
    data = engine_sql.execute(table.select()).fetchall()
    if data:
        engine_pg.execute(table.insert(), [dict(r) for r in data])

print('Migración finalizada')
