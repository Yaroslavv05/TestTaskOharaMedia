# Dockerfile.get_data
FROM python:3.11-slim

WORKDIR /app

# Встановлення залежностей для psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY utils/get_data_script.py .
COPY utils/models.py .

CMD ["python", "get_data_script.py"]
