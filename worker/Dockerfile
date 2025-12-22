FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

ENV PYTHONPATH=/app

CMD ["celery", "-A", "celery_worker.celery", "worker", "--loglevel=info"]
