#!/usr/bin/env python3
"""
Script to train the car price prediction model
Run this before starting the API server
"""

import os
import sys
from train_model import train_model

def main():
    print("🚗 Starting Car Price Prediction Model Training...")
    print("=" * 50)
    
    # Check if dataset exists (try both current and parent directory)
    dataset_path = None
    if os.path.exists("car_price_dataset.csv"):
        dataset_path = "car_price_dataset.csv"
    elif os.path.exists("../car_price_dataset.csv"):
        dataset_path = "../car_price_dataset.csv"
    else:
        print("❌ Error: car_price_dataset.csv not found!")
        print("Please ensure the dataset is in the current or parent directory.")
        sys.exit(1)
    
    try:
        # Train the model
        model, encoders, features = train_model()
        
        print("\n✅ Model training completed successfully!")
        print("📁 Files created:")
        print("   - car_price_model.pkl (trained model)")
        print("   - model_info.json (model metadata)")
        print("\n🚀 You can now start the API server with:")
        print("   python app.py")
        print("   or")
        print("   uvicorn app:app --reload")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
