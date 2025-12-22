FROM python:3.10-slim

WORKDIR /app

COPY worker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY ml-service/app/ ./app/
COPY worker/celery_worker.py ./worker/


ENV PYTHONPATH="/app"

CMD ["celery", "-A", "worker.celery_worker.celery", "worker", "--loglevel=info"]


