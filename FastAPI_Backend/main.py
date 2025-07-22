
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Incident Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← OR restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
anomaly_model = joblib.load("ml-models/isolation_forest_model.pkl")
log_model = joblib.load("ml-models/log_classifier.pkl")
tfidf = joblib.load("ml-models/tfidf_vectorizer.pkl")

class MetricInput(BaseModel):
    cpu: float
    memory: float
    disk: float

class LogInput(BaseModel):
    log: str

@app.post("/predict/anomaly")
def predict_anomaly(data: MetricInput):
    features = np.array([[data.cpu, data.memory, data.disk]])
    pred = anomaly_model.predict(features)[0]
    return {
        "input": data.dict(),
        "prediction": int(pred),
        "anomaly": bool(pred == -1)
    }

@app.post("/predict/log")
def predict_log(data: LogInput):
    vec = tfidf.transform([data.log])
    pred = log_model.predict(vec)[0]
    return {
        "log": data.log,
        "prediction": pred
    }