# 🔄 Real-Time Transaction Monitoring System

## Overview
The Real-Time Monitoring feature allows you to upload CSV/Excel files containing transaction data and monitor them for fraud detection in real-time. This system simulates live transaction processing with configurable speed and provides comprehensive fraud detection analytics.

## 🚀 **Getting Started**

### 1. **Access the Real-Time Monitoring Page**
- Navigate to **Real-Time Monitoring** in the sidebar
- Or go directly to: `http://localhost:3000/real-time-monitoring`

### 2. **Upload Transaction Data**
- **Supported Formats**: CSV (.csv), Excel (.xlsx, .xls)
- **Required Columns**: Amount, Merchant, Customer_ID, Timestamp, Card_Type
- **Optional Columns**: Any additional transaction features

### 3. **Sample Data File**
A sample CSV file is provided at: `C:\CFD\sample_transactions.csv`

---

## 📊 **Features**

### **File Upload & Processing**
- ✅ **Drag & Drop Interface**: Easy file upload with visual feedback
- ✅ **File Validation**: Automatic format validation and error handling
- ✅ **Data Preview**: Shows first 5 rows and column information
- ✅ **Progress Indicators**: Real-time upload and parsing feedback

### **Real-Time Monitoring**
- ✅ **Live Transaction Stream**: Process transactions at configurable speeds
- ✅ **Fraud Detection**: Real-time risk scoring and fraud identification
- ✅ **Processing Controls**: Start, pause, resume, and stop monitoring
- ✅ **Speed Control**: Adjust processing speed from 100ms to 3000ms per transaction

### **Analytics Dashboard**
- ✅ **Live Statistics**: Total processed, fraud detected, fraud rate, processing time
- ✅ **Risk Visualization**: Color-coded risk indicators and progress bars
- ✅ **Transaction History**: Scrollable list of recent transactions
- ✅ **Fraud Alerts**: Dedicated panel for high-risk transactions

### **Data Export**
- ✅ **CSV Export**: Export detected fraud cases with full details
- ✅ **Filtering Options**: Show fraud only, filter by risk level
- ✅ **Time-based Filtering**: Filter by time ranges

---

## 🎯 **How to Use**

### **Step 1: Upload Data**
1. Click the upload area or drag a CSV/Excel file
2. Wait for file validation and parsing
3. Review the file preview and transaction count

### **Step 2: Configure Monitoring**
1. Adjust processing speed using the slider (default: 1000ms)
2. Set any filters (fraud only, risk level, etc.)
3. Click **"Start Monitoring"**

### **Step 3: Monitor Real-Time**
1. Watch the live transaction stream
2. Monitor fraud detection statistics
3. Review fraud alerts as they appear
4. Use pause/resume controls as needed

### **Step 4: Export Results**
1. Click **"Export Fraud Cases"** to download detected fraud
2. Use filters to customize the export data
3. Save results for further analysis

---

## 🔧 **Backend API Endpoints**

### **File Upload**
```http
POST /api/upload/file
Content-Type: multipart/form-data
Authorization: Bearer demo_token_123

Body: FormData with 'file' field
```

### **Start Monitoring**
```http
POST /api/monitoring/start
Content-Type: multipart/form-data
Authorization: Bearer demo_token_123

Body: 
- file_id: string
- processing_speed_ms: integer
```

### **Monitor Status**
```http
GET /api/monitoring/status/{session_id}
Authorization: Bearer demo_token_123
```

### **Control Monitoring**
```http
POST /api/monitoring/control/{session_id}
Content-Type: multipart/form-data
Authorization: Bearer demo_token_123

Body:
- action: "pause" | "resume" | "stop"
```

### **Get Fraud Alerts**
```http
GET /api/monitoring/alerts?limit=50
Authorization: Bearer demo_token_123
```

---

## 📁 **File Format Requirements**

### **CSV Format Example:**
```csv
Amount,Merchant,Customer_ID,Timestamp,Card_Type
25.50,Coffee Shop,CUST001,2024-01-15T08:30:00Z,credit
1500.00,Electronics Store,CUST002,2024-01-15T14:22:00Z,credit
75.25,Gas Station,CUST003,2024-01-15T09:15:00Z,debit
```

### **Required Columns:**
- **Amount**: Transaction amount (numeric)
- **Merchant**: Merchant name (string)
- **Customer_ID**: Customer identifier (string)
- **Timestamp**: Transaction timestamp (ISO format)
- **Card_Type**: Type of card (credit/debit/prepaid)

### **Optional Columns:**
- Any additional features will be preserved and used in analysis

---

## 🚨 **Fraud Detection Logic**

### **Risk Scoring Factors:**
1. **Transaction Amount**:
   - Amounts > $1,000: +0.3 risk
   - Amounts > $5,000: +0.4 additional risk

2. **Merchant Type**:
   - High-risk merchants (ATM, Casino, Cash Advance): +0.5 risk
   - Normal merchants: baseline risk

3. **Random Variation**: ±0.1 for realistic simulation

### **Risk Levels:**
- **Low Risk**: 0.0 - 0.3 (Green)
- **Medium Risk**: 0.3 - 0.7 (Yellow)
- **High Risk**: 0.7 - 1.0 (Red)

### **Fraud Threshold:**
- Transactions with risk score > 0.7 are flagged as fraud
- Critical alerts for risk score > 0.9

---

## 🎨 **UI Features**

### **Visual Indicators**
- **Green**: Safe transactions (✅)
- **Red**: Fraudulent transactions (❌)
- **Progress Bars**: Real-time risk visualization
- **Animations**: Smooth transitions and updates

### **Interactive Elements**
- **Hover Effects**: Enhanced user experience
- **Real-time Updates**: Live data streaming
- **Responsive Design**: Works on all screen sizes
- **Toast Notifications**: Instant feedback

### **Dark Aqua Theme**
- Consistent with the overall application design
- High contrast for better visibility
- Modern card-based layout

---

## 🧪 **Testing Scenarios**

### **Scenario 1: Normal Processing**
1. Upload the sample CSV file
2. Start monitoring with default speed (1000ms)
3. Watch normal transactions flow through
4. Observe low fraud rate (10-20%)

### **Scenario 2: High-Risk Detection**
1. Upload file with high-value transactions
2. Start monitoring with fast speed (100ms)
3. Watch for fraud alerts on large amounts
4. Export fraud cases for analysis

### **Scenario 3: Speed Control**
1. Start monitoring with slow speed (3000ms)
2. Pause and resume monitoring
3. Change speed during processing
4. Stop monitoring mid-stream

### **Scenario 4: Filtering & Export**
1. Enable "Show Fraud Only" filter
2. Set risk level to "High Risk"
3. Monitor filtered results
4. Export filtered fraud cases

---

## 🔍 **Troubleshooting**

### **File Upload Issues**
- **Error**: "Unsupported file format"
  - **Solution**: Use only CSV, XLSX, or XLS files
- **Error**: "File parsing failed"
  - **Solution**: Check file format and column names

### **Monitoring Issues**
- **Error**: "Session not found"
  - **Solution**: Re-upload file and start new session
- **Error**: "No transactions to display"
  - **Solution**: Check file upload and data parsing

### **Performance Issues**
- **Slow Processing**: Increase processing speed interval
- **Memory Issues**: Use smaller files or restart browser
- **Network Errors**: Check backend API connection

---

## 📈 **Performance Metrics**

### **Expected Performance**
- **File Upload**: < 5 seconds for files up to 10MB
- **Processing Speed**: 100ms - 3000ms per transaction
- **Real-time Updates**: Every 2 seconds
- **Fraud Detection**: < 50ms per transaction

### **Scalability**
- **File Size**: Up to 10,000 transactions recommended
- **Concurrent Sessions**: Multiple monitoring sessions supported
- **Memory Usage**: Optimized for browser performance

---

## 🎉 **Success Indicators**

✅ **File uploads successfully and shows preview**
✅ **Monitoring starts and processes transactions**
✅ **Fraud alerts appear for high-risk transactions**
✅ **Statistics update in real-time**
✅ **Export functionality works correctly**
✅ **Controls (pause/resume/stop) function properly**
✅ **Filters apply correctly to transaction stream**
✅ **Responsive design works on mobile devices**

---

**Ready to monitor transactions in real-time!** 🚀

For technical support or feature requests, check the API documentation or contact the development team.
