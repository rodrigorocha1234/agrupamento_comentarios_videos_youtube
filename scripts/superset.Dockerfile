FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV SUPERSET_SECRET_KEY=MyVeryStrongSecretKey
ENV FLASK_APP=superset

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libsasl2-dev \
    libldap2-dev \
    default-libmysqlclient-dev \
    curl \
    pkg-config \
    gcc \
    g++ \
    freetds-dev \
    freetds-bin \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir \
    apache_superset \
    psycopg2-binary \
    pymssql \
    sqlalchemy-trino \
    redis \
    celery \
    cachetools

WORKDIR /app

COPY superset_config.py /app/

ENV SUPERSET_CONFIG_PATH=/app/superset_config.py

CMD superset db upgrade && \
    superset fab create-admin \
      --username admin \
      --firstname Admin \
      --lastname User \
      --email admin@superset.com \
      --password admin || true && \
    superset init && \
    superset run -h 0.0.0.0 -p 8088