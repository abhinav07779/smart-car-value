import os
import re
import json
import glob
import pandas as pd
from typing import Dict, List, Optional


ROOT = os.path.dirname(os.path.dirname(__file__))
CAR_DS_DIR = os.path.join(ROOT, "car dataset")
CAR_XLSX_DIR = os.path.join(CAR_DS_DIR, "Car_Dataset")
OUTPUT_CSV = os.path.join(CAR_DS_DIR, "car_dekho_extended.csv")


ALIASES: Dict[str, List[str]] = {
    "price": ["price", "selling_price", "Price"],
    "brand": ["brand", "make", "oem", "Make", "Brand"],
    "model": ["model", "Model"],
    "year": ["modelYear", "Registration Year", "Year", "year", "year_of_manufacture"],
    "mileage": ["mileage", "km", "kms_driven", "Kms Driven", "kilometers_driven"],
    "fuel_type": ["fuel_type", "Fuel Type", "ft", "fuel"],
    "transmission": ["transmission", "Transmission"],
    "engine_size": ["engine_size", "Engine Displacement", "engine", "Displacement"],
    "variant_trim": ["variant_trim", "variant", "variantName", "Variant", "trim"],
    "owners_count": ["owners_count", "ownerNo", "Owners", "No. of Owners"],
    "city": ["City", "city"],
    "state": ["State", "state"],
    "rto_code": ["RTO", "rto_code", "Registration RTO"],
}


EXTENDED_COLUMNS = [
    "price","make","model","year","mileage","engine_size","fuel_type","transmission",
    "transmission_detail","drivetrain","body_type","seats","airbags","variant_trim",
    "generation_code","import_type","adas_level","air_suspension","sunroof","branded_audio",
    "owners_count","insurance_months_left","warranty_months_left","tyre_life_pct",
    "accident_history","flood_history","odometer_tamper","service_history_complete","recall_fixed",
    "ex_showroom_msrp","option_msrp_sum","rto_code","city","state",
]


def first_col(df: pd.DataFrame, names: List[str]) -> Optional[str]:
    for n in names:
        if n in df.columns:
            return n
    return None


def parse_numeric(val) -> Optional[float]:
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).replace(",", "")
    m = re.search(r"([0-9]+\.?[0-9]*)", s)
    return float(m.group(1)) if m else None


def infer_drivetrain(brand: str, model: str, variant: str) -> Optional[str]:
    text = " ".join([str(brand or ""), str(model or ""), str(variant or "")]).lower()
    if any(k in text for k in ["quattro", "awd", "4wd", "4x4", "xdrive", "4matic", "4matic+"]):
        return "AWD"
    if any(k in text for k in ["rwd", "rear-wheel"]):
        return "RWD"
    if any(k in text for k in ["fwd", "front-wheel"]):
        return "FWD"
    # BMW 1/3/5 sedans default RWD, most India-spec crossovers FWD; leave None to avoid wrong labels
    return None


CBU_MODELS = {"911", "AMG GT", "Mustang", "Z4", "i8"}


def infer_import_type(brand: str, model: str) -> Optional[str]:
    if brand is None or model is None:
        return None
    b = str(brand).strip()
    m = str(model).strip()
    if not b or not m:
        return None
    if m.upper() in {x.upper() for x in CBU_MODELS}:
        return "CBU"
    if b in {"Mercedes-Benz", "Mercedes", "BMW", "Audi"}:
        return "CKD"
    return None


def infer_adas(brand: str, model: str, variant: str) -> Optional[str]:
    txt = " ".join([str(brand or ""), str(model or ""), str(variant or "")]).lower()
    if "xuv700" in txt and any(k in txt for k in ["ax7", "ax7l", "adas"]):
        return "L1"
    return None


def normalize_brand(brand: str) -> str:
    if not isinstance(brand, str):
        return brand
    b = brand.strip()
    return {"Merc": "Mercedes-Benz", "Mercedes": "Mercedes-Benz"}.get(b, b)


def load_frontend_mapping() -> Dict[str, List[str]]:
    candidates = [
        os.path.join(ROOT, "public", "year_brand_model_mapping.json"),
        os.path.join(ROOT, "dist", "year_brand_model_mapping.json"),
        os.path.join(ROOT, "year_brand_model_mapping.json"),
    ]
    mapping: Dict[str, List[str]] = {}
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for _year, brands in data.items():
                    if isinstance(brands, dict):
                        for brand_name, models_list in brands.items():
                            mapping.setdefault(brand_name, [])
                            if isinstance(models_list, list):
                                for m in models_list:
                                    if isinstance(m, str):
                                        mapping[brand_name].append(m)
            except Exception:
                continue
    return mapping


def coerce_row(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(columns=EXTENDED_COLUMNS)
    # Map basics
    brand_col = first_col(df, ALIASES["brand"]) or ""
    model_col = first_col(df, ALIASES["model"]) or ""
    year_col = first_col(df, ALIASES["year"]) or ""
    price_col = first_col(df, ALIASES["price"]) or ""
    km_col = first_col(df, ALIASES["mileage"]) or ""
    eng_col = first_col(df, ALIASES["engine_size"]) or ""
    fuel_col = first_col(df, ALIASES["fuel_type"]) or ""
    trans_col = first_col(df, ALIASES["transmission"]) or ""
    variant_col = first_col(df, ALIASES["variant_trim"]) or ""
    owners_col = first_col(df, ALIASES["owners_count"]) or ""
    city_col = first_col(df, ALIASES["city"]) or ""
    state_col = first_col(df, ALIASES["state"]) or ""
    rto_col = first_col(df, ALIASES["rto_code"]) or ""

    def owners_to_num(x) -> Optional[float]:
        if pd.isna(x):
            return None
        if isinstance(x, (int, float)):
            return float(x)
        s = str(x).lower()
        m = re.search(r"([0-9]+)", s)
        return float(m.group(1)) if m else None

    out["make"] = df[brand_col].apply(normalize_brand) if brand_col else None
    out["model"] = df[model_col] if model_col else None
    out["year"] = df[year_col].apply(parse_numeric) if year_col else None
    out["price"] = df[price_col].apply(parse_numeric) if price_col else None
    out["mileage"] = df[km_col].apply(parse_numeric) if km_col else None
    out["engine_size"] = df[eng_col].apply(parse_numeric) if eng_col else None
    out["fuel_type"] = df[fuel_col] if fuel_col else None
    out["transmission"] = df[trans_col] if trans_col else None
    out["variant_trim"] = df[variant_col] if variant_col else None
    out["owners_count"] = df[owners_col].apply(owners_to_num) if owners_col else None
    out["city"] = df[city_col] if city_col else None
    out["state"] = df[state_col] if state_col else None
    out["rto_code"] = df[rto_col] if rto_col else None

    # Heuristics
    out["drivetrain"] = [
        infer_drivetrain(b, m, v) for b, m, v in zip(out.get("make", []), out.get("model", []), out.get("variant_trim", []))
    ]
    out["import_type"] = [infer_import_type(b, m) for b, m in zip(out.get("make", []), out.get("model", []))]
    out["adas_level"] = [infer_adas(b, m, v) for b, m, v in zip(out.get("make", []), out.get("model", []), out.get("variant_trim", []))]

    return out


def read_sources() -> List[pd.DataFrame]:
    dfs: List[pd.DataFrame] = []
    # Cleaned CSVs
    for base in ["car_dekho_cleaned_dataset.csv", "car_dekho_Structured.csv"]:
        p = os.path.join(CAR_DS_DIR, base)
        if os.path.exists(p):
            try:
                dfs.append(pd.read_csv(p))
            except Exception:
                pass
    # XLSX per city
    for xlsx in glob.glob(os.path.join(CAR_XLSX_DIR, "*.xlsx")):
        try:
            df = pd.read_excel(xlsx)
            # Inject city from filename if not present
            city = os.path.splitext(os.path.basename(xlsx))[0].replace("_cars", "").replace(".xlsx", "")
            if "City" not in df.columns and "city" not in df.columns:
                df["City"] = city.capitalize()
            dfs.append(df)
        except Exception:
            continue
    return dfs


def main():
    os.makedirs(CAR_DS_DIR, exist_ok=True)
    _ = load_frontend_mapping()  # currently not used directly; reserved for future normalization

    sources = read_sources()
    if not sources:
        raise SystemExit("No input datasets found under 'car dataset/'.")

    extended_frames: List[pd.DataFrame] = []
    for src in sources:
        coerced = coerce_row(src)
        extended_frames.append(coerced)

    combined = pd.concat(extended_frames, ignore_index=True, sort=False)

    # Keep only declared columns in stable order
    for col in EXTENDED_COLUMNS:
        if col not in combined.columns:
            combined[col] = None
    combined = combined[EXTENDED_COLUMNS]

    # Drop rows without price or brand/model/year
    combined = combined.dropna(subset=["price"], how="all")
    # Basic cleanup
    combined["make"] = combined["make"].fillna("").replace("", pd.NA)
    combined["model"] = combined["model"].fillna("").replace("", pd.NA)
    combined["year"] = pd.to_numeric(combined["year"], errors="coerce")
    combined["mileage"] = pd.to_numeric(combined["mileage"], errors="coerce")
    combined["engine_size"] = pd.to_numeric(combined["engine_size"], errors="coerce")

    combined.to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote extended dataset: {OUTPUT_CSV} ({len(combined)} rows)")


if __name__ == "__main__":
    main()


