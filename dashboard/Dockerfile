FROM python:3.10-slim
WORKDIR /dashboard
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app
COPY start.sh /start.sh
RUN chmod +x /start.sh
EXPOSE 8000


CMD ["gunicorn", "--workers", "3", "--timeout", "120", "--bind", "0.0.0.0:8000", "app.run:app"]

