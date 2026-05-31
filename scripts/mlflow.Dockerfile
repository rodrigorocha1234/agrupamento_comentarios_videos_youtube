FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    mlflow \
    psycopg2-binary \
    boto3

WORKDIR /mlflow

EXPOSE 5000

CMD sh -c "mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri ${MLFLOW_BACKEND_STORE_URI} \
  --artifacts-destination ${MLFLOW_ARTIFACTS_DESTINATION} \
  --serve-artifacts"