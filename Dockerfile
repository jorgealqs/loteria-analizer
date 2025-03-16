FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY analizer /app

CMD ["uvicorn", "analizer.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]