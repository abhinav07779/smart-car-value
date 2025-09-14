#!/usr/bin/env python3
"""
Test XUV700 prediction to debug the low price issue
"""

from services import model_service
from models import CarData

def test_xuv700():
    """Test XUV700 prediction with different configurations"""
    
    test_cases = [
        {
            'name': 'XUV700 - 2021, 30k km, Mumbai',
            'data': CarData(
                brand='Mahindra',
                model='XUV700',
                year=2021,
                kmDriven=30000,
                fuelType='Diesel',
                transmission='Manual',
                engineSize=2.2,
                city='Mumbai',
                state='Maharashtra',
                cngKit=False,
                qualityScore=8.5
            )
        },
        {
            'name': 'XUV700 - 2022, 20k km, Delhi',
            'data': CarData(
                brand='Mahindra',
                model='XUV700',
                year=2022,
                kmDriven=20000,
                fuelType='Diesel',
                transmission='Automatic',
                engineSize=2.2,
                city='Delhi',
                state='Delhi',
                cngKit=False,
                qualityScore=9.0
            )
        },
        {
            'name': 'XUV700 - 2020, 50k km, Bangalore',
            'data': CarData(
                brand='Mahindra',
                model='XUV700',
                year=2020,
                kmDriven=50000,
                fuelType='Diesel',
                transmission='Manual',
                engineSize=2.2,
                city='Bangalore',
                state='Karnataka',
                cngKit=False,
                qualityScore=8.0
            )
        }
    ]
    
    print("🚗 Mahindra XUV700 Price Prediction Analysis")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        try:
            result = model_service.predict_price(test['data'])
            print(f"\n{i}. {test['name']}:")
            print(f"   Predicted Price: ₹{result['predictedPrice']:,.0f}")
            print(f"   Confidence: {result['confidence']:.1f}%")
            
            # Check if price seems reasonable
            price = result['predictedPrice']
            if price < 800000:
                print(f"   ⚠️  WARNING: Price seems too low for XUV700!")
            elif price < 1200000:
                print(f"   ⚠️  Price seems low for XUV700")
            elif price < 1800000:
                print(f"   ✅ Price seems reasonable for XUV700")
            else:
                print(f"   ✅ Price seems high but possible for XUV700")
                
        except Exception as e:
            print(f"\n{i}. {test['name']}: ❌ Error - {str(e)}")
    
    # Check available models
    print(f"\n🔍 Available Mahindra Models:")
    try:
        options = model_service.get_available_options()
        mahindra_models = [model for model in options['models'] if 'XUV' in model or 'Mahindra' in model]
        print(f"   {mahindra_models}")
    except Exception as e:
        print(f"   Error getting models: {e}")

if __name__ == "__main__":
    test_xuv700()
