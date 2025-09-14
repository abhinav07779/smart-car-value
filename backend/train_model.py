import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json
from datetime import datetime

def load_and_prepare_data():
    """Load and prepare the car dataset for training"""
    # Load the dataset (try both current and parent directory)
    import os
    if os.path.exists("car_price_dataset.csv"):
        df = pd.read_csv("car_price_dataset.csv")
    elif os.path.exists("../car_price_dataset.csv"):
        df = pd.read_csv("../car_price_dataset.csv")
    else:
        raise FileNotFoundError("car_price_dataset.csv not found in current or parent directory")
    
    print(f"Dataset loaded: {len(df)} records")
    print(f"Features: {list(df.columns)}")
    
    # Create additional features for better predictions
    df['age'] = 2024 - df['year']
    df['km_per_year'] = df['kmDriven'] / (df['age'] + 1)  # Avoid division by zero
    
    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['brand', 'model', 'fuelType', 'transmission', 'city', 'state']
    
    for col in categorical_columns:
        le = LabelEncoder()
        df[f'{col}_encoded'] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Create feature matrix
    feature_columns = [
        'year', 'kmDriven', 'engineSize', 'cngKit', 'qualityScore', 
        'age', 'km_per_year'
    ] + [f'{col}_encoded' for col in categorical_columns]
    
    X = df[feature_columns]
    y = df['price']
    
    return X, y, label_encoders, feature_columns

def train_model():
    """Train the Random Forest model"""
    print("Loading and preparing data...")
    X, y, label_encoders, feature_columns = load_and_prepare_data()
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train Random Forest model
    print("Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"RMSE: ₹{rmse:,.2f}")
    print(f"R² Score: {r2:.4f}")
    print(f"Mean Absolute Error: ₹{np.mean(np.abs(y_test - y_pred)):,.2f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nTop 10 Most Important Features:")
    print(feature_importance.head(10))
    
    # Save model and encoders
    print("\nSaving model and encoders...")
    joblib.dump(model, 'car_price_model.pkl')
    
    # Save encoders and feature info
    model_info = {
        'label_encoders': {k: v.classes_.tolist() for k, v in label_encoders.items()},
        'feature_columns': feature_columns,
        'categorical_columns': ['brand', 'model', 'fuelType', 'transmission', 'city', 'state'],
        'numerical_columns': ['year', 'kmDriven', 'engineSize', 'cngKit', 'qualityScore'],
        'model_metrics': {
            'rmse': float(rmse),
            'r2_score': float(r2),
            'mae': float(np.mean(np.abs(y_test - y_pred)))
        },
        'training_date': datetime.now().isoformat()
    }
    
    with open('model_info.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print("Model training completed successfully!")
    return model, label_encoders, feature_columns

if __name__ == "__main__":
    train_model()
