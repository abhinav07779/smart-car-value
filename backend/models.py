"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class CarData(BaseModel):
    """Input model for car price prediction"""
    brand: str = Field(..., description="Car brand (e.g., 'Maruti Suzuki', 'Hyundai')")
    model: str = Field(..., description="Car model (e.g., 'Swift', 'Creta')")
    year: int = Field(..., ge=1990, le=2024, description="Manufacturing year")
    kmDriven: int = Field(..., ge=0, description="Kilometers driven")
    fuelType: str = Field(..., description="Fuel type: 'Petrol', 'Diesel', or 'Electric'")
    transmission: str = Field(..., description="Transmission type: 'Manual' or 'Automatic'")
    engineSize: float = Field(..., gt=0, description="Engine size in liters")
    city: str = Field(..., description="City where car is located")
    state: str = Field(..., description="State where car is located")
    cngKit: bool = Field(..., description="Whether car has CNG kit installed")
    qualityScore: float = Field(..., ge=0, le=10, description="Quality score from 0-10")


class PredictionResponse(BaseModel):
    """Response model for car price prediction"""
    predictedPrice: float = Field(..., description="Predicted car price in INR")
    confidence: float = Field(..., ge=0, le=100, description="Prediction confidence percentage")
    rmse: float = Field(..., description="Root Mean Square Error of the model")
    r2Score: float = Field(..., description="R² score of the model")
    modelInfo: Dict[str, Any] = Field(..., description="Additional model information")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")


class ModelInfoResponse(BaseModel):
    """Model information response"""
    model_metrics: Dict[str, float] = Field(..., description="Model performance metrics")
    training_date: str = Field(..., description="When the model was trained")
    features_count: int = Field(..., description="Number of features used")
    categorical_features: list = Field(..., description="List of categorical features")
    numerical_features: list = Field(..., description="List of numerical features")


class BrandsResponse(BaseModel):
    """Available brands and options response"""
    brands: list = Field(..., description="Available car brands")
    models: list = Field(..., description="Available car models")
    fuel_types: list = Field(..., description="Available fuel types")
    transmissions: list = Field(..., description="Available transmission types")
    cities: list = Field(..., description="Available cities")
    states: list = Field(..., description="Available states")
