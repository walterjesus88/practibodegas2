from celery import Celery
import os
import sys

# Aseguramos que /app esté en el path
sys.path.append('/app')

celery = Celery(
    'worker',
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL')
)

# Importar tareas explícitamente
try:
    import app.tasks
    print("Tasks imported correctly!")
except Exception as e:
    print("Error importing tasks:", e)

celery.autodiscover_tasks(['app'])
