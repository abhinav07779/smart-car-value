import os
import json
import joblib
import argparse
import numpy as np
import pandas as pd
from typing import Tuple, List

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

try:
    from xgboost import XGBRegressor  # type: ignore
    HAS_XGB = True
except Exception:
    HAS_XGB = False

DEFAULT_TARGET = "price"

# Columns mapping for provided CarDekho-like dataset
COLUMN_ALIASES = {
    # target
    "price": ["price", "selling_price", "Price"],
    # brand/make
    "make": ["make", "brand", "oem", "Make", "Brand"],
    # model
    "model": ["model", "Model"],
    # year
    "year": ["year", "modelYear", "Registration Year", "Year", "year_of_manufacture"],
    # mileage / km driven
    "mileage": ["mileage", "km", "kms_driven", "Kms Driven", "kilometers_driven"],
    # fuel
    "fuel_type": ["fuel_type", "Fuel Type", "ft", "fuel"],
    # transmission
    "transmission": ["transmission", "Transmission"],
    # engine size
    "engine_size": ["engine_size", "Engine Displacement", "engine", "Displacement"],
    # extended categorical features (if present)
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
    "option_msrp_sum": ["option_msrp_sum", "Options Price"]
}


def find_first_existing(df: pd.DataFrame, candidates: List[str]) -> str:
    for name in candidates:
        if name in df.columns:
            return name
    return ""


def detect_schema(df: pd.DataFrame) -> Tuple[dict, List[str], List[str]]:
    schema = {}
    numeric_candidates: List[str] = []
    categorical_candidates: List[str] = []

    for key, aliases in COLUMN_ALIASES.items():
        col = find_first_existing(df, aliases)
        if col:
            schema[key] = col

    # Fallback heuristics
    if "price" not in schema:
        raise ValueError("Target column 'price' not found. Please provide a CSV with a price column or update mapping.")

    # Prepare feature lists
    if "make" in schema:
        categorical_candidates.append(schema["make"])
    if "model" in schema:
        categorical_candidates.append(schema["model"])
    if "fuel_type" in schema:
        categorical_candidates.append(schema["fuel_type"])
    if "transmission" in schema:
        categorical_candidates.append(schema["transmission"])
    # Optional extended categoricals
    for key in [
        "variant_trim","generation_code","import_type","drivetrain","transmission_detail",
        "body_type","adas_level","air_suspension","sunroof","branded_audio","rto_code",
        "city","state"
    ]:
        if key in COLUMN_ALIASES:
            col = find_first_existing(df, COLUMN_ALIASES[key])
            if col:
                schema[key] = col
                categorical_candidates.append(col)

    if "year" in schema:
        numeric_candidates.append(schema["year"])
    if "mileage" in schema:
        numeric_candidates.append(schema["mileage"])
    if "engine_size" in schema:
        numeric_candidates.append(schema["engine_size"])
    # Optional extended numerics
    for key in [
        "seats","airbags","owners_count","insurance_months_left","warranty_months_left",
        "tyre_life_pct","ex_showroom_msrp","option_msrp_sum"
    ]:
        if key in COLUMN_ALIASES:
            col = find_first_existing(df, COLUMN_ALIASES[key])
            if col:
                schema[key] = col
                numeric_candidates.append(col)

    # Keep only columns present in df
    numeric_features = [c for c in numeric_candidates if c in df.columns]
    categorical_features = [c for c in categorical_candidates if c in df.columns]

    return schema, numeric_features, categorical_features


def load_known_categories() -> Tuple[List[str], List[str]]:
    """Load known brands and models from public/year_brand_model_mapping.json if available.
    Models in that file include brand prefixes; we strip them when possible.
    """
    candidates = [
        os.path.join(os.getcwd(), "public", "year_brand_model_mapping.json"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "public", "year_brand_model_mapping.json"),
    ]
    brands: set[str] = set()
    models: set[str] = set()
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for _year, brand_map in data.items():
                    if isinstance(brand_map, dict):
                        for brand_name, models_list in brand_map.items():
                            brands.add(brand_name)
                            if isinstance(models_list, list):
                                for m in models_list:
                                    if isinstance(m, str):
                                        # Remove leading brand prefix if present
                                        prefix = f"{brand_name} "
                                        models.add(m[len(prefix):] if m.startswith(prefix) else m)
            except Exception:
                continue
    return sorted(brands), sorted(models)


def build_preprocessor(numeric_features: List[str], categorical_features: List[str]) -> ColumnTransformer:
    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    # Prepare stable categories for brand/model to align with frontend dropdowns
    known_brands, known_models = load_known_categories()
    categories_per_feature: List[List[str] | None] = []
    for col in categorical_features:
        lc = col.lower()
        if lc in ("make", "brand", "oem") and known_brands:
            categories_per_feature.append(known_brands)
        elif lc == "model" and known_models:
            categories_per_feature.append(known_models)
        else:
            categories_per_feature.append(None)

    # Use explicit categories only if every categorical feature has a category list
    use_explicit = len(categories_per_feature) > 0 and all(c is not None for c in categories_per_feature)
    onehot = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
        categories=categories_per_feature if use_explicit else "auto",
    )

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", onehot),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )
    return preprocessor


def evaluate_model(name: str, y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    return {"model": name, "rmse": rmse, "mae": mae, "r2": r2}


def train_models(X_train, y_train):
    models = []

    models.append(("LinearRegression", LinearRegression()))
    models.append(("RandomForest", RandomForestRegressor(n_estimators=300, random_state=42)))
    if HAS_XGB:
        models.append(("XGBRegressor", XGBRegressor(
            n_estimators=600,
            learning_rate=0.05,
            max_depth=8,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            tree_method="hist",
        )))

    fitted = []
    for name, model in models:
        model.fit(X_train, y_train)
        fitted.append((name, model))
    return fitted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str, required=True, help="Path to dataset CSV")
    parser.add_argument("--target", type=str, default=DEFAULT_TARGET, help="Target column name (default: price)")
    parser.add_argument("--out", type=str, default="backend/models", help="Output directory for model artifacts")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    df = pd.read_csv(args.csv)

    # Coerce numerics where possible (mileage/engine might be strings like '998 cc' or '32,706 Kms')
    def coerce_numeric(series: pd.Series) -> pd.Series:
        if series.dtype == object:
            ser = series.astype(str)
            ser = ser.str.replace(",", "", regex=False)
            ser = ser.str.extract(r"([0-9]+\.?[0-9]*)")[0]
            return pd.to_numeric(ser, errors="coerce")
        return pd.to_numeric(series, errors="coerce")

    schema, numeric_features, categorical_features = detect_schema(df)

    # Rename target to 'price' for consistency
    target_col = schema.get("price", args.target)

    # Clean numerics
    for col in numeric_features + [c for c in [target_col] if c]:
        if col in df.columns:
            df[col] = coerce_numeric(df[col])

    # Basic sanity: drop rows without target
    df = df.dropna(subset=[target_col])

    features = numeric_features + categorical_features
    X = df[features].copy()

    # Drop all-empty columns to avoid imputer warnings and noisy features
    empty_cols = [c for c in X.columns if X[c].isna().all()]
    if empty_cols:
        X = X.drop(columns=empty_cols)
        numeric_features = [c for c in numeric_features if c not in empty_cols]
        categorical_features = [c for c in categorical_features if c not in empty_cols]
    y = df[target_col].astype(float).values

    preprocessor = build_preprocessor(numeric_features, categorical_features)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit preprocessor
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    # Train candidates
    candidates = train_models(X_train_processed, y_train)

    # Evaluate
    results = []
    best = None
    best_rmse = float("inf")
    for name, model in candidates:
        y_pred = model.predict(X_test_processed)
        metrics = evaluate_model(name, y_test, y_pred)
        results.append(metrics)
        if metrics["rmse"] < best_rmse:
            best_rmse = metrics["rmse"]
            best = (name, model)

    assert best is not None
    best_name, best_model = best

    # Save artifacts
    joblib.dump(preprocessor, os.path.join(args.out, "preprocessor.joblib"))
    joblib.dump(best_model, os.path.join(args.out, "model.joblib"))

    from datetime import datetime
    info = {
        "best_model": best_name,
        "metrics": results,
        "model_metrics": results,
        "features": {
            "numeric": numeric_features,
            "categorical": categorical_features,
        },
        "training_date": datetime.utcnow().isoformat(),
    }
    with open(os.path.join(args.out, "model_info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)

    print(json.dumps({"status": "ok", **info}, indent=2))


if __name__ == "__main__":
    main()



