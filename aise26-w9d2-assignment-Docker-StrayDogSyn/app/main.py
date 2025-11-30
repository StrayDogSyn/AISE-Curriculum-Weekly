from fastapi import FastAPI, Response
from pydantic import BaseModel
import time
import os
import joblib
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from app.metrics import request_counter, request_latency
from models.train import ensure_model

MODEL_PATH = os.path.join("models", "baseline.joblib")
MODEL_VERSION = "v1.0"

class PredictInput(BaseModel):
    x1: float
    x2: float

class PredictOutput(BaseModel):
    score: float
    model_version: str

app = FastAPI()

model = None

@app.on_event("startup")
def startup_event():
    global model
    model = ensure_model(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictOutput)
def predict(payload: PredictInput):
    start = time.perf_counter()
    status = "200"
    try:
        score = float(model.predict_proba([[payload.x1, payload.x2]])[0][1])
        return {"score": score, "model_version": MODEL_VERSION}
    except Exception:
        status = "500"
        raise
    finally:
        request_counter.labels(endpoint="/predict", method="POST", status=status).inc()
        request_latency.labels(endpoint="/predict", method="POST").observe(time.perf_counter() - start)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)