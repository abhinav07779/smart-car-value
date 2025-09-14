# Car Price Prediction API Backend

A FastAPI-based machine learning API for predicting car prices based on various features.

## 🏗️ Project Structure

```
backend/
├── __init__.py          # Package initialization
├── app.py              # Main FastAPI application
├── config.py           # Configuration settings
├── models.py           # Pydantic models for validation
├── services.py         # Business logic and ML services
├── train_model.py      # Model training script
├── run_training.py     # Training execution script
├── run_server.py       # Server startup script
├── requirements.txt    # Python dependencies
├── car_price_model.pkl # Trained ML model
├── model_info.json     # Model metadata
└── README.md          # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model (if not already trained)
```bash
python run_training.py
```

### 3. Start the Server
```bash
# Option 1: Direct Python execution
python app.py

# Option 2: Using uvicorn
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Option 3: From project root
python start_backend.py
```

## 📡 API Endpoints

### Health Check
- **GET** `/health` - Check server and model status

### Predictions
- **POST** `/predict` - Predict car price
  ```json
  {
    "brand": "Maruti Suzuki",
    "model": "Swift",
    "year": 2020,
    "kmDriven": 45000,
    "fuelType": "Petrol",
    "transmission": "Manual",
    "engineSize": 1.2,
    "city": "Mumbai",
    "state": "Maharashtra",
    "cngKit": false,
    "qualityScore": 8.5
  }
  ```

### Model Information
- **GET** `/model-info` - Get model metrics and information
- **GET** `/brands` - Get available brands, models, and options

### Documentation
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative API documentation

## 🤖 Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: 13 features including categorical and numerical data
- **Performance**: R² Score: 0.92, RMSE: ₹437,514
- **Training Date**: 2025-09-14

## 🔧 Configuration

Edit `config.py` to modify:
- Server host and port
- CORS origins
- Model file paths
- Debug settings

## 📊 Model Features

### Numerical Features
- `year`: Manufacturing year
- `kmDriven`: Kilometers driven
- `engineSize`: Engine size in liters
- `cngKit`: CNG kit presence (0/1)
- `qualityScore`: Quality rating (0-10)
- `age`: Car age (calculated)
- `km_per_year`: Average km per year (calculated)

### Categorical Features (Label Encoded)
- `brand`: Car brand
- `model`: Car model
- `fuelType`: Fuel type (Petrol/Diesel/Electric)
- `transmission`: Transmission type (Manual/Automatic)
- `city`: City location
- `state`: State location

## 🛠️ Development

### Adding New Features
1. Update `models.py` for new data structures
2. Modify `services.py` for business logic
3. Update `config.py` for configuration changes
4. Test endpoints using `/docs`

### Model Retraining
1. Update dataset in `../car_price_dataset.csv`
2. Run `python run_training.py`
3. Restart the server

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F

# Or use a different port
uvicorn app:app --port 8001
```

### Model Not Loading
- Ensure `car_price_model.pkl` and `model_info.json` exist
- Check file permissions
- Verify model training completed successfully

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python path and virtual environment
