"""
Configuration settings for the Car Price Prediction API
"""

import os
from typing import List

# API Configuration
API_TITLE = "Car Price Prediction API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Machine Learning API for predicting car prices based on various features"

# Server Configuration
HOST = "0.0.0.0"
PORT = 8002
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# CORS Configuration
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:8080",  # Vite configured port
    "http://127.0.0.1:8080",  # Vite configured port
    "http://localhost:8081", 
    "http://127.0.0.1:8081",
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173"
]

# Model Configuration
MODEL_PATH = "car_price_model.pkl"
MODEL_INFO_PATH = "model_info.json"

# File paths
DATASET_PATH = "../car_price_dataset.csv"
