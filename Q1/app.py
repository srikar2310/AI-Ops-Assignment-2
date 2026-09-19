from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

app = FastAPI()

model = None

@app.on_event("startup")
def load_model():
    global model
    model_path = os.getenv("MODEL_PATH", "spam_model.joblib")
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        raise RuntimeError(f"Model artifact not found at {model_path}")

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    prediction = model.predict([request.text])[0]
    return {"label": str(prediction)}

@app.get("/healthz")
def healthz():
    if model is not None:
        return {"status": "ok"}
    raise HTTPException(status_code=503, detail="Model uninitialized")