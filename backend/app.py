from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
import joblib
import pandas as pd
from typing import Optional, Dict, List
from fastapi.middleware.cors import CORSMiddleware

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "preprocessor.joblib")
MODEL_PATH = os.path.join(MODELS_DIR, "model.joblib")
INFO_PATH = os.path.join(MODELS_DIR, "model_info.json")

app = FastAPI(title="Car Price Prediction API")

# CORS for development: allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[float] = None
    mileage: Optional[float] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    engine_size: Optional[float] = None

class PredictResponse(BaseModel):
    predictedPrice: float
    confidence: float
    rmse: Optional[float] = None
    r2Score: Optional[float] = None


@app.get("/")
async def root():
    return {"message": "Car Price Prediction API", "status": "running", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}


def load_artifacts():
    if not (os.path.exists(PREPROCESSOR_PATH) and os.path.exists(MODEL_PATH) and os.path.exists(INFO_PATH)):
        raise RuntimeError("Model artifacts not found. Train the model first.")
    pre = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)
    with open(INFO_PATH, "r", encoding="utf-8") as f:
        info = json.load(f)
    return pre, model, info


@app.get("/model-info")
async def model_info():
    try:
        if not os.path.exists(INFO_PATH):
            raise FileNotFoundError("model_info.json not found")
        with open(INFO_PATH, "r", encoding="utf-8") as f:
            info = json.load(f)
        response = {
            "model_metrics": info.get("model_metrics") or info.get("metrics") or {},
            "training_date": info.get("training_date") or info.get("trained_at") or "",
            "features_count": len(info.get("feature_columns") or info.get("features", {}).get("all", [])),
            "categorical_features": info.get("categorical_columns") or info.get("features", {}).get("categorical", []),
            "numerical_features": info.get("numerical_columns") or info.get("features", {}).get("numeric", []),
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


ALIASES: Dict[str, List[str]] = {
    "make": ["make", "brand", "oem", "Make", "Brand"],
    "model": ["model", "Model"],
    "year": ["year", "modelYear", "Registration Year", "Year", "year_of_manufacture"],
    "mileage": ["mileage", "km", "kms_driven", "Kms Driven", "kilometers_driven"],
    "fuel_type": ["fuel_type", "Fuel Type", "ft", "fuel"],
    "transmission": ["transmission", "Transmission"],
    "engine_size": ["engine_size", "Engine Displacement", "engine", "Displacement"],
}


def pick_trained_name(trained_cols: List[str], aliases: List[str]) -> Optional[str]:
    for alias in aliases:
        if alias in trained_cols:
            return alias
    return None


def coerce_numeric(value: Optional[float | int | str]) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value)
    s = s.replace(",", "")
    import re
    m = re.search(r"([0-9]+\.?[0-9]*)", s)
    if not m:
        return None
    try:
        return float(m.group(1))
    except Exception:
        return None


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    try:
        pre, model, info = load_artifacts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    trained_numeric = info.get("features", {}).get("numeric", [])
    trained_categorical = info.get("features", {}).get("categorical", [])
    trained_cols = list(trained_numeric) + list(trained_categorical)

    mapping = {
        pick_trained_name(trained_cols, ALIASES["make"]): req.make,
        pick_trained_name(trained_cols, ALIASES["model"]): req.model,
        pick_trained_name(trained_cols, ALIASES["year"]): coerce_numeric(req.year),
        pick_trained_name(trained_cols, ALIASES["mileage"]): coerce_numeric(req.mileage),
        pick_trained_name(trained_cols, ALIASES["fuel_type"]): req.fuel_type,
        pick_trained_name(trained_cols, ALIASES["transmission"]): req.transmission,
        pick_trained_name(trained_cols, ALIASES["engine_size"]): coerce_numeric(req.engine_size),
    }

    # Remove None keys (aliases not used in training)
    row = {k: v for k, v in mapping.items() if k is not None}

    if not row:
        raise HTTPException(status_code=400, detail="No matching features for trained model. Re-train or adjust input.")

    X = pd.DataFrame([row])

    try:
        Xp = pre.transform(X)
        yhat = float(model.predict(Xp)[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return PredictResponse(
        predictedPrice=round(yhat, 2),
        confidence=85.0,
        rmse=None,
        r2Score=None,
    )

