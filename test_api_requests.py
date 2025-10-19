"""
API Testing Script using Python Requests
Alternative to CURL for testing the Fraud Detection API
"""

import requests
import json
import time
from datetime import datetime

class APITester:
    def __init__(self, base_url="http://localhost:8000", auth_token="demo_token_123"):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        self.test_results = []
    
    def log_test(self, test_name, status, response_data=None, error=None):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "response": response_data,
            "error": str(error) if error else None
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {status}")
        if error:
            print(f"   Error: {error}")
        elif response_data and isinstance(response_data, dict):
            if "fraud_probability" in response_data:
                print(f"   Fraud Probability: {response_data['fraud_probability']:.2%}")
                print(f"   Prediction: {response_data['prediction']}")
            elif "status" in response_data:
                print(f"   Status: {response_data['status']}")
    
    def test_health_check(self):
        """Test 1: Health Check"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", "PASS", data)
                return True
            else:
                self.log_test("Health Check", "FAIL", error=f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", "FAIL", error=e)
            return False
    
    def test_api_info(self):
        """Test 2: API Root Info"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("API Info", "PASS", data)
                return True
            else:
                self.log_test("API Info", "FAIL", error=f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Info", "FAIL", error=e)
            return False
    
    def test_normal_transaction(self):
        """Test 3: Normal Transaction Prediction"""
        try:
            payload = {
                "transaction_data": {
                    "amount": 25.50,
                    "merchant": "Grocery Store",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "card_type": "debit",
                    "customer_id": "CUST001"
                },
                "model_type": "xgboost"
            }
            
            response = requests.post(
                f"{self.base_url}/api/fraud/predict",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Normal Transaction", "PASS", data)
                return True
            else:
                self.log_test("Normal Transaction", "FAIL", error=f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Normal Transaction", "FAIL", error=e)
            return False
    
    def test_suspicious_transaction(self):
        """Test 4: Suspicious Transaction Prediction"""
        try:
            payload = {
                "transaction_data": {
                    "amount": 5000.00,
                    "merchant": "Cash Advance ATM",
                    "timestamp": "2024-01-15T03:45:00Z",
                    "card_type": "credit",
                    "customer_id": "CUST003"
                },
                "model_type": "xgboost"
            }
            
            response = requests.post(
                f"{self.base_url}/api/fraud/predict",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Suspicious Transaction", "PASS", data)
                return True
            else:
                self.log_test("Suspicious Transaction", "FAIL", error=f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Suspicious Transaction", "FAIL", error=e)
            return False
    
    def test_batch_prediction(self):
        """Test 5: Batch Prediction"""
        try:
            payload = {
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
                            "amount": 2500.00,
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
            
            response = requests.post(
                f"{self.base_url}/api/fraud/predict/batch",
                json=payload,
                headers=self.headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Processed: {data['total_processed']} transactions")
                print(f"   Success: {data['success_count']}, Errors: {data['error_count']}")
                self.log_test("Batch Prediction", "PASS", data)
                return True
            else:
                self.log_test("Batch Prediction", "FAIL", error=f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Batch Prediction", "FAIL", error=e)
            return False
    
    def test_model_status(self):
        """Test 6: Model Status"""
        try:
            response = requests.get(
                f"{self.base_url}/api/models/status",
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Models loaded: {len(data)}")
                for model in data:
                    print(f"   - {model['model_name']}: {model['status']}")
                self.log_test("Model Status", "PASS", data)
                return True
            else:
                self.log_test("Model Status", "FAIL", error=f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Model Status", "FAIL", error=e)
            return False
    
    def test_model_reload(self):
        """Test 7: Model Reload"""
        try:
            response = requests.post(
                f"{self.base_url}/api/models/reload",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Model Reload", "PASS", data)
                return True
            else:
                self.log_test("Model Reload", "FAIL", error=f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Model Reload", "FAIL", error=e)
            return False
    
    def test_authentication_error(self):
        """Test 8: Authentication Error"""
        try:
            invalid_headers = {
                "Authorization": "Bearer invalid_token",
                "Content-Type": "application/json"
            }
            
            payload = {
                "transaction_data": {
                    "amount": 100.00,
                    "merchant": "Test Store",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "card_type": "credit",
                    "customer_id": "CUST001"
                },
                "model_type": "xgboost"
            }
            
            response = requests.post(
                f"{self.base_url}/api/fraud/predict",
                json=payload,
                headers=invalid_headers,
                timeout=5
            )
            
            if response.status_code == 401:
                self.log_test("Authentication Error", "PASS", {"expected_401": True})
                return True
            else:
                self.log_test("Authentication Error", "FAIL", error=f"Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Authentication Error", "FAIL", error=e)
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 FRAUD DETECTION API TESTING")
        print("=" * 50)
        print(f"Testing API at: {self.base_url}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()
        
        tests = [
            self.test_health_check,
            self.test_api_info,
            self.test_normal_transaction,
            self.test_suspicious_transaction,
            self.test_batch_prediction,
            self.test_model_status,
            self.test_model_reload,
            self.test_authentication_error
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        print()
        print("=" * 50)
        print("🏁 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {passed/total*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! API is working correctly.")
        else:
            print(f"⚠️ {total-passed} tests failed. Check the output above.")
        
        return self.test_results

def main():
    """Main function"""
    tester = APITester()
    
    # Check if server is running first
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code != 200:
            print("❌ API server is not responding properly")
            print("Please start the server with:")
            print("cd C:\\CFD\\phase4_rpa_integration")
            print("python api_integration/fraud_detection_api.py")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to API server at http://localhost:8000")
        print("Please start the server with:")
        print("cd C:\\CFD\\phase4_rpa_integration")
        print("python api_integration/fraud_detection_api.py")
        return
    
    # Run all tests
    results = tester.run_all_tests()
    
    # Save results to file
    with open("api_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: api_test_results.json")

if __name__ == "__main__":
    main()
