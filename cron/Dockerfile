# Dockerfile.cron
FROM python:3.11-slim

WORKDIR /app

# Встановлення залежностей для psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY utils/get_data_script.py .

# Налаштування cron
RUN apt-get update && \
    apt-get install -y cron && \
    echo "*/5 * * * * python /app/get_data_script.py" > /etc/cron.d/get_data_cron && \
    chmod 0644 /etc/cron.d/get_data_cron && \
    crontab /etc/cron.d/get_data_cron

CMD ["cron", "-f"]
