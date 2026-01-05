# AGENTS.md - Guía para Agentes de Codificación

Este documento proporciona comandos y directrices de estilo para agentes que trabajan en este repositorio Bodega.

## Comandos de Desarrollo

### Docker Compose
```bash
docker compose up --build      # Construir y levantar servicios
docker compose up --build -d   # Modo detached
docker compose down            # Detener servicios
docker compose logs -f mlservice|dashboard|worker  # Logs en vivo
```

### Ejecución de Tests
```bash
# Todos los tests
docker exec -it bodega_scaffold-mlservice-1 pytest

# Test específico
docker exec -it bodega_scaffold-mlservice-1 pytest tests/test_file.py::test_function_name

# Con coverage
docker exec -it bodega_scaffold-mlservice-1 pytest --cov=app --cov-report=html

# Verbose
docker exec -it bodega_scaffold-mlservice-1 pytest -v
```

### Linting y Formateo
```bash
docker exec -it bodega_scaffold-mlservice-1 black app/ scripts/
docker exec -it bodega_scaffold-mlservice-1 flake8 app/ scripts/
docker exec -it bodega_scaffold-mlservice-1 mypy app/
```

### Scripts y Scripts de Datos
```bash
docker exec -it bodega_scaffold-mlservice-1 python -m scripts.cargar_data
docker exec -it bodega_scaffold-mlservice-1 python -m scripts.cargar_data2
docker exec -it bodega_scaffold-mlservice-1 bash
```

### PostgreSQL
```bash
docker exec -it bodega_scaffold-postgres-1 bash
psql -U postgres -d bodega  # \dt, \d tabla, \q
```

## Directrices de Estilo de Código

### Python - Imports (ordenados)
```python
# 1. Bibliotecas estándar
import os
import logging
from datetime import datetime

# 2. Bibliotecas de terceros
import pandas as pd
from fastapi import FastAPI
from sqlalchemy import Column

# 3. Imports locales
from .models import Producto
from .db import SessionLocal
```

### Convenciones de Nombres
- Variables/funciones: `snake_case` (ej: `min_support`, `run_apriori`)
- Clases: `PascalCase` (ej: `Producto`, `Venta`, `AprioriRun`)
- Constantes: `UPPER_SNAKE_CASE` (ej: `DATABASE_URL`)
- Módulos: `snake_case` (ej: `apriori_service.py`)

### Type Hints y Pydantic
```python
from pydantic import BaseModel
from typing import List

class AprioriRun(BaseModel):
    min_support: float = 0.01
    min_confidence: float = 0.3

class Rule(BaseModel):
    antecedents: List[str]
    consequents: List[str]
    support: float
    confidence: float
    lift: float
```

### Gestión de Sesiones de Base de Datos
```python
from .db import SessionLocal

def function():
    session = SessionLocal()
    try:
        results = session.query(Producto).all()
        session.commit()
        return results
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {e}")
        raise
    finally:
        session.close()
```

### Logging
```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("mlservice")

logger.info("Mensaje informativo")
logger.error(f"Error: {e}")
```

### Manejo de Errores
```python
from fastapi import HTTPException

try:
    rules = run_apriori_from_df(df, min_support, min_confidence)
except Exception as e:
    logger.error(f"Error ejecutando Apriori: {e}")
    raise HTTPException(status_code=500, detail="Error procesando Apriori")

# Validar respuestas de APIs externas
if "categories" not in response or "matrix" not in response:
    return "Error: JSON incompleto", 500
```

### Celery Tasks
```python
@celery.task
def task_run_apriori(min_support=0.005, min_confidence=0.05):
    from .db import engine  # Importar locales dentro de la tarea
    from .models import Producto
    return {'status': 'ok', 'rules_count': len(rules)}

# Registrar en celery_worker.py
celery.conf.imports = ['app.tasks']
```

### Flask Dashboard
```python
from flask import Flask, render_template, jsonify
import requests

ML_URL = os.getenv('MLSERVICE_URL', 'http://mlservice:8001')

@app.route('/api/correlacion')
def correlacion():
    r = requests.get(f"{ML_URL}/correlacion")
    response = r.json()
    if "categories" not in response or "matrix" not in response:
        return "Error: JSON incompleto", 500
    return render_template('correlaciones.html',
                          data=response["matrix"],
                          categorias=response["categories"])
```

### Frontend - JavaScript/CSS
```javascript
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.nav-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => { /* handler */ });
    });
});

const products = data.map(x => ({
    name: x.p,
    sales: x.sold,
    margin: ((x.price - x.cost) / x.price) * 100
}));
```

```css
:root {
    --bg: #071021;
    --panel: #0b1220;
    --accent: #06b6d4;
    --accent2: #9b59ff;
}

.sidebar {
    background: linear-gradient(180deg, var(--accent2), var(--accent));
}
```

## Configuración de Servicios

| Servicio | URL/Puerto |
|----------|------------|
| Dashboard (Flask) | http://localhost:8000 |
| ML Service (FastAPI) | http://localhost:8001 |
| PostgreSQL | localhost:5433 |
| Redis | localhost:6379 |

**Variables de Entorno (.env):**
- `DATABASE_URL`: PostgreSQL connection
- `REDIS_URL`: Redis connection
- `MLSERVICE_URL`: ML service URL (from dashboard)
- `NESTLE_CSV_PATH`: Path to Nestle.csv dataset

## Notas Importantes

1. **Comentarios**: Mantener en español, solo cuando sea necesario
2. **Error Handling**: Usar try-except con logging en operaciones críticas
3. **Session Management**: Siempre cerrar sesiones de base de datos
4. **Docker First**: Ejecutar operaciones dentro de contenedores
5. **Celery Tasks**: Importar dependencias locales dentro de la tarea
6. **Logging**: Stream a stdout para compatibilidad con Docker
7. **Sin comentarios redundantes**: El código debe ser auto-documentado
