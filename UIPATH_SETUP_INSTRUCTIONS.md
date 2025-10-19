# 🤖 UiPath Studio Setup Instructions for Fraud Detection System

## 🚀 **Quick Setup Guide**

### **Step 1: Start the UiPath Integration Server**
```bash
# Navigate to your project directory
cd C:\CFD

# Start the UiPath integration server
python uipath_integration_server.py
```
**Expected Output:**
```
🤖 Starting UiPath Integration Server...
📡 Server will be available at: http://localhost:8001
🔗 Connect your UiPath Studio workflows to this endpoint
💬 Chatbot integration ready for dashboard deployment
```

### **Step 2: Start Your Fraud Detection System**
```bash
# Terminal 1: Start Backend API
cd C:\CFD\phase4_rpa_integration
python api_integration/enhanced_fraud_api.py

# Terminal 2: Start Frontend
cd C:\CFD\phase5_frontend
npm start
```

### **Step 3: Import UiPath Workflow**
1. **Open UiPath Studio**
2. **Create New Project** or **Open Existing Project**
3. **Import Workflow File**: `C:\CFD\UiPath_Fraud_Detection_Workflow.xaml`
4. **Set Project Dependencies**:
   - UiPath.System.Activities
   - UiPath.UIAutomation.Activities
   - UiPath.Web.Activities

---

## 🔧 **UiPath Studio Configuration**

### **Required Activities Package**
Install these packages in UiPath Studio:
- **UiPath.Web.Activities** (latest version)
- **UiPath.System.Activities** (latest version)
- **UiPath.UIAutomation.Activities** (latest version)

### **Workflow Arguments**
Configure these input arguments in your workflow:

| Argument Name | Type | Direction | Default Value |
|---------------|------|-----------|---------------|
| `DashboardUrl` | String | In | `http://localhost:3000/dashboard` |
| `ApiEndpoint` | String | In | `http://localhost:8000` |
| `AuthToken` | String | In | `demo_token_123` |

### **Variables to Create**
Add these variables in your Main sequence:

| Variable Name | Type | Scope | Default Value |
|---------------|------|-------|---------------|
| `ChatbotResponse` | String | Sequence | `""` |
| `UserInput` | String | Sequence | `""` |
| `ApiResponse` | String | Sequence | `""` |
| `IsSystemHealthy` | Boolean | Sequence | `True` |

---

## 🎯 **Workflow Execution Steps**

### **Automatic Workflow Execution**
1. **Run the Workflow** in UiPath Studio
2. **Browser Opens** automatically to dashboard
3. **Chatbot Injects** into the page
4. **Integration Server Connects** to the chatbot
5. **Ready for Interaction** - chatbot appears in bottom-right

### **Manual Testing Steps**
1. **Click the Chatbot Icon** (orange UiPath-branded button)
2. **Type Test Messages**:
   - "Check system health"
   - "Analyze $5000 transaction at Casino"
   - "Show fraud statistics"
3. **Verify Responses** appear in chat window
4. **Check UiPath Logs** in Studio for activity tracking

---

## 🔗 **Connection Verification**

### **Test Integration Server**
Open browser and navigate to: `http://localhost:8001`

**Expected Response:**
```json
{
  "service": "UiPath Integration Server",
  "version": "1.0.0",
  "status": "running",
  "connected_systems": {
    "fraud_detection_api": "http://localhost:8000",
    "frontend_dashboard": "http://localhost:3000"
  }
}
```

### **Test Chatbot Connection**
1. Open dashboard: `http://localhost:3000/dashboard`
2. Look for **floating chatbot button** (bottom-right)
3. **UiPath indicator** should show "UiPath Connected"
4. Click chatbot and send test message

---

## 📊 **Monitoring & Debugging**

### **UiPath Studio Debugging**
- **Set Breakpoints** in workflow activities
- **Use Debug Mode** to step through execution
- **Monitor Variables** in the Variables panel
- **Check Output Panel** for log messages

### **Integration Server Logs**
Monitor the Python server console for:
```
INFO: Conversation logged: Check system health...
INFO: Workflow executed: transaction_analyzer
INFO: WebSocket connection established
```

### **Browser Developer Tools**
1. **Open DevTools** (F12)
2. **Check Console** for chatbot injection messages:
   ```
   🤖 Injecting UiPath Fraud Detection Chatbot...
   ✅ UiPath Fraud Detection Chatbot injected successfully!
   ```
3. **Network Tab** - verify API calls to `localhost:8001`

---

## 🎬 **Demo Scenarios for Presentation**

### **Scenario 1: System Health Check**
```
User Input: "Is the system healthy?"
Expected Flow:
1. UiPath captures message
2. Calls integration server API
3. Server checks fraud detection API
4. Returns system status
5. Chatbot displays: "✅ System is healthy! All models loaded."
```

### **Scenario 2: Transaction Analysis**
```
User Input: "Check $7500 at Casino for fraud"
Expected Flow:
1. UiPath parses amount and merchant
2. Calls fraud detection API
3. Gets risk score and prediction
4. Returns formatted analysis
5. Chatbot displays: "🚨 High fraud risk detected (95% probability)"
```

### **Scenario 3: Navigation Assistance**
```
User Input: "How do I upload a file?"
Expected Flow:
1. UiPath recognizes navigation intent
2. Provides step-by-step guidance
3. Can optionally navigate user to correct page
4. Chatbot displays: "📁 Go to Real-Time Monitoring page..."
```

---

## 🛠 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **Issue: Chatbot Not Appearing**
**Symptoms**: No chatbot button on dashboard
**Solutions**:
1. Check if integration server is running (`http://localhost:8001`)
2. Verify frontend is running (`http://localhost:3000`)
3. Clear browser cache and refresh
4. Check browser console for JavaScript errors

#### **Issue: UiPath Workflow Fails**
**Symptoms**: Workflow stops with error
**Solutions**:
1. **Check Browser**: Ensure Chrome is installed
2. **Verify URLs**: Confirm all endpoints are accessible
3. **Update Packages**: Ensure latest UiPath activities
4. **Check Permissions**: Run UiPath Studio as administrator

#### **Issue: API Connection Failed**
**Symptoms**: "System offline" messages in chatbot
**Solutions**:
1. **Start Backend**: `python enhanced_fraud_api.py`
2. **Check Port**: Verify port 8000 is not blocked
3. **Test Manually**: Visit `http://localhost:8000/health`
4. **Check Firewall**: Ensure local connections allowed

#### **Issue: Integration Server Not Responding**
**Symptoms**: Chatbot shows "Standalone Mode"
**Solutions**:
1. **Restart Server**: `python uipath_integration_server.py`
2. **Check Port 8001**: Ensure not in use by other applications
3. **Verify Python**: Ensure FastAPI and uvicorn installed
4. **Check Logs**: Look for error messages in server console

---

## 📁 **File Structure for UiPath Project**

```
UiPath_Fraud_Detection_Project/
├── Main.xaml                          # Import the provided workflow
├── project.json                       # UiPath project configuration
├── Config/
│   └── Config.xlsx                    # Configuration data
├── Data/
│   └── sample_transactions.csv        # Test data
└── Documentation/
    ├── README.md                      # Project documentation
    └── API_Endpoints.md               # API reference
```

---

## 🎯 **Advanced Configuration**

### **Custom Workflow Modifications**
You can enhance the workflow by adding:

1. **Error Handling**: Try-Catch blocks around API calls
2. **Data Validation**: Input validation for transaction data
3. **Logging**: Enhanced logging for audit trails
4. **Notifications**: Email alerts for critical fraud cases
5. **Scheduling**: Automated periodic health checks

### **Production Deployment**
For production use:

1. **Security**: Replace demo tokens with real authentication
2. **Monitoring**: Add application performance monitoring
3. **Scaling**: Deploy integration server with load balancing
4. **Backup**: Implement data backup and recovery
5. **Compliance**: Add audit logging and compliance features

---

## 📞 **Support & Resources**

### **Testing Endpoints**
- **Integration Server**: `http://localhost:8001`
- **Fraud Detection API**: `http://localhost:8000`
- **Frontend Dashboard**: `http://localhost:3000`

### **Key Files**
- **Chatbot Component**: `C:\CFD\phase5_frontend\src\components\FraudChatbot.js`
- **Integration Server**: `C:\CFD\uipath_integration_server.py`
- **UiPath Workflow**: `C:\CFD\UiPath_Fraud_Detection_Workflow.xaml`

### **Documentation**
- **UiPath Integration Guide**: `C:\CFD\UIPATH_INTEGRATION_GUIDE.md`
- **API Documentation**: Available at `http://localhost:8000/docs`
- **Project Workflow**: `C:\CFD\PROJECT_WORKFLOW_PRESENTATION.md`

---

## 🎉 **Success Indicators**

✅ **UiPath Studio** opens workflow without errors
✅ **Integration Server** starts and shows "running" status
✅ **Browser Opens** automatically to dashboard
✅ **Chatbot Appears** with UiPath branding
✅ **Messages Work** - responses appear in chat
✅ **API Calls** logged in integration server console
✅ **Workflow Completes** without errors in UiPath Studio

**Your UiPath Studio is now connected to the Fraud Detection System! 🚀**

This integration demonstrates the power of RPA automation combined with modern AI-powered fraud detection, perfect for your project presentation.
