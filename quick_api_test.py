"""
Quick API Test - Verify endpoints are working
"""

import requests
import json

def test_endpoints():
    base_url = "http://localhost:8000"
    headers = {
        "Authorization": "Bearer demo_token_123",
        "Content-Type": "application/json"
    }
    
    print("🧪 QUICK API ENDPOINT TEST")
    print("=" * 40)
    
    # Test 1: Health Check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health Check: {response.status_code} - {response.json()['status']}")
    except Exception as e:
        print(f"❌ Health Check: {str(e)}")
    
    # Test 2: Model Status
    try:
        response = requests.get(f"{base_url}/api/models/status", headers=headers, timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Model Status: {len(models)} models loaded")
        else:
            print(f"⚠️ Model Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Model Status: {str(e)}")
    
    # Test 3: Simple Prediction
    try:
        sample_data = {
            "transaction_data": {
                "amount": 100.00,
                "merchant": "Test Store",
                "timestamp": "2024-01-15T10:30:00Z",
                "card_type": "credit",
                "customer_id": "TEST001"
            },
            "model_type": "xgboost"
        }
        
        response = requests.post(f"{base_url}/api/fraud/predict", 
                               json=sample_data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Fraud Prediction: {result['prediction']} (prob: {result['fraud_probability']:.2%})")
        else:
            print(f"⚠️ Fraud Prediction: {response.status_code} - {response.text[:100]}")
            
    except Exception as e:
        print(f"❌ Fraud Prediction: {str(e)}")
    
    print("\n🎯 Ready for Postman testing!")
    print("Server running at: http://localhost:8000")

if __name__ == "__main__":
    test_endpoints()
