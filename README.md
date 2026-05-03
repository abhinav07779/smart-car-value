# 🚗 Car Price Prediction AI
Deployment done by vecel-https://drive-price-ai-main.vercel.app/

A full-stack machine learning application that predicts car prices using a trained Random Forest model with 91.96% accuracy, built for the Indian automotive market.

## 🌟 Features

- **AI-Powered Predictions**: Random Forest Regressor with 91.96% accuracy
- **Multi-Currency Support**: View prices in INR, USD, EUR, GBP, JPY, CAD, AUD
- **Comprehensive Data**: 15+ brands, 200+ models, Indian market focus
- **Real-time API**: FastAPI backend with automatic documentation
- **Modern UI**: React + TypeScript with Tailwind CSS and shadcn/ui
- **Price Comparison**: Integration with OLX, CarDekho, and Cars24
- **Responsive Design**: Mobile and desktop optimized

## 🏗️ Project Structure

```
car-price-ai/
├── backend/                    # FastAPI backend
│   ├── data/                  # Dataset files
│   │   └── car_price_dataset.csv
│   ├── models/                # ML model files
│   │   ├── car_price_model.pkl
│   │   └── model_info.json
│   ├── utils/                 # Utility functions
│   ├── app.py                 # FastAPI application
│   ├── config.py              # Configuration settings
│   ├── models.py              # Pydantic models
│   ├── services.py            # ML service layer
│   ├── train_model.py         # Model training script
│   └── requirements.txt       # Python dependencies
├── src/                       # React frontend
│   ├── components/            # React components
│   │   ├── CarPricePredictor.tsx
│   │   ├── DatasetVisualization.tsx
│   │   └── ui/                # shadcn/ui components
│   ├── contexts/              # React contexts
│   ├── hooks/                 # Custom hooks
│   ├── lib/                   # Utility functions
│   ├── pages/                 # Page components
│   └── utils/                 # Helper functions
├── scripts/                   # Utility scripts
│   ├── start-dev.py          # Start development environment
│   ├── start-backend.py      # Start backend only
│   └── test-connection.py    # Test frontend-backend connection
├── public/                    # Static assets
├── package.json              # Node.js dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd car-price-ai
   ```

2. **Install backend dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   npm install
   ```

### Development

**Start full development environment:**
```bash
python scripts/start-dev.py
```

**Start only backend:**
```bash
python scripts/start-backend.py
```

**Start only frontend:**
```bash
npm run dev
```

### Testing

**Test frontend-backend connection:**
```bash
python scripts/test-connection.py
```

## 🌐 Access Points

- **Frontend**: http://localhost:8080
- **Backend API**: http://127.0.0.1:8002
- **API Documentation**: http://127.0.0.1:8002/docs

## 🤖 Machine Learning Model

- **Algorithm**: Random Forest Regressor
- **Accuracy**: 91.96% (R² Score: 0.9196)
- **Training Data**: 50,000+ Indian car samples
- **Features**: Brand, Model, Year, KM Driven, Fuel Type, Transmission, Engine Size, Location, CNG Kit, Quality Score

## 🛠️ Technology Stack

### Frontend
- React 18.3.1 + TypeScript 5.8.3
- Vite 5.4.19 (build tool)
- Tailwind CSS 3.4.17 (styling)
- Radix UI (component primitives)
- React Query 5.83.0 (data fetching)

### Backend
- Python 3.13+ (runtime)
- FastAPI 0.104.1 (web framework)
- scikit-learn 1.3.2 (ML library)
- pandas 2.1.3 (data processing)
- Pydantic 2.5.0 (data validation)

## 📊 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Car price prediction
- `GET /model-info` - Model performance metrics
- `GET /brands` - Available brands and models

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Recommended**: Vercel (Frontend) + Railway (Backend)

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you have any questions or issues, please open an issue on GitHub.
