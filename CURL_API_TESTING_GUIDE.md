# 🔌 CURL API TESTING GUIDE
## Credit Card Fraud Detection API Endpoints

### 🚀 **Prerequisites**

1. **Start the API Server**:
   ```bash
   cd C:\CFD\phase4_rpa_integration
   python api_integration/fraud_detection_api.py
   ```
   Server will run on: `http://localhost:8000`

2. **Ensure CURL is installed** (comes with Windows 10+ by default)

---

## 📋 **CURL COMMANDS FOR EACH ENDPOINT**

### **1. Health Check** ✅
**Purpose**: Verify API is running and check system status

```bash
curl -X GET "http://localhost:8000/health" ^
  -H "Content-Type: application/json"
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-17T13:30:00.123456",
  "models_loaded": ["xgboost", "isolation_forest"]
}
```

---

### **2. Root Endpoint** ℹ️
**Purpose**: Basic API information

```bash
curl -X GET "http://localhost:8000/" ^
  -H "Content-Type: application/json"
```

**Expected Response**:
```json
{
  "message": "Credit Card Fraud Detection API",
  "version": "1.0.0"
}
```

---

### **3. Single Fraud Prediction - Normal Transaction** 🎯
**Purpose**: Predict fraud for a low-risk transaction

```bash
curl -X POST "http://localhost:8000/api/fraud/predict" ^
  -H "Authorization: Bearer demo_token_123" ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_data\": {\"amount\": 25.50, \"merchant\": \"Grocery Store\", \"timestamp\": \"2024-01-15T10:30:00Z\", \"card_type\": \"debit\", \"customer_id\": \"CUST001\", \"features\": {\"V1\": -0.15, \"V2\": 0.07, \"V3\": 0.34, \"V4\": 0.18}}, \"customer_data\": {\"customer_id\": \"CUST001\", \"risk_profile\": \"low\", \"age_group\": \"25-35\", \"location\": \"Chicago\"}, \"model_type\": \"xgboost\", \"explain\": true}"
```

---

### **4. Single Fraud Prediction - Suspicious Transaction** ⚠️
**Purpose**: Predict fraud for a high-risk transaction

```bash
curl -X POST "http://localhost:8000/api/fraud/predict" ^
  -H "Authorization: Bearer demo_token_123" ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_data\": {\"amount\": 5000.00, \"merchant\": \"Cash Advance ATM\", \"timestamp\": \"2024-01-15T03:45:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST003\", \"features\": {\"V1\": -2.35, \"V2\": 1.87, \"V3\": -3.54, \"V4\": 2.98, \"V5\": -1.34}}, \"customer_data\": {\"customer_id\": \"CUST003\", \"risk_profile\": \"high\", \"age_group\": \"unknown\", \"location\": \"unknown\"}, \"model_type\": \"xgboost\", \"explain\": true}"
```

---

### **5. Batch Fraud Prediction** 📦
**Purpose**: Predict fraud for multiple transactions at once

```bash
curl -X POST "http://localhost:8000/api/fraud/predict/batch" ^
  -H "Authorization: Bearer demo_token_123" ^
  -H "Content-Type: application/json" ^
  -d "{\"transactions\": [{\"transaction_data\": {\"amount\": 50.00, \"merchant\": \"Coffee Shop\", \"timestamp\": \"2024-01-15T08:30:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST124\"}, \"model_type\": \"xgboost\"}, {\"transaction_data\": {\"amount\": 5000.00, \"merchant\": \"Luxury Store\", \"timestamp\": \"2024-01-15T23:45:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST125\"}, \"model_type\": \"xgboost\"}, {\"transaction_data\": {\"amount\": 25.99, \"merchant\": \"Gas Station\", \"timestamp\": \"2024-01-15T12:15:00Z\", \"card_type\": \"debit\", \"customer_id\": \"CUST126\"}, \"model_type\": \"isolation_forest\"}], \"model_type\": \"xgboost\", \"include_explanations\": false}"
```

---

### **6. Model Status** 📊
**Purpose**: Check status and performance of loaded models

```bash
curl -X GET "http://localhost:8000/api/models/status" ^
  -H "Authorization: Bearer demo_token_123" ^
  -H "Content-Type: application/json"
```

**Expected Response**:
```json
[
  {
    "model_name": "xgboost",
    "status": "active",
    "last_updated": "2025-10-17T13:30:00.123456",
    "version": "1.0.0",
    "performance_metrics": {
      "accuracy": 0.95,
      "precision": 0.87,
      "recall": 0.82,
      "f1_score": 0.84,
      "auc": 0.93
    }
  }
]
```

---

### **7. Reload Models** 🔄
**Purpose**: Reload ML models (useful for updates)

```bash
curl -X POST "http://localhost:8000/api/models/reload" ^
  -H "Authorization: Bearer demo_token_123" ^
  -H "Content-Type: application/json"
```

---

### **8. Test Authentication Error** ❌
**Purpose**: Test invalid authentication

```bash
curl -X POST "http://localhost:8000/api/fraud/predict" ^
  -H "Authorization: Bearer invalid_token" ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_data\": {\"amount\": 100.00, \"merchant\": \"Test Store\", \"timestamp\": \"2024-01-15T10:30:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST001\"}, \"model_type\": \"xgboost\"}"
```

**Expected Response**: `401 Unauthorized`

---

## 🧪 **TESTING SCENARIOS**

### **Scenario 1: Normal Transaction** ✅
```bash
curl -X POST "http://localhost:8000/api/fraud/predict" ^
  -H "Authorization: Bearer demo_token_123" ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_data\": {\"amount\": 25.50, \"merchant\": \"Grocery Store\", \"timestamp\": \"2024-01-15T10:30:00Z\", \"card_type\": \"debit\", \"customer_id\": \"CUST001\"}, \"model_type\": \"xgboost\"}"
```
**Expected**: Low fraud probability, "approve" or "monitor"

### **Scenario 2: Medium Risk Transaction** ⚠️
```bash
curl -X POST "http://localhost:8000/api/fraud/predict" ^
  -H "Authorization: Bearer demo_token_123" ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_data\": {\"amount\": 800.00, \"merchant\": \"Online Store\", \"timestamp\": \"2024-01-15T02:30:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST002\"}, \"model_type\": \"xgboost\"}"
```
**Expected**: Medium fraud probability, "review"

### **Scenario 3: High Risk Transaction** 🚨
```bash
curl -X POST "http://localhost:8000/api/fraud/predict" ^
  -H "Authorization: Bearer demo_token_123" ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_data\": {\"amount\": 5000.00, \"merchant\": \"Cash Advance\", \"timestamp\": \"2024-01-15T03:45:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST003\"}, \"model_type\": \"xgboost\"}"
```
**Expected**: High fraud probability, "fraud"

---

## 📊 **RESPONSE INTERPRETATION**

### **Fraud Probability Ranges**:
- **0.0 - 0.1**: Minimal risk → "approve"
- **0.1 - 0.3**: Low risk → "monitor"  
- **0.3 - 0.6**: Medium risk → "review"
- **0.6 - 0.8**: High risk → "fraud"
- **0.8 - 1.0**: Critical risk → "fraud"

### **Risk Levels**:
- **minimal**: Very low fraud probability
- **low**: Low fraud probability
- **medium**: Moderate fraud probability  
- **high**: High fraud probability
- **critical**: Very high fraud probability

---

## 🎯 **WHAT EACH ENDPOINT DOES**

| Endpoint | Purpose | Use Case |
|----------|---------|----------|
| `/health` | System health check | Monitoring, load balancer health checks |
| `/` | API information | Documentation, version checking |
| `/api/fraud/predict` | Single transaction fraud detection | Real-time transaction processing |
| `/api/fraud/predict/batch` | Multiple transaction processing | Batch processing, historical analysis |
| `/api/models/status` | Model performance monitoring | System monitoring, model health |
| `/api/models/reload` | Model updates | Deployment, model versioning |

---

## 🚀 **QUICK TEST SEQUENCE**

Run these commands in order to test all functionality:

```bash
# 1. Check if API is running
curl -X GET "http://localhost:8000/health"

# 2. Get API info
curl -X GET "http://localhost:8000/"

# 3. Test normal transaction
curl -X POST "http://localhost:8000/api/fraud/predict" -H "Authorization: Bearer demo_token_123" -H "Content-Type: application/json" -d "{\"transaction_data\": {\"amount\": 25.50, \"merchant\": \"Grocery Store\", \"timestamp\": \"2024-01-15T10:30:00Z\", \"card_type\": \"debit\", \"customer_id\": \"CUST001\"}, \"model_type\": \"xgboost\"}"

# 4. Test suspicious transaction
curl -X POST "http://localhost:8000/api/fraud/predict" -H "Authorization: Bearer demo_token_123" -H "Content-Type: application/json" -d "{\"transaction_data\": {\"amount\": 5000.00, \"merchant\": \"Cash Advance\", \"timestamp\": \"2024-01-15T03:45:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST003\"}, \"model_type\": \"xgboost\"}"

# 5. Check model status
curl -X GET "http://localhost:8000/api/models/status" -H "Authorization: Bearer demo_token_123"

# 6. Test authentication error
curl -X POST "http://localhost:8000/api/fraud/predict" -H "Authorization: Bearer invalid_token" -H "Content-Type: application/json" -d "{\"transaction_data\": {\"amount\": 100.00, \"merchant\": \"Test Store\", \"timestamp\": \"2024-01-15T10:30:00Z\", \"card_type\": \"credit\", \"customer_id\": \"CUST001\"}, \"model_type\": \"xgboost\"}"
```

This will give you a complete test of your fraud detection API using CURL! 🎉
