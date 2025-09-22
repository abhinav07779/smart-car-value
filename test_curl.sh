#!/bin/bash
# Quick test script for deployed Car Price Prediction API

echo "🚀 Testing Car Price Prediction API Deployment"
echo "=============================================="

# Get URLs from user
read -p "Enter your Railway backend URL (e.g., https://your-app.railway.app): " BACKEND_URL
read -p "Enter your Vercel frontend URL (e.g., https://your-app.vercel.app): " FRONTEND_URL

echo ""
echo "🧪 Testing Backend API: $BACKEND_URL"
echo "===================================="

# Test 1: Health Check
echo "1. Testing Health Check..."
curl -s "$BACKEND_URL/health" | jq '.' 2>/dev/null || curl -s "$BACKEND_URL/health"
echo ""

# Test 2: API Root
echo "2. Testing API Root..."
curl -s "$BACKEND_URL/" | jq '.' 2>/dev/null || curl -s "$BACKEND_URL/"
echo ""

# Test 3: Model Info
echo "3. Testing Model Info..."
curl -s "$BACKEND_URL/model-info" | jq '.' 2>/dev/null || curl -s "$BACKEND_URL/model-info"
echo ""

# Test 4: Prediction
echo "4. Testing Prediction..."
curl -X POST "$BACKEND_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Maruti Suzuki",
    "model": "Swift",
    "year": 2020,
    "kmDriven": 50000,
    "fuelType": "Petrol",
    "transmission": "Manual",
    "engineSize": 1.2,
    "city": "Mumbai",
    "state": "Maharashtra",
    "cngKit": false,
    "qualityScore": 8.0
  }' | jq '.' 2>/dev/null || curl -X POST "$BACKEND_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Maruti Suzuki",
    "model": "Swift",
    "year": 2020,
    "kmDriven": 50000,
    "fuelType": "Petrol",
    "transmission": "Manual",
    "engineSize": 1.2,
    "city": "Mumbai",
    "state": "Maharashtra",
    "cngKit": false,
    "qualityScore": 8.0
  }'
echo ""

echo "🌐 Testing Frontend: $FRONTEND_URL"
echo "=================================="

# Test 5: Frontend Load
echo "5. Testing Frontend Load..."
curl -s -I "$FRONTEND_URL" | head -1
echo ""

echo "✅ Testing Complete!"
echo ""
echo "🔗 Backend API: $BACKEND_URL"
echo "🔗 Frontend: $FRONTEND_URL"
echo "🔗 API Docs: $BACKEND_URL/docs"

