import os
import json
import joblib
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Spam Detection API")

MODEL_PATH = os.getenv("MODEL_PATH", "model.joblib")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))

try:
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
except Exception:
    cache = None

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
elif os.path.exists("spam_model.joblib"):
    model = joblib.load("spam_model.joblib")

class PredictRequest(BaseModel):
    text: str

@app.get("/healthz")
def healthz():
    if model is not None:
        return {"status": "ok", "version": "v1.0"}
    raise HTTPException(status_code=503, detail="Model file not loaded")

@app.post("/predict")
def predict(payload: PredictRequest):
    text = payload.text.strip()
    
    if cache:
        try:
            cached_res = cache.get(text)
            if cached_res:
                res = json.loads(cached_res)
                res["source"] = "cache_hit"
                return res
        except Exception:
            pass

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    prediction = model.predict([text])[0]
    response = {"label": str(prediction)}

    if cache:
        try:
            res_to_cache = dict(response)
            cache.setex(text, CACHE_TTL, json.dumps(res_to_cache))
        except Exception:
            pass

    response["source"] = "cache_miss"
    return response