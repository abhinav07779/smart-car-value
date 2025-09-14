"""
Car Price Prediction API - Main Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import API_TITLE, API_VERSION, API_DESCRIPTION, HOST, PORT, ALLOWED_ORIGINS
from .models import (
    CarData, 
    PredictionResponse, 
    HealthResponse, 
    ModelInfoResponse, 
    BrandsResponse
)
from .services import model_service

# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Car Price Prediction API", 
        "status": "running",
        "version": API_VERSION,
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy", 
        model_loaded=model_service.is_model_loaded()
    )

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_price(car_data: CarData):
    """Predict car price based on input features"""
    return model_service.predict_price(car_data)

@app.get("/model-info", response_model=ModelInfoResponse, tags=["Model"])
async def get_model_info():
    """Get model information and performance metrics"""
    return model_service.get_model_info()

@app.get("/brands", response_model=BrandsResponse, tags=["Data"])
async def get_available_brands():
    """Get available brands, models, and other options"""
    return model_service.get_available_options()

if __name__ == "__main__":
    import uvicorn
    print("🚗 Starting Car Price Prediction API Server...")
    print(f"📍 Server running on: http://{HOST}:{PORT}")
    print(f"📚 API Documentation: http://{HOST}:{PORT}/docs")
    uvicorn.run(app, host=HOST, port=PORT)
