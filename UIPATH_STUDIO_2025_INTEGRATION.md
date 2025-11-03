# 🤖 **UiPath Studio 2025.10.0 Integration Guide**

## **📋 System Information**
- **UiPath Studio Version**: 2025.10.0 (Released: 10/6/2025)
- **License**: Community License - Automation Developer
- **Installation**: Per-user Installation
- **License Provider**: Orchestrator
- **OS**: Microsoft Windows 11 Home 64-bit 8.0.15

---

## **🔍 Understanding the Chatbot Connection**

### **How the Chatbot Currently Works**
The chatbot in your fraud detection system is **NOT connected to UiPath yet**. It's currently functioning because:

1. **React Component**: `C:\CFD\phase5_frontend\src\components\FraudChatbot.js`
2. **Backend API**: `C:\CFD\phase1_data_foundation\flask_server.py`
3. **Direct Integration**: The chatbot calls Flask APIs directly

### **UiPath Integration Architecture**
```
UiPath Studio Workflow
         ↓
   Browser Automation (Edge/Chrome)
         ↓
   React Frontend (localhost:3000)
         ↓
   Chatbot Component (Already Built)
         ↓
   Flask Backend APIs (localhost:5000)
```

**The UiPath workflow will:**
- Open the browser
- Navigate to your fraud detection system
- Interact with the existing chatbot
- Take screenshots and generate reports

---

## **🚀 Step-by-Step UiPath Studio 2025.10.0 Setup**

### **Step 1: Create New Project**

1. **Open UiPath Studio 2025.10.0**
2. **Click "New Project"**
3. **Select "Process"** (not Library or Test)
4. **Project Details:**
   - **Name**: `FraudDetectionAutomation`
   - **Location**: `C:\CFD\UiPath_Studio_Project\`
   - **Description**: `Automated fraud detection system interaction with chatbot integration`

### **Step 2: Configure Project Settings**

1. **In Project Panel** → Right-click project → **"Project Settings"**
2. **General Tab:**
   - **Project Version**: `1.0.0`
   - **Target Framework**: `.NET 6` (default for 2025.10.0)
3. **Dependencies Tab:**
   - Ensure these packages are installed:
     - `UiPath.UIAutomation.Activities` (latest)
     - `UiPath.System.Activities` (latest)
     - `UiPath.WebAPI.Activities` (latest)

### **Step 3: Create Variables**

**In Main.xaml, create these variables:**

| Variable Name | Type | Scope | Default Value |
|---------------|------|-------|---------------|
| `SystemURL` | String | Main | `"http://localhost:3000"` |
| `ApiEndpoint` | String | Main | `"http://localhost:5000"` |
| `BrowserType` | String | Main | `"Edge"` |
| `ScreenshotPath` | String | Main | `"C:\CFD\UiPath_Screenshots\"` |
| `TestTransactionAmount` | String | Main | `"1500.00"` |
| `TestMerchant` | String | Main | `"Test Store"` |
| `ChatbotResponse` | String | Main | `""` |

### **Step 4: Main Workflow Design**

**Drag these activities in sequence:**

#### **4.1 Initialize Sequence**
1. **Drag "Sequence"** → Name: `"Main Automation Sequence"`
2. **Drag "Log Message"** inside sequence
   - **Level**: `Info`
   - **Message**: `"🚀 Starting Fraud Detection Automation - UiPath Studio 2025.10.0"`

#### **4.2 Create Screenshot Directory**
1. **Drag "Create Directory"**
   - **Path**: `ScreenshotPath`

#### **4.3 Open Browser**
1. **Drag "Use Application/Browser"** (New in 2025.10.0)
   - **Application**: Click "Indicate Application" → **Select Edge Browser**
   - **URL**: `SystemURL`
   - **Browser Type**: `Edge`

#### **4.4 Inside Browser Scope - Add These Activities:**

**A. Wait for Page Load**
1. **Drag "Delay"**
   - **Duration**: `00:00:05`

**B. Take Initial Screenshot**
1. **Drag "Take Screenshot"**
   - **FileName**: `ScreenshotPath + "01_dashboard_loaded.png"`

**C. Navigate to Chatbot**
1. **Drag "Click"**
   - **Target**: Use **"Indicate on Screen"** → Click the chatbot icon
   - **Selector**: Will be auto-generated (something like `<webctrl tag='BUTTON' class='chatbot-toggle' />`)

**D. Wait for Chatbot to Open**
1. **Drag "Delay"**
   - **Duration**: `00:00:02`

**E. Take Chatbot Screenshot**
1. **Drag "Take Screenshot"**
   - **FileName**: `ScreenshotPath + "02_chatbot_opened.png"`

**F. Type in Chatbot**
1. **Drag "Type Into"**
   - **Target**: Use **"Indicate on Screen"** → Click chatbot input field
   - **Text**: `"Check system health"`
   - **Selector**: Auto-generated (like `<webctrl tag='INPUT' class='chat-input' />`)

**G. Send Message**
1. **Drag "Click"**
   - **Target**: Use **"Indicate on Screen"** → Click send button
   - **Selector**: Auto-generated

**H. Wait for Response**
1. **Drag "Delay"**
   - **Duration**: `00:00:03`

**I. Capture Response**
1. **Drag "Get Text"**
   - **Target**: Use **"Indicate on Screen"** → Select chatbot response area
   - **Output**: `ChatbotResponse`

**J. Take Final Screenshot**
1. **Drag "Take Screenshot"**
   - **FileName**: `ScreenshotPath + "03_system_health_response.png"`

**K. Log Results**
1. **Drag "Log Message"**
   - **Level**: `Info`
   - **Message**: `"✅ Automation Complete. Response: " + ChatbotResponse`

### **Step 5: Advanced Interaction Sequence**

**Add a second sequence for transaction analysis:**

1. **Drag "Sequence"** → Name: `"Transaction Analysis"`

**Inside this sequence:**

**A. Click "Analyze a transaction"**
1. **Drag "Click"**
   - **Target**: Indicate the "Analyze a transaction" button in chatbot

**B. Type Transaction Details**
1. **Drag "Type Into"**
   - **Target**: Chatbot input
   - **Text**: `"Amount: " + TestTransactionAmount + ", Merchant: " + TestMerchant`

**C. Send and Capture Analysis**
1. **Drag "Click"** → Send button
2. **Drag "Delay"** → `00:00:05`
3. **Drag "Get Text"** → Capture analysis result
4. **Drag "Take Screenshot"** → `"04_transaction_analysis.png"`

### **Step 6: Error Handling**

**Wrap main activities in Try-Catch:**

1. **Drag "Try Catch"** around main browser activities
2. **In Catch block:**
   - **Exception Type**: `System.Exception`
   - **Drag "Log Message"**
     - **Level**: `Error`
     - **Message**: `"❌ Automation failed: " + exception.Message`
   - **Drag "Take Screenshot"**
     - **FileName**: `ScreenshotPath + "error_screenshot.png"`

### **Step 7: Final Workflow Structure**

```
Main.xaml
├── Log Message: "🚀 Starting Automation"
├── Create Directory: Screenshots
├── Try Catch
│   ├── Try:
│   │   ├── Use Application/Browser (Edge)
│   │   │   ├── Delay: 5 seconds
│   │   │   ├── Take Screenshot: Dashboard
│   │   │   ├── Click: Chatbot Icon
│   │   │   ├── Delay: 2 seconds
│   │   │   ├── Take Screenshot: Chatbot Opened
│   │   │   ├── Type Into: "Check system health"
│   │   │   ├── Click: Send Button
│   │   │   ├── Delay: 3 seconds
│   │   │   ├── Get Text: Response
│   │   │   ├── Take Screenshot: Response
│   │   │   ├── Sequence: Transaction Analysis
│   │   │   │   ├── Click: "Analyze transaction"
│   │   │   │   ├── Type Into: Transaction details
│   │   │   │   ├── Click: Send
│   │   │   │   ├── Delay: 5 seconds
│   │   │   │   ├── Get Text: Analysis result
│   │   │   │   └── Take Screenshot: Analysis
│   │   │   └── Log Message: "✅ Complete"
│   └── Catch:
│       ├── Log Message: Error
│       └── Take Screenshot: Error
└── Log Message: "🎉 Automation Finished"
```

### **Step 8: Testing Your Workflow**

1. **Save the workflow** (Ctrl+S)
2. **Start your backend**: `python flask_server.py`
3. **Start your frontend**: `npm start`
4. **Click "Run"** in UiPath Studio (F5)
5. **Watch the automation**:
   - Browser opens automatically
   - Navigates to your fraud detection system
   - Interacts with chatbot
   - Takes screenshots
   - Generates reports

### **Step 9: UiPath Studio 2025.10.0 Specific Features**

**New features you can use:**

1. **AI Computer Vision**: Better element detection
2. **Enhanced Selectors**: More reliable web automation
3. **Modern Activities**: "Use Application/Browser" instead of old "Open Browser"
4. **Improved Debugging**: Better error messages and debugging tools

---

## **🔧 Troubleshooting**

### **Common Issues & Solutions:**

1. **Browser doesn't open**:
   - Check if Edge is installed
   - Try Chrome: Change `BrowserType` to `"Chrome"`

2. **Elements not found**:
   - Use "Indicate on Screen" to refresh selectors
   - Add more delays between actions

3. **Screenshots not saving**:
   - Check if `C:\CFD\UiPath_Screenshots\` directory exists
   - Verify write permissions

### **Expected Results:**
- ✅ Browser opens to fraud detection system
- ✅ Chatbot interactions work automatically
- ✅ Screenshots saved in designated folder
- ✅ System health check completed
- ✅ Transaction analysis performed
- ✅ All results logged in UiPath

**Your UiPath Studio 2025.10.0 is now fully integrated with your fraud detection system! 🚀**
