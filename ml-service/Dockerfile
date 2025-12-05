FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias incluyendo gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación
COPY ./app ./app
COPY ./scripts ./scripts
COPY ./data ./data

# Exponer puerto
EXPOSE 8001

# Comando para producción con Gunicorn + Uvicorn worker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--workers", "3", "--timeout", "120", "--bind", "0.0.0.0:8001", "app.main:app"]
