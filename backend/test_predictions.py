#!/usr/bin/env python3
"""
Test script to evaluate prediction quality and accuracy
"""

from services import model_service
from models import CarData

def test_predictions():
    """Test multiple prediction scenarios"""
    
    # Test cases with different car types and conditions
    test_cases = [
        {
            'name': 'New Maruti Swift (2022)',
            'data': CarData(
                brand='Maruti Suzuki', 
                model='Swift', 
                year=2022, 
                kmDriven=15000, 
                fuelType='Petrol', 
                transmission='Manual', 
                engineSize=1.2, 
                city='Mumbai', 
                state='Maharashtra', 
                cngKit=False, 
                qualityScore=9.0
            )
        },
        {
            'name': 'Old Maruti Alto (2015)',
            'data': CarData(
                brand='Maruti Suzuki', 
                model='Alto', 
                year=2015, 
                kmDriven=120000, 
                fuelType='Petrol', 
                transmission='Manual', 
                engineSize=0.8, 
                city='Delhi', 
                state='Delhi', 
                cngKit=True, 
                qualityScore=6.5
            )
        },
        {
            'name': 'Luxury BMW 3 Series (2020)',
            'data': CarData(
                brand='BMW', 
                model='3 Series', 
                year=2020, 
                kmDriven=40000, 
                fuelType='Petrol', 
                transmission='Automatic', 
                engineSize=2.0, 
                city='Mumbai', 
                state='Maharashtra', 
                cngKit=False, 
                qualityScore=8.9
            )
        },
        {
            'name': 'Hyundai Creta (2021)',
            'data': CarData(
                brand='Hyundai', 
                model='Creta', 
                year=2021, 
                kmDriven=30000, 
                fuelType='Diesel', 
                transmission='Manual', 
                engineSize=1.5, 
                city='Bangalore', 
                state='Karnataka', 
                cngKit=False, 
                qualityScore=8.7
            )
        },
        {
            'name': 'Tata Nexon (2019)',
            'data': CarData(
                brand='Tata', 
                model='Nexon', 
                year=2019, 
                kmDriven=50000, 
                fuelType='Diesel', 
                transmission='Manual', 
                engineSize=1.5, 
                city='Chennai', 
                state='Tamil Nadu', 
                cngKit=False, 
                qualityScore=8.2
            )
        }
    ]

    print("🚗 Car Price Prediction Quality Analysis")
    print("=" * 60)
    
    # Get model info
    model_info = model_service.get_model_info()
    print(f"\n📊 Model Performance Metrics:")
    print(f"   R² Score: {model_info['model_metrics']['r2_score']:.3f}")
    print(f"   RMSE: ₹{model_info['model_metrics']['rmse']:,.0f}")
    print(f"   MAE: ₹{model_info['model_metrics']['mae']:,.0f}")
    print(f"   Training Date: {model_info['training_date']}")
    
    print(f"\n🔍 Prediction Tests:")
    print("-" * 60)
    
    for i, test in enumerate(test_cases, 1):
        try:
            result = model_service.predict_price(test['data'])
            print(f"\n{i}. {test['name']}:")
            print(f"   Predicted Price: ₹{result['predictedPrice']:,.0f}")
            print(f"   Confidence: {result['confidence']:.1f}%")
            print(f"   Features: {result['modelInfo']['features_used']}")
            
            # Analyze prediction reasonableness
            price = result['predictedPrice']
            if price < 200000:
                price_category = "Budget Car"
            elif price < 800000:
                price_category = "Mid-range Car"
            elif price < 2000000:
                price_category = "Premium Car"
            else:
                price_category = "Luxury Car"
            
            print(f"   Category: {price_category}")
            
        except Exception as e:
            print(f"\n{i}. {test['name']}: ❌ Error - {str(e)}")
    
    print(f"\n✅ Prediction Quality Assessment:")
    print(f"   • Model R² Score of {model_info['model_metrics']['r2_score']:.3f} indicates {'excellent' if model_info['model_metrics']['r2_score'] > 0.9 else 'good' if model_info['model_metrics']['r2_score'] > 0.8 else 'moderate'} accuracy")
    print(f"   • RMSE of ₹{model_info['model_metrics']['rmse']:,.0f} means predictions are typically within this range of actual prices")
    print(f"   • Model uses {model_info['features_count']} features for comprehensive analysis")
    print(f"   • Confidence scores are calculated based on prediction variance")

if __name__ == "__main__":
    test_predictions()
