# AGENTS.md - Guía para Agentes de Codificación

Este documento proporciona comandos y directrices de estilo para agentes que trabajan en este repositorio Bodega.

## Comandos de Desarrollo

### Docker Compose - Operaciones Principales
```bash
# Construir y levantar todos los servicios
docker compose up --build

# Levantar en modo detached (background)
docker compose up --build -d

# Detener todos los servicios
docker compose down

# Detener y eliminar volúmenes (limpieza completa)
docker compose down -v

# Ver logs de un servicio específico
docker compose logs -f mlservice
docker compose logs -f dashboard
docker compose logs -f worker
```

### Comandos por Servicio

**ML Service (FastAPI) - Puerto 8001:**
```bash
# Ejecutar un script dentro del contenedor
docker exec -it bodega_scaffold-mlservice-1 python -m scripts.cargar_data
docker exec -it bodega_scaffold-mlservice-1 python -m scripts.cargar_data2

# Instalar dependencias adicionales
docker exec -it bodega_scaffold-mlservice-1 pip install requests

# Shell interactivo
docker exec -it bodega_scaffold-mlservice-1 bash

# Test de endpoint desde dentro del contenedor
docker exec -i bodega_scaffold-mlservice-1 python3 - << 'EOF'
import requests
print(requests.get("http://localhost:8001/health").json())
EOF
```

**Dashboard (Flask) - Puerto 8000:**
```bash
# Shell interactivo
docker exec -it bodega_scaffold-dashboard-1 bash
```

**PostgreSQL - Puerto 5433:**
```bash
# Acceder a psql
docker exec -it bodega_scaffold-postgres-1 bash
psql -U postgres -d bodega

# Comandos psql útiles
\dt                    # Listar tablas
\d nombre_tabla        # Describir tabla
SELECT * FROM products LIMIT 10;
\q                     # Salir
```

### Comandos de Testing (Futuro - Pendiente de Implementación)
```bash
# Ejecutar todos los tests (pytest)
docker exec -it bodega_scaffold-mlservice-1 pytest

# Ejecutar un solo test específico
docker exec -it bodega_scaffold-mlservice-1 pytest tests/test_file.py::test_function_name

# Ejecutar tests con coverage
docker exec -it bodega_scaffold-mlservice-1 pytest --cov=app --cov-report=html

# Ejecutar tests en modo verbose
docker exec -it bodega_scaffold-mlservice-1 pytest -v
```

### Comandos de Linting y Formateo (Recomendados Agregar)
```bash
# Formatear código con Black
docker exec -it bodega_scaffold-mlservice-1 black app/ scripts/

# Verificar estilo con flake8
docker exec -it bodega_scaffold-mlservice-1 flake8 app/ scripts/

# Verificar tipos con mypy
docker exec -it bodega_scaffold-mlservice-1 mypy app/
```

## Directrices de Estilo de Código

### Python Backend (FastAPI, Flask, Celery)

**Imports - Ordenamiento:**
```python
# 1. Bibliotecas estándar de Python
import os
import logging
from datetime import datetime

# 2. Bibliotecas de terceros
import pandas as pd
import numpy as np
from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String
from celery import Celery

# 3. Imports locales (relativos al paquete app)
from .models import Producto, Venta
from .db import SessionLocal, engine
from .schemas import AprioriRun
```

**Convenciones de Nombres:**
- Variables y funciones: `snake_case` (ej: `min_support`, `run_apriori`)
- Clases: `PascalCase` (ej: `Producto`, `Venta`, `ReglaAprioriRun`)
- Constantes: `UPPER_SNAKE_CASE` (ej: `DATABASE_URL`, `REDIS_URL`)
- Módulos: `snake_case` (ej: `apriori_service.py`, `correlacion_service.py`)

**Type Hints y Pydantic:**
```python
# Usar Pydantic para modelos de API
from pydantic import BaseModel
from typing import List, Any

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

**Gestión de Sesiones de Base de Datos:**
```python
from .db import SessionLocal

# Opción 1: Context manager (recomendado)
def some_function():
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

# Opción 2: Manejo explícito
def another_function():
    db = SessionLocal()
    try:
        runs = db.execute("SELECT * FROM reglas_apriori ORDER BY id DESC LIMIT 1").fetchall()
        return [dict(r) for r in runs]
    finally:
        db.close()
```

**Logging:**
```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("mlservice")

# Uso en código
logger.info("Iniciando proceso de Apriori 🚀")
logger.error(f"Error al procesar: {e}")
```

**Manejo de Errores:**
```python
# Añadir try-except en operaciones críticas
try:
    rules = run_apriori_from_df(df, min_support, min_confidence)
except Exception as e:
    logger.error(f"Error ejecutando Apriori: {e}")
    raise HTTPException(status_code=500, detail="Error procesando Apriori")

# Validar respuestas de APIs externas
if "categories" not in response or "matrix" not in response:
    return "Error: JSON incompleto", 500
```

**Celery Tasks:**
```python
from celery import Celery

celery = Celery(__name__, broker=os.getenv('REDIS_URL'))

@celery.task
def task_run_apriori(min_support=0.005, min_confidence=0.05):
    # Import locales dentro de la tarea
    from .db import engine
    from .models import Producto
    import pandas as pd

    # Lógica de la tarea
    return {'status': 'ok', 'rules_count': len(rules)}

# Registrar tareas en celery_worker.py
celery.conf.imports = ['app.tasks']
```

**Comentarios y Documentación:**
- Mantener comentarios en español (consistente con el códigobase)
- Usar comentarios descriptivos para lógica compleja
- Ejemplo: `# JOIN: agregar nombre del producto`

### Flask Dashboard

**Patrones de Flask:**
```python
from flask import Flask, render_template, jsonify
import requests

ML_URL = os.getenv('MLSERVICE_URL', 'http://mlservice:8001')

@app.route('/api/correlacion')
def correlacion():
    r = requests.get(f"{ML_URL}/correlacion")
    response = r.json()
    
    # Validar estructura de respuesta
    if "categories" not in response or "matrix" not in response:
        return "Error: JSON incompleto", 500
    
    return render_template('correlaciones.html',
                          data=response["matrix"],
                          categorias=response["categories"])
```

### Frontend (JavaScript/CSS)

**CSS - Variables Globales:**
```css
:root {
    --bg: #071021;
    --panel: #0b1220;
    --muted: #94a3b8;
    --accent: #06b6d4;
    --accent2: #9b59ff;
    --warn: #ff7a59;
}

/* Usar variables */
.sidebar {
    background: linear-gradient(180deg, var(--accent2), var(--accent));
}
```

**JavaScript - ES6+:**
```javascript
// Modern patterns
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.nav-btn');
    
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Event handler logic
        });
    });
});

// Arrow functions, destructuring
const products = data.map(x => ({
    name: x.p,
    sales: x.sold,
    margin: ((x.price - x.cost) / x.price) * 100
}));
```

**Chart.js Configuration:**
```javascript
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Ventas',
            data: values,
            backgroundColor: '#4bc0c0'
        }]
    },
    options: {
        plugins: {
            legend: { display: false }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});
```

## Configuración de Servicios

**URLs y Puertos:**
- Dashboard (Flask): http://localhost:8000
- ML Service (FastAPI): http://localhost:8001
- PostgreSQL: localhost:5433
- Redis: localhost:6379

**Variables de Entorno (.env):**
- `DATABASE_URL`: URL de conexión a PostgreSQL
- `REDIS_URL`: URL de conexión a Redis
- `MLSERVICE_URL`: URL del servicio ML (desde dashboard)
- `NESTLE_CSV_PATH`: Ruta al dataset Nestle.csv

## Patrones de Proyecto

**SQLAlchemy Models:**
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    categoria = Column(String(50))
    precio = Column(Float)
    ventas = relationship("Venta", back_populates="producto")
```

**FastAPI Endpoints:**
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post('/apriori/run')
def apriori_run(body: AprioriRun):
    task = task_run_apriori.delay(body.min_support, body.min_confidence)
    return {"task_id": task.id}
```

**Health Checks en Docker:**
Todos los servicios deben tener health checks:
- PostgreSQL: `pg_isready -U ${POSTGRES_USER}`
- Redis: `redis-cli ping`
- ML Service: `curl -f http://localhost:8001/health || exit 1`

## Notas Importantes

1. **Lenguaje de Comentarios**: Mantener todos los comentarios en español
2. **Error Handling**: Agregar try-except con logging en operaciones críticas
3. **Session Management**: Siempre cerrar sesiones de base de datos
4. **Docker First**: La mayoría de operaciones deben ejecutarse dentro de contenedores
5. **Celery Tasks**: Importar dependencias locales dentro de la tarea
6. **Logging**: Usar logger configurado para el servicio (stream a stdout para Docker)
7. **Code Comments**: NO agregar comentarios innecesarios o redundantes

## Testing Pendiente de Implementar

Para cuando se agreguen tests:
- Usar pytest como framework de testing
- Estructura: `tests/` con archivos `test_*.py`
- Tests unitarios para servicios y endpoints
- Tests de integración para endpoints de API
- Mock de dependencias externas (PostgreSQL, Redis) cuando sea apropiado
