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

    if "year" in schema:
        numeric_candidates.append(schema["year"])
    if "mileage" in schema:
        numeric_candidates.append(schema["mileage"])
    if "engine_size" in schema:
        numeric_candidates.append(schema["engine_size"])

    # Keep only columns present in df
    numeric_features = [c for c in numeric_candidates if c in df.columns]
    categorical_features = [c for c in categorical_candidates if c in df.columns]

    return schema, numeric_features, categorical_features


def build_preprocessor(numeric_features: List[str], categorical_features: List[str]) -> ColumnTransformer:
    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
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

    info = {
        "best_model": best_name,
        "metrics": results,
        "features": {
            "numeric": numeric_features,
            "categorical": categorical_features,
        }
    }
    with open(os.path.join(args.out, "model_info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)

    print(json.dumps({"status": "ok", **info}, indent=2))


if __name__ == "__main__":
    main()



