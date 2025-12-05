# Bodega - ML FastAPI + Flask Dashboard

Levanta localmente con Docker Compose: PostgreSQL, Redis, FastAPI (ML), Celery worker y Flask dashboard.

## Requisitos
- Docker & Docker Compose

## Levantar en local
1. Copiar .env.example -> .env y ajustar credenciales
2. `docker compose up --build`
3. Dashboard: http://localhost:8000
   ML API: http://localhost:8001

## Flujo
- Flask hace requests a FastAPI para obtener reglas/forecast
- FastAPI puede ejecutar tareas en background (Celery)
- Resultados guardados en PostgreSQL



docker exec -it bodega_scaffold-postgres-1 bash
psql -U postgres -d bodega
\dt
\d nombre_tabla
SELECT * FROM products LIMIT 10;
\q


docker compose down
docker compose up --build -d
-------------------------------
docker compose up --build
-----------------------------------

para correr data 
-------------------------------------------
docker exec -it bodega_scaffold-mlservice-1 bash
python -m scripts.cargar_data

------------------------------------------------

docker compose down -v
docker compose up --build

-------------------------------

docker compose logs -f servicio

------------------------------------------

FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app

COPY scripts /app/scripts
COPY data /app/data

COPY start.sh /start.sh
RUN chmod +x /start.sh
# Copiar dataset
COPY data /data
EXPOSE 8001
CMD ["/start.sh"]
-------------------------------------------------------------------


docker exec -i bodega_scaffold-mlservice-1 python3 - << 'EOF'

import requests
print(requests.get("http://localhost:8001/correlacion").json())
EOF
{'rows': ['llega tarde']}


-------------------------------------
docker exec -it bodega_scaffold-mlservice-1 pip install requests





