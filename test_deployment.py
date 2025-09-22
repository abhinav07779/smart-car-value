#!/usr/bin/env python3
"""
Test script for deployed Car Price Prediction API
"""
import requests
import json
import sys
from typing import Dict, Any

def test_backend_api(backend_url: str) -> Dict[str, Any]:
    """Test the deployed backend API"""
    results = {
        "backend_url": backend_url,
        "tests_passed": 0,
        "tests_failed": 0,
        "errors": []
    }
    
    print(f"🧪 Testing Backend API: {backend_url}")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get(f"{backend_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("   ✅ Health check passed")
                results["tests_passed"] += 1
            else:
                print(f"   ❌ Health check failed: {data}")
                results["tests_failed"] += 1
                results["errors"].append("Health check returned unexpected data")
        else:
            print(f"   ❌ Health check failed: HTTP {response.status_code}")
            results["tests_failed"] += 1
            results["errors"].append(f"Health check HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        results["tests_failed"] += 1
        results["errors"].append(f"Health check error: {e}")
    
    # Test 2: API Root
    print("\n2. Testing API Root...")
    try:
        response = requests.get(f"{backend_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API root: {data.get('message', 'No message')}")
            results["tests_passed"] += 1
        else:
            print(f"   ❌ API root failed: HTTP {response.status_code}")
            results["tests_failed"] += 1
            results["errors"].append(f"API root HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ API root error: {e}")
        results["tests_failed"] += 1
        results["errors"].append(f"API root error: {e}")
    
    # Test 3: Model Info
    print("\n3. Testing Model Info...")
    try:
        response = requests.get(f"{backend_url}/model-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Model info retrieved")
            print(f"   📊 Best model: {data.get('model_metrics', {}).get('best_model', 'Unknown')}")
            results["tests_passed"] += 1
        else:
            print(f"   ❌ Model info failed: HTTP {response.status_code}")
            results["tests_failed"] += 1
            results["errors"].append(f"Model info HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Model info error: {e}")
        results["tests_failed"] += 1
        results["errors"].append(f"Model info error: {e}")
    
    # Test 4: Prediction Endpoint
    print("\n4. Testing Prediction Endpoint...")
    test_data = {
        "brand": "Maruti Suzuki",
        "model": "Swift",
        "year": 2020,
        "kmDriven": 50000,
        "fuelType": "Petrol",
        "transmission": "Manual",
        "engineSize": 1.2,
        "city": "Mumbai",
        "state": "Maharashtra",
        "cngKit": False,
        "qualityScore": 8.0
    }
    
    try:
        response = requests.post(
            f"{backend_url}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            predicted_price = data.get("predictedPrice", 0)
            confidence = data.get("confidence", 0)
            print(f"   ✅ Prediction successful")
            print(f"   💰 Predicted Price: ₹{predicted_price:,.2f}")
            print(f"   📈 Confidence: {confidence}%")
            print(f"   📊 RMSE: {data.get('rmse', 'N/A')}")
            print(f"   📊 R² Score: {data.get('r2Score', 'N/A')}")
            results["tests_passed"] += 1
        else:
            print(f"   ❌ Prediction failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            results["tests_failed"] += 1
            results["errors"].append(f"Prediction HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ❌ Prediction error: {e}")
        results["tests_failed"] += 1
        results["errors"].append(f"Prediction error: {e}")
    
    # Test 5: API Documentation
    print("\n5. Testing API Documentation...")
    try:
        response = requests.get(f"{backend_url}/docs", timeout=10)
        if response.status_code == 200:
            print("   ✅ API documentation accessible")
            results["tests_passed"] += 1
        else:
            print(f"   ❌ API docs failed: HTTP {response.status_code}")
            results["tests_failed"] += 1
            results["errors"].append(f"API docs HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ API docs error: {e}")
        results["tests_failed"] += 1
        results["errors"].append(f"API docs error: {e}")
    
    return results

def test_frontend(frontend_url: str) -> Dict[str, Any]:
    """Test the deployed frontend"""
    results = {
        "frontend_url": frontend_url,
        "tests_passed": 0,
        "tests_failed": 0,
        "errors": []
    }
    
    print(f"\n🌐 Testing Frontend: {frontend_url}")
    print("=" * 50)
    
    # Test 1: Frontend Loads
    print("1. Testing Frontend Load...")
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("   ✅ Frontend loads successfully")
            results["tests_passed"] += 1
            
            # Check for key content
            content = response.text
            if "Car Price Predictor" in content:
                print("   ✅ Main title found")
                results["tests_passed"] += 1
            else:
                print("   ⚠️  Main title not found")
                results["tests_failed"] += 1
                results["errors"].append("Main title not found in HTML")
                
            if "Machine Learning" in content:
                print("   ✅ ML content found")
                results["tests_passed"] += 1
            else:
                print("   ⚠️  ML content not found")
                results["tests_failed"] += 1
                results["errors"].append("ML content not found in HTML")
        else:
            print(f"   ❌ Frontend load failed: HTTP {response.status_code}")
            results["tests_failed"] += 1
            results["errors"].append(f"Frontend load HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Frontend load error: {e}")
        results["tests_failed"] += 1
        results["errors"].append(f"Frontend load error: {e}")
    
    return results

def main():
    """Main test function"""
    print("🚀 Car Price Prediction API - Deployment Test")
    print("=" * 60)
    
    # Get URLs from user
    backend_url = input("Enter your Railway backend URL (e.g., https://your-app.railway.app): ").strip()
    if not backend_url:
        print("❌ Backend URL is required")
        return
    
    frontend_url = input("Enter your Vercel frontend URL (e.g., https://your-app.vercel.app): ").strip()
    if not frontend_url:
        print("❌ Frontend URL is required")
        return
    
    # Test backend
    backend_results = test_backend_api(backend_url)
    
    # Test frontend
    frontend_results = test_frontend(frontend_url)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_passed = backend_results["tests_passed"] + frontend_results["tests_passed"]
    total_failed = backend_results["tests_failed"] + frontend_results["tests_failed"]
    
    print(f"Backend Tests: {backend_results['tests_passed']} passed, {backend_results['tests_failed']} failed")
    print(f"Frontend Tests: {frontend_results['tests_passed']} passed, {frontend_results['tests_failed']} failed")
    print(f"Total: {total_passed} passed, {total_failed} failed")
    
    if total_failed == 0:
        print("\n🎉 All tests passed! Your deployment is working perfectly!")
    else:
        print(f"\n⚠️  {total_failed} tests failed. Check the errors above.")
        print("\nErrors:")
        for error in backend_results["errors"] + frontend_results["errors"]:
            print(f"  - {error}")
    
    print(f"\n🔗 Backend API: {backend_url}")
    print(f"🔗 Frontend: {frontend_url}")
    print(f"🔗 API Docs: {backend_url}/docs")

if __name__ == "__main__":
    main()

