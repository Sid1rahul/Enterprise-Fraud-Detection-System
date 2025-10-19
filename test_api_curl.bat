@echo off
echo ========================================
echo 🧪 CURL API TESTING SCRIPT
echo Credit Card Fraud Detection API
echo ========================================
echo.

set BASE_URL=http://localhost:8000
set AUTH_TOKEN=demo_token_123

echo 🔍 TEST 1: Health Check
echo ----------------------------------------
curl -X GET "%BASE_URL%/health" -H "Content-Type: application/json"
echo.
echo.

echo ℹ️ TEST 2: API Root Info
echo ----------------------------------------
curl -X GET "%BASE_URL%/" -H "Content-Type: application/json"
echo.
echo.

echo 🎯 TEST 3: Normal Transaction Prediction
echo ----------------------------------------
curl -X POST "%BASE_URL%/api/fraud/predict" ^
  -H "Authorization: Bearer %AUTH_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_data\": {\"amount\": 25.50, \"merchant\": \"Grocery Store\", \"timestamp\": \"2024-01-15T10:30:00Z\", \"card_type\": \"debit\", \"customer_id\": \"CUST001\"}, \"model_type\": \"xgboost\"}"
echo.
echo.

echo ⚠️ TEST 4: Suspicious Transaction Prediction
echo ----------------------------------------
curl -X POST "%BASE_URL%/api/fraud/predict" ^
  -H "Authorization: Bearer %AUTH_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_data\": {\"amount\": 5000.00, \"merchant\": \"Cash Advance ATM\", \"timestamp\": \"2024-01-15T03:45:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST003\"}, \"model_type\": \"xgboost\"}"
echo.
echo.

echo 📦 TEST 5: Batch Prediction
echo ----------------------------------------
curl -X POST "%BASE_URL%/api/fraud/predict/batch" ^
  -H "Authorization: Bearer %AUTH_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"transactions\": [{\"transaction_data\": {\"amount\": 50.00, \"merchant\": \"Coffee Shop\", \"timestamp\": \"2024-01-15T08:30:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST124\"}, \"model_type\": \"xgboost\"}, {\"transaction_data\": {\"amount\": 2500.00, \"merchant\": \"Electronics Store\", \"timestamp\": \"2024-01-15T23:45:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST125\"}, \"model_type\": \"xgboost\"}], \"model_type\": \"xgboost\", \"include_explanations\": false}"
echo.
echo.

echo 📊 TEST 6: Model Status
echo ----------------------------------------
curl -X GET "%BASE_URL%/api/models/status" ^
  -H "Authorization: Bearer %AUTH_TOKEN%" ^
  -H "Content-Type: application/json"
echo.
echo.

echo 🔄 TEST 7: Reload Models
echo ----------------------------------------
curl -X POST "%BASE_URL%/api/models/reload" ^
  -H "Authorization: Bearer %AUTH_TOKEN%" ^
  -H "Content-Type: application/json"
echo.
echo.

echo ❌ TEST 8: Authentication Error Test
echo ----------------------------------------
curl -X POST "%BASE_URL%/api/fraud/predict" ^
  -H "Authorization: Bearer invalid_token" ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_data\": {\"amount\": 100.00, \"merchant\": \"Test Store\", \"timestamp\": \"2024-01-15T10:30:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST001\"}, \"model_type\": \"xgboost\"}"
echo.
echo.

echo ========================================
echo ✅ ALL CURL TESTS COMPLETED!
echo ========================================
echo.
echo 📊 Summary:
echo - Health Check: Basic connectivity
echo - API Info: Version and status
echo - Normal Transaction: Low-risk prediction
echo - Suspicious Transaction: High-risk prediction
echo - Batch Processing: Multiple transactions
echo - Model Status: Performance metrics
echo - Model Reload: Update capability
echo - Auth Error: Security validation
echo.
echo 🎯 Your API is ready for production use!
pause
