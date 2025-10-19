"""
Test the Fraud Detection API
"""

import requests
import json
import time

def test_api():
    """Test the fraud detection API"""
    print("🔌 Testing Fraud Detection API")
    print("-" * 40)
    
    # API base URL
    base_url = "http://localhost:8000"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health Check: API is running")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {str(e)}")
        return
    
    # Test fraud prediction
    print("\n🎯 Testing Fraud Prediction:")
    
    # Sample transaction data
    sample_request = {
        "transaction_data": {
            "amount": 1500.00,
            "merchant": "Online Store",
            "timestamp": "2024-01-15T14:30:00Z",
            "card_type": "credit",
            "customer_id": "CUST123",
            "features": {
                "V1": -1.35,
                "V2": -0.07,
                "V3": 2.54,
                "V4": 1.38
            }
        },
        "customer_data": {
            "customer_id": "CUST123",
            "risk_profile": "medium",
            "age_group": "35-45",
            "location": "New York"
        },
        "model_type": "xgboost",
        "explain": True
    }
    
    headers = {
        "Authorization": "Bearer demo_token_123",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/fraud/predict",
            json=sample_request,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Fraud Prediction Successful:")
            print(f"   Case ID: {result['case_id']}")
            print(f"   Fraud Probability: {result['fraud_probability']:.2%}")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   Prediction: {result['prediction']}")
            print(f"   Confidence: {result['confidence']:.2%}")
            print(f"   Processing Time: {result['processing_time_ms']:.1f}ms")
            print(f"   Model Used: {result['model_used']}")
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Prediction request failed: {str(e)}")
    
    # Test batch prediction
    print("\n📦 Testing Batch Prediction:")
    
    batch_request = {
        "transactions": [
            {
                "transaction_data": {
                    "amount": 50.00,
                    "merchant": "Coffee Shop",
                    "timestamp": "2024-01-15T08:30:00Z",
                    "card_type": "credit",
                    "customer_id": "CUST124"
                },
                "model_type": "xgboost"
            },
            {
                "transaction_data": {
                    "amount": 5000.00,
                    "merchant": "Electronics Store",
                    "timestamp": "2024-01-15T23:45:00Z",
                    "card_type": "credit",
                    "customer_id": "CUST125"
                },
                "model_type": "xgboost"
            }
        ],
        "model_type": "xgboost",
        "include_explanations": False
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/fraud/predict/batch",
            json=batch_request,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Batch Prediction Successful:")
            print(f"   Total Processed: {result['total_processed']}")
            print(f"   Success Count: {result['success_count']}")
            print(f"   Error Count: {result['error_count']}")
            print(f"   Processing Time: {result['processing_time_ms']:.1f}ms")
            
            for i, prediction in enumerate(result['predictions']):
                print(f"   Transaction {i+1}: {prediction['prediction']} (prob: {prediction['fraud_probability']:.2%})")
        else:
            print(f"❌ Batch prediction failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Batch prediction request failed: {str(e)}")
    
    # Test model status
    print("\n📊 Testing Model Status:")
    
    try:
        response = requests.get(
            f"{base_url}/api/models/status",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Model Status Retrieved:")
            for model in models:
                print(f"   Model: {model['model_name']}")
                print(f"   Status: {model['status']}")
                print(f"   AUC: {model['performance_metrics']['auc']:.3f}")
        else:
            print(f"❌ Model status failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Model status request failed: {str(e)}")

if __name__ == "__main__":
    print("🧪 API Testing Suite")
    print("=" * 40)
    time.sleep(2)  # Wait for server to be ready
    test_api()
    print("\n✅ API testing completed!")
