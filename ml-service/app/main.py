from fastapi import FastAPI, Depends, BackgroundTasks
from .schemas import AprioriRun
from .tasks import task_run_apriori#, celery
#from .apriori_service import run_apriori_from_df
from .correlacion_service import run_correlation_from_csv
from .db import SessionLocal, engine
from .models import Base, ReglaAprioriRun, ReglaAprioriRule, Producto, Venta
import os
# import logging
# logger = logging.getLogger(__name__)

import logging
import sys

from sqlalchemy import text
#from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("mlservice")


# crear tablas si no existen (solo local/dev)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5000",
#         "http://127.0.0.1:5000",
#         "http://mlservice:8001/pareto",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    logger.info("📌 FastAPI inició correctamente!")
    # Esto creará todas las tablas definidas en Base que no existan
    Base.metadata.create_all(bind=engine)


@app.get('/')
def root():
    return {"ok": True}

@app.get("/apriori/runs")
def get_runs():
    session = SessionLocal()
    runs = session.query(ReglaAprioriRun).order_by(ReglaAprioriRun.created_at.desc()).all()
    session.close()
    return [
        {
            "id": r.id,
            "created_at": r.created_at,
            "params": r.params
        }
        for r in runs
    ]

@app.get("/apriori/runs/{run_id}/rules")
def get_rules_by_run(run_id: int):
    session = SessionLocal()
    rules = session.query(ReglaAprioriRule).filter_by(run_id=run_id).order_by(ReglaAprioriRule.lift.desc()).limit(15).all()
    session.close()
    return [
        {
            "antecedents": rule.antecedents,
            "consequents": rule.consequents,
            "lift": rule.lift,
            "confidence": rule.confidence,
            "support": rule.support
        }
        for rule in rules
    ]


@app.post('/apriori/run')
def apriori_run(body: AprioriRun):
    # lanzar tarea en background (celery)
    task = task_run_apriori.delay(body.min_support, body.min_confidence)
    return {"task_id": task.id}

@app.get('/apriori/result')
def apriori_results():
    # ejemplo: leer última ejecución
    db = SessionLocal()
    res = db.execute("SELECT * FROM reglas_apriori ORDER BY id DESC LIMIT 1").fetchall()
    db.close()
    return {"latest": [dict(r) for r in res]}

@app.get('/correlacion')
def correlacion():  

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(BASE_DIR)
    csv_path = os.path.join(BASE_DIR, "..", "data", "Nestle.csv")

    #csv_path = os.getenv('NESTLE_CSV_PATH', 'data/Nestle.csv')

    logger.info("Entrando al endpoint /correlacion 🚀")
    logger.info(f"CSV path: {csv_path}")
    #print(csv_path)
    matrix, categorias = run_correlation_from_csv(csv_path, threshold=0.8)
    print('estoy en /correlacion')
    #print(data)
    #return data
    return {"matrix": matrix, "categories": categorias}  # temporalmente deshabilitado





PARETO_SQL = """
WITH base AS (
    SELECT
        v.producto_id,
        p.nombre AS producto,
        SUM(v.cantidad::numeric * p.precio::numeric) AS total_ventas
    FROM ventas v
    JOIN productos p ON v.producto_id = p.id
    GROUP BY v.producto_id, p.nombre
),
ordenado AS (
    SELECT
        producto_id,
        producto,
        total_ventas,
        SUM(total_ventas) OVER () AS total_general
    FROM base
),
acumulado AS (
    SELECT
        producto_id,
        producto,
        total_ventas,
        SUM(total_ventas) OVER (ORDER BY total_ventas DESC) AS acumulado,
        total_general
    FROM ordenado
)
SELECT
    producto_id,
    producto,
    total_ventas,
    acumulado,
    ROUND(acumulado * 100 / total_general, 2) AS porcentaje_acumulado
FROM acumulado
ORDER BY total_ventas DESC;
"""

@app.get("/pareto")
def get_pareto():

    db = SessionLocal()
    rows = db.execute(text(PARETO_SQL)).mappings().all()
    db.close()

    return rows

ROTACION_SQL = """
SELECT
    p.nombre AS producto,
    SUM(v.cantidad) AS total_vendido,
    COUNT(DISTINCT DATE(v.fecha)) AS dias_con_venta,
    ROUND(
        SUM(v.cantidad) / NULLIF(COUNT(DISTINCT DATE(v.fecha)), 0),
        2
    ) AS rotacion
FROM ventas v
JOIN productos p ON p.id = v.producto_id
GROUP BY p.nombre
ORDER BY rotacion DESC;
"""

@app.get("/rotacion")
def get_rotacion():
    db = SessionLocal()
    rows = db.execute(text(ROTACION_SQL)).mappings().all()
    db.close()
    return rows

TICKETPROMEDIO_SQL = """
    SELECT
        DATE(v.fecha) AS fecha,
        SUM((v.cantidad * p.precio)::numeric) AS total_ventas_dia,
        COUNT(*) AS tickets_dia,  -- si cada fila es una venta
        ROUND(SUM((v.cantidad * p.precio)::numeric) / COUNT(*), 2) AS ticket_promedio
    FROM ventas v
    JOIN productos p ON p.id = v.producto_id
    GROUP BY DATE(v.fecha)
"""

@app.get("/ticket_promedio")
def get_ticket_promedio():
    db = SessionLocal()
    rows = db.execute(text(TICKETPROMEDIO_SQL)).mappings().all()
    db.close()
    return rows