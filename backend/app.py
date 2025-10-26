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

# CORS configuration for production and development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Allow all origins for development
        "https://drive-price-ai-main-lolxgl92z-abhinav07779s-projects.vercel.app",
        "https://drive-price-ai-main-32iq7ghdo-abhinav07779s-projects.vercel.app",
        "https://drive-price-ai-main-n157z8q8e-abhinav07779s-projects.vercel.app",
        "https://smart-car-value.onrender.com",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[float] = None
    kmDriven: Optional[float] = None
    fuelType: Optional[str] = None
    transmission: Optional[str] = None
    engineSize: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    cngKit: Optional[bool] = None
    qualityScore: Optional[float] = None
    # Extended optional fields to align with new training features
    variant_trim: Optional[str] = None
    generation_code: Optional[str] = None
    import_type: Optional[str] = None
    drivetrain: Optional[str] = None
    transmission_detail: Optional[str] = None
    body_type: Optional[str] = None
    seats: Optional[float] = None
    adas_level: Optional[str] = None
    airbags: Optional[float] = None
    air_suspension: Optional[str] = None
    sunroof: Optional[str] = None
    branded_audio: Optional[str] = None
    owners_count: Optional[float] = None
    insurance_months_left: Optional[float] = None
    warranty_months_left: Optional[float] = None
    tyre_life_pct: Optional[float] = None
    accident_history: Optional[str] = None
    flood_history: Optional[str] = None
    odometer_tamper: Optional[str] = None
    service_history_complete: Optional[str] = None
    recall_fixed: Optional[str] = None
    rto_code: Optional[str] = None
    ex_showroom_msrp: Optional[float] = None
    option_msrp_sum: Optional[float] = None

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

@app.get("/test-deps")
async def test_deps():
    try:
        import xgboost
        return {"xgboost": "available", "version": xgboost.__version__}
    except ImportError as e:
        return {"xgboost": "not available", "error": str(e)}


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
    "brand": ["brand", "make", "oem", "Make", "Brand"],
    "model": ["model", "Model"],
    "year": ["year", "modelYear", "Registration Year", "Year", "year_of_manufacture"],
    "kmDriven": ["kmDriven", "mileage", "km", "kms_driven", "Kms Driven", "kilometers_driven"],
    "fuelType": ["fuelType", "fuel_type", "Fuel Type", "ft", "fuel"],
    "transmission": ["transmission", "Transmission"],
    "engineSize": ["engineSize", "engine_size", "Engine Displacement", "engine", "Displacement"],
    # extended
    "variant_trim": ["variant_trim", "variant", "variantName", "Variant", "trim"],
    "generation_code": ["generation_code", "generation", "gen_code"],
    "import_type": ["import_type", "importType", "CBU_CKD", "cbu_ckd"],
    "drivetrain": ["drivetrain", "Drive Type", "drive_type", "AWD_RWD_FWD"],
    "transmission_detail": ["transmission_detail", "gearbox", "Transmission Detail"],
    "body_type": ["body_type", "Body Type", "body"],
    "seats": ["seats", "Seating Capacity"],
    "adas_level": ["adas_level", "ADAS", "adas"],
    "airbags": ["airbags", "Airbags"],
    "air_suspension": ["air_suspension", "Air Suspension"],
    "sunroof": ["sunroof", "Panoramic Sunroof", "Sunroof"],
    "branded_audio": ["branded_audio", "Audio Brand"],
    "owners_count": ["owners_count", "ownerNo", "Owners", "No. of Owners"],
    "insurance_months_left": ["insurance_months_left", "Insurance Months Left"],
    "warranty_months_left": ["warranty_months_left", "Warranty Months Left"],
    "tyre_life_pct": ["tyre_life_pct", "Tyre Life %"],
    "accident_history": ["accident_history", "Accident History"],
    "flood_history": ["flood_history", "Flood History"],
    "odometer_tamper": ["odometer_tamper", "Odometer Tamper"],
    "service_history_complete": ["service_history_complete", "Service History Complete"],
    "recall_fixed": ["recall_fixed", "Recall Fixed"],
    "rto_code": ["rto_code", "RTO", "Registration RTO"],
    "city": ["City", "city"],
    "state": ["state", "State"],
    "ex_showroom_msrp": ["ex_showroom_msrp", "Ex-Showroom Price"],
    "option_msrp_sum": ["option_msrp_sum", "Options Price"],
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
        pick_trained_name(trained_cols, ALIASES["brand"]): req.brand,
        pick_trained_name(trained_cols, ALIASES["model"]): req.model,
        pick_trained_name(trained_cols, ALIASES["year"]): coerce_numeric(req.year),
        pick_trained_name(trained_cols, ALIASES["kmDriven"]): coerce_numeric(req.kmDriven),
        pick_trained_name(trained_cols, ALIASES["fuelType"]): req.fuelType,
        pick_trained_name(trained_cols, ALIASES["transmission"]): req.transmission,
        pick_trained_name(trained_cols, ALIASES["engineSize"]): coerce_numeric(req.engineSize),
        # extended (will only be included if used in training)
        pick_trained_name(trained_cols, ALIASES["variant_trim"]): req.variant_trim,
        pick_trained_name(trained_cols, ALIASES["generation_code"]): req.generation_code,
        pick_trained_name(trained_cols, ALIASES["import_type"]): req.import_type,
        pick_trained_name(trained_cols, ALIASES["drivetrain"]): req.drivetrain,
        pick_trained_name(trained_cols, ALIASES["transmission_detail"]): req.transmission_detail,
        pick_trained_name(trained_cols, ALIASES["body_type"]): req.body_type,
        pick_trained_name(trained_cols, ALIASES["seats"]): coerce_numeric(req.seats),
        pick_trained_name(trained_cols, ALIASES["adas_level"]): req.adas_level,
        pick_trained_name(trained_cols, ALIASES["airbags"]): coerce_numeric(req.airbags),
        pick_trained_name(trained_cols, ALIASES["air_suspension"]): req.air_suspension,
        pick_trained_name(trained_cols, ALIASES["sunroof"]): req.sunroof,
        pick_trained_name(trained_cols, ALIASES["branded_audio"]): req.branded_audio,
        pick_trained_name(trained_cols, ALIASES["owners_count"]): coerce_numeric(req.owners_count),
        pick_trained_name(trained_cols, ALIASES["insurance_months_left"]): coerce_numeric(req.insurance_months_left),
        pick_trained_name(trained_cols, ALIASES["warranty_months_left"]): coerce_numeric(req.warranty_months_left),
        pick_trained_name(trained_cols, ALIASES["tyre_life_pct"]): coerce_numeric(req.tyre_life_pct),
        pick_trained_name(trained_cols, ALIASES["accident_history"]): req.accident_history,
        pick_trained_name(trained_cols, ALIASES["flood_history"]): req.flood_history,
        pick_trained_name(trained_cols, ALIASES["odometer_tamper"]): req.odometer_tamper,
        pick_trained_name(trained_cols, ALIASES["service_history_complete"]): req.service_history_complete,
        pick_trained_name(trained_cols, ALIASES["recall_fixed"]): req.recall_fixed,
        pick_trained_name(trained_cols, ALIASES["rto_code"]): req.rto_code,
        pick_trained_name(trained_cols, ALIASES["city"]): req.city,
        pick_trained_name(trained_cols, ALIASES["state"]): req.state,
        pick_trained_name(trained_cols, ALIASES["ex_showroom_msrp"]): coerce_numeric(req.ex_showroom_msrp),
        pick_trained_name(trained_cols, ALIASES["option_msrp_sum"]): coerce_numeric(req.option_msrp_sum),
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

    # Get model metrics from info
    model_metrics = info.get("metrics", [])
    best_model_metrics = None
    for metric in model_metrics:
        if metric.get("model") == info.get("best_model"):
            best_model_metrics = metric
            break
    
    rmse = best_model_metrics.get("rmse") if best_model_metrics else None
    r2_score = best_model_metrics.get("r2") if best_model_metrics else None
    confidence = min(95.0, max(70.0, (r2_score * 100) if r2_score else 85.0))

    return PredictResponse(
        predictedPrice=round(yhat, 2),
        confidence=round(confidence, 1),
        rmse=round(rmse, 2) if rmse else None,
        r2Score=round(r2_score, 4) if r2_score else None,
    )

