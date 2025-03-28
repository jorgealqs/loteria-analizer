FROM python:3.11-slim

# Instala dependencias necesarias para Chrome y Chromedriver
RUN apt-get update && apt-get install -y wget unzip curl \
    chromium chromium-driver -y

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

COPY app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]