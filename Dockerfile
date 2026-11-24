FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements-service.txt tracks/fraud/requirements.txt ./
RUN mkdir -p tracks/fraud && mv requirements.txt tracks/fraud/requirements.txt && pip install --no-cache-dir -r requirements-service.txt
COPY scripts ./scripts
RUN mkdir -p tracks/fraud/data tracks/fraud/artifacts && python -c "import urllib.request; urllib.request.urlretrieve('https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv', 'tracks/fraud/data/creditcard.csv')" && OMP_NUM_THREADS=1 python scripts/train.py

FROM python:3.11-slim
WORKDIR /app
COPY requirements-service.txt tracks/fraud/requirements.txt ./
RUN mkdir -p tracks/fraud && mv requirements.txt tracks/fraud/requirements.txt && pip install --no-cache-dir -r requirements-service.txt && useradd --create-home raqib
COPY raqib ./raqib
COPY --from=builder /app/tracks/fraud/artifacts ./tracks/fraud/artifacts
USER raqib
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/ready', timeout=3)" || exit 1
CMD ["uvicorn", "raqib.api:app", "--host", "0.0.0.0", "--port", "8000"]
