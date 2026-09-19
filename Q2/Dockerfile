# Stage 1: Builder (Installs dependencies & trains model)
FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Use a virtual environment to bundle dependencies cleanly
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Run dataset generation and model training inside the builder stage
COPY dataset_generator.py train.py ./
RUN python dataset_generator.py && python train.py

# Stage 2: Final Runtime Image
FROM python:3.10-slim AS runner

WORKDIR /app

# Copy virtual environment and model artifact generated in stage 1
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/spam_model.joblib ./model.joblib
COPY --from=builder /app/spam_model.joblib ./spam_model.joblib
COPY app.py ./

ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]