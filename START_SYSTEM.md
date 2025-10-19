# 🚀 FRAUD DETECTION SYSTEM - STARTUP GUIDE

## Quick Start Instructions

### 1. **Start the Backend API** (Terminal 1)
```bash
cd C:\CFD\phase4_rpa_integration
python api_integration/fraud_detection_api.py
```
**Expected Output**: Server running on http://localhost:8000

### 2. **Start the Frontend** (Terminal 2) 
```bash
cd C:\CFD\phase5_frontend
npm install  # (if not already done)
npm start
```
**Expected Output**: React app running on http://localhost:3000

### 3. **Open in Browser**
Navigate to: **http://localhost:3000**

---

## 🎯 **FEATURES TO TEST**

### **Dashboard Page** (`/dashboard`)
✅ **Real-time metrics and charts**
- Transaction statistics
- Fraud detection trends  
- Risk distribution pie chart
- Model performance metrics
- Recent activity feed
- API status monitoring

### **Fraud Detection Page** (`/fraud-detection`)
✅ **Single transaction analysis**
- Transaction form with validation
- Real-time fraud prediction
- Risk level assessment
- SHAP explanations (if enabled)
- Transaction history
- Mock data generation

### **Batch Processing Page** (`/batch-processing`)
✅ **Multiple transaction processing**
- Add/remove transactions
- Bulk fraud analysis
- Progress tracking
- Results summary with charts
- Export to CSV
- Mock batch data generation

### **Analytics Page** (`/analytics`)
✅ **Advanced reporting and insights**
- Fraud trend analysis
- Merchant risk breakdown
- Hourly pattern analysis
- Model performance comparison
- Interactive charts and filters
- Data export functionality

### **Settings Page** (`/settings`)
✅ **System configuration**
- API endpoint configuration
- Model parameters
- Notification preferences
- UI theme settings
- Security options
- System information

---

## 🔧 **BACKEND API ENDPOINTS TO TEST**

### **Health Check**
```bash
curl http://localhost:8000/health
```

### **Single Fraud Prediction**
```bash
curl -X POST http://localhost:8000/api/fraud/predict \
  -H "Authorization: Bearer demo_token_123" \
  -H "Content-Type: application/json" \
  -d '{"transaction_data": {"amount": 1500, "merchant": "Test Store", "timestamp": "2024-01-15T10:30:00Z", "card_type": "credit", "customer_id": "CUST001"}, "model_type": "xgboost"}'
```

### **Batch Processing**
```bash
curl -X POST http://localhost:8000/api/fraud/predict/batch \
  -H "Authorization: Bearer demo_token_123" \
  -H "Content-Type: application/json" \
  -d '{"transactions": [{"transaction_data": {"amount": 100, "merchant": "Coffee Shop", "timestamp": "2024-01-15T08:30:00Z", "card_type": "credit", "customer_id": "CUST124"}}, {"transaction_data": {"amount": 5000, "merchant": "Electronics", "timestamp": "2024-01-15T23:45:00Z", "card_type": "credit", "customer_id": "CUST125"}}], "model_type": "xgboost"}'
```

---

## 🎨 **UI FEATURES TO EXPLORE**

### **Dark Aqua Theme**
- Deep dark background (`#0f0f23`, `#1a1a2e`, `#16213e`)
- Aqua blue accents (`#00d4ff`, `#00b8e6`)
- Smooth animations and transitions
- Glowing effects on interactive elements
- Modern card-based layout

### **Interactive Elements**
- Hover effects on cards and buttons
- Animated progress bars
- Real-time chart updates
- Toast notifications
- Loading spinners
- Form validation

### **Responsive Design**
- Mobile-friendly layout
- Collapsible sidebar
- Adaptive grid system
- Touch-friendly controls

---

## 🧪 **TESTING SCENARIOS**

### **Scenario 1: Normal Transaction**
1. Go to Fraud Detection page
2. Enter: Amount: $25.50, Merchant: "Grocery Store"
3. Click "Analyze Transaction"
4. **Expected**: Low fraud probability, "approve" status

### **Scenario 2: Suspicious Transaction**
1. Go to Fraud Detection page  
2. Enter: Amount: $5000, Merchant: "Cash Advance ATM"
3. Click "Analyze Transaction"
4. **Expected**: High fraud probability, "fraud" status

### **Scenario 3: Batch Processing**
1. Go to Batch Processing page
2. Click "Generate Mock Data"
3. Click "Process Batch"
4. **Expected**: Progress bar, results table, export option

### **Scenario 4: Dashboard Monitoring**
1. Go to Dashboard
2. Check API status indicator
3. View real-time charts
4. Check recent activity feed
5. **Expected**: Live data updates, interactive charts

---

## 🔍 **TROUBLESHOOTING**

### **API Connection Issues**
- Check if backend server is running on port 8000
- Verify no firewall blocking
- Check browser console for CORS errors

### **Frontend Issues**
- Clear browser cache
- Check browser console for JavaScript errors
- Verify all npm dependencies installed

### **Performance Issues**
- Check if both servers are running
- Monitor network requests in DevTools
- Verify API response times

---

## 📊 **EXPECTED PERFORMANCE**

- **API Response Time**: < 100ms
- **Frontend Load Time**: < 3 seconds
- **Chart Rendering**: < 1 second
- **Form Submission**: < 2 seconds
- **Batch Processing**: Depends on size

---

## 🎉 **SUCCESS INDICATORS**

✅ Backend API responds to health checks
✅ Frontend loads without errors
✅ Navigation between pages works
✅ Forms submit and show results
✅ Charts render with data
✅ Notifications appear on actions
✅ Responsive design works on mobile
✅ Dark theme with aqua accents visible
✅ Real-time updates functioning

---

**Ready to test your complete fraud detection system!** 🚀
