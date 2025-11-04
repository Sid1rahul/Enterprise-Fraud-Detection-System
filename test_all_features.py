"""
Comprehensive Feature Testing Script
Tests all backend endpoints and validates responses
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("\n🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_model_status():
    """Test model status endpoint"""
    print("\n🔍 Testing Model Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/models/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ Model status check passed")
            print(f"   Models loaded: {data.get('models_loaded', [])}")
            return True
        else:
            print(f"❌ Model status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model status error: {str(e)}")
        return False

def test_fraud_detection():
    """Test fraud detection endpoint"""
    print("\n🔍 Testing Fraud Detection...")
    try:
        test_data = {
            "amount": 1500.00,
            "merchant": "Test Store",
            "category": "retail",
            "location": "New York"
        }
        response = requests.post(f"{BASE_URL}/api/detect", json=test_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Fraud detection passed")
            print(f"   Risk Score: {data.get('risk_score', 'N/A')}")
            print(f"   Prediction: {data.get('prediction', 'N/A')}")
            return True
        else:
            print(f"❌ Fraud detection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Fraud detection error: {str(e)}")
        return False

def test_monitoring_start():
    """Test monitoring session start"""
    print("\n🔍 Testing Monitoring Start...")
    try:
        response = requests.post(f"{BASE_URL}/api/monitoring/start", 
                                data={'file_id': 'TEST_FILE', 'processing_speed_ms': 1000})
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print("✅ Monitoring start passed")
            print(f"   Session ID: {session_id}")
            return session_id
        else:
            print(f"❌ Monitoring start failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Monitoring start error: {str(e)}")
        return None

def test_monitoring_status(session_id):
    """Test monitoring status endpoint"""
    print("\n🔍 Testing Monitoring Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/monitoring/status/{session_id}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Monitoring status passed")
            print(f"   Processed: {data.get('processed_count', 0)}")
            print(f"   Fraud Detected: {data.get('fraud_detected', 0)}")
            return True
        else:
            print(f"❌ Monitoring status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Monitoring status error: {str(e)}")
        return False

def test_chatbot():
    """Test chatbot endpoint"""
    print("\n🔍 Testing Chatbot...")
    try:
        test_message = {
            "message": "Check system health",
            "user_id": "test_user"
        }
        response = requests.post(f"{BASE_URL}/api/chatbot", json=test_message)
        if response.status_code == 200:
            data = response.json()
            print("✅ Chatbot passed")
            print(f"   Response: {data.get('response', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Chatbot failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Chatbot error: {str(e)}")
        return False

def test_analytics():
    """Test analytics endpoint"""
    print("\n🔍 Testing Analytics...")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/summary")
        if response.status_code == 200:
            data = response.json()
            print("✅ Analytics passed")
            print(f"   Total Transactions: {data.get('total_transactions', 0)}")
            return True
        else:
            print(f"❌ Analytics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analytics error: {str(e)}")
        return False

def run_all_tests():
    """Run all feature tests"""
    print("=" * 60)
    print("🧪 COMPREHENSIVE FEATURE TESTING")
    print("=" * 60)
    print(f"Testing backend at: {BASE_URL}")
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'passed': 0,
        'failed': 0,
        'total': 0
    }
    
    # Run all tests
    tests = [
        ('Health Check', test_health_check),
        ('Model Status', test_model_status),
        ('Fraud Detection', test_fraud_detection),
        ('Chatbot', test_chatbot),
        ('Analytics', test_analytics),
    ]
    
    for test_name, test_func in tests:
        results['total'] += 1
        try:
            if test_func():
                results['passed'] += 1
            else:
                results['failed'] += 1
        except Exception as e:
            print(f"❌ {test_name} crashed: {str(e)}")
            results['failed'] += 1
    
    # Test monitoring separately (needs session)
    results['total'] += 2
    session_id = test_monitoring_start()
    if session_id:
        results['passed'] += 1
        if test_monitoring_status(session_id):
            results['passed'] += 1
        else:
            results['failed'] += 1
    else:
        results['failed'] += 2
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    print("=" * 60)
    
    return results['failed'] == 0

if __name__ == "__main__":
    print("\n⚠️  Make sure the Flask server is running on http://localhost:5000")
    print("   Start it with: python phase1_data_foundation/flask_server.py\n")
    
    input("Press Enter to start testing...")
    
    success = run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! System is ready for Git commit.")
    else:
        print("\n⚠️  Some tests failed. Please fix issues before committing.")
