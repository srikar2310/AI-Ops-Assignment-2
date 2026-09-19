import os
import joblib
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Spam Detection API with Redis Caching")

MODEL_PATH = os.getenv("MODEL_PATH", "model.joblib")
REDIS_HOST = os.getenv("REDIS_HOST", "cache")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_TTL = 3600  # TTL of 1 hour (3600 seconds)

model = None
redis_client = None

@app.on_event("startup")
def load_resources():
    global model, redis_client
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        raise RuntimeError(f"Model file not found at {MODEL_PATH}")

    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True
    )

class PredictRequest(BaseModel):
    text: str

@app.get("/healthz")
def healthz():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return {"status": "ok"}

@app.post("/predict")
def predict(request: PredictRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # 1. Check Redis Cache
    try:
        cached_label = redis_client.get(text)
        if cached_label:
            return {"label": cached_label, "source": "cache_hit"}
    except redis.RedisError as e:
        # Fallback in case Redis is temporarily unreachable
        pass

    # 2. Compute prediction on cache MISS
    prediction = model.predict([text])[0]

    # 3. Store prediction in Redis with TTL
    try:
        redis_client.setex(text, CACHE_TTL, prediction)
    except redis.RedisError:
        pass

    return {"label": prediction, "source": "cache_miss"}