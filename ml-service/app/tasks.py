from celery import Celery
import os
import pandas as pd
from .db import SessionLocal
from .apriori_service import run_apriori_from_df, save_rules
from .models import Venta, Producto

celery = Celery(__name__, broker=os.getenv('REDIS_URL'))

@celery.task
def task_run_apriori(min_support=0.01, min_confidence=0.3):
    from .db import engine
    import sqlalchemy as sa
    from .models import Producto  # Asegurar import
    import pandas as pd

    with engine.connect() as conn:
        ventas_df = pd.read_sql_table('ventas', conn)
        productos_df = pd.read_sql_table('productos', conn)

    # JOIN: agregar nombre del producto
    df = ventas_df.merge(productos_df[['id', 'nombre']], left_on='producto_id', right_on='id', how='left')
    df = df.rename(columns={'nombre': 'producto'})
    
    print('dfffffff')
    print(df)

    # Ahora ya existe ticket_id y producto 😄
    rules = run_apriori_from_df(df[['ticket_id', 'producto']], min_support, min_confidence)

    session = SessionLocal()
    save_rules(session, rules, {'min_support': min_support, 'min_confidence': min_confidence})
    session.close()

    return {'status': 'ok', 'rules_count': len(rules)}


