from celery import Celery
import os
import sys

# Aseguramos que /app esté en el path
#sys.path.append('/app')

celery = Celery(
    'worker',
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL')
)


# Esto es vital: Celery necesita registrar las tareas al iniciar
# El nombre 'app.tasks' debe ser importable desde donde lances el worker
celery.conf.imports = [
    'app.tasks', 
]

# Opcional: Configuraciones adicionales
celery.conf.task_ignore_result = False


# Importar tareas explícitamente
# try:
#     import app.tasks
#     print("Tasks imported correctly!")
# except Exception as e:
#     print("Error importing tasks:", e)

#celery.autodiscover_tasks(['app'])
