# 🤖 **UiPath Studio Project - Fraud Detection System Integration**

## **📁 How to Import This Project into UiPath Studio**

### **Step 1: Copy the Project Folder**
1. Copy the entire `UiPath_Studio_Project` folder to your UiPath projects directory
2. Default location: `C:\Users\[YourUsername]\Documents\UiPath\`
3. Final path should be: `C:\Users\[YourUsername]\Documents\UiPath\UiPath_Studio_Project\`

### **Step 2: Open in UiPath Studio**
1. **Open UiPath Studio**
2. Click **"Open a Local Project"**
3. Navigate to the `UiPath_Studio_Project` folder
4. Select the `project.json` file
5. Click **"Open"**

### **Step 3: Install Dependencies**
UiPath Studio will automatically prompt you to install required packages:
- ✅ **UiPath.Excel.Activities** (v2.20.1)
- ✅ **UiPath.Mail.Activities** (v1.18.2)
- ✅ **UiPath.System.Activities** (v23.10.3)
- ✅ **UiPath.UIAutomation.Activities** (v23.10.5)
- ✅ **UiPath.WebAPI.Activities** (v1.18.0)

Click **"Restore"** to install all dependencies.

---

## **🎯 Project Structure**

```
UiPath_Studio_Project/
├── project.json                 # Project configuration
├── Main.xaml                   # Main workflow entry point
├── ChatbotInteraction.xaml     # Chatbot testing workflow
├── FraudAnalysis.xaml          # Batch processing workflow
└── README.md                   # This file
```

---

## **🚀 Workflows Included**

### **1. Main.xaml - Primary Workflow**
**Purpose**: Opens the fraud detection system and performs admin login

**What it does**:
- 🌐 Opens Chrome browser to `http://localhost:3000`
- 🔐 Automatically clicks "Admin Access" demo login
- ⏱️ Waits for system to load
- 📝 Logs all activities for monitoring

**Variables**:
- `chatbotUrl`: System URL (http://localhost:3000)
- `apiEndpoint`: API endpoint (http://localhost:5000/api)
- `isConnected`: Connection status check

### **2. ChatbotInteraction.xaml - Chatbot Testing**
**Purpose**: Tests the intelligent chatbot with various queries

**What it does**:
- 🤖 Clicks the chatbot icon to open
- 💬 Tests multiple queries:
  - "Hello" (greeting test)
  - "Check $500 transaction at Amazon" (fraud analysis)
  - "Show system status" (system query)
  - "Thank you" (gratitude response)
  - "Goodbye" (farewell response)
- 📸 Takes screenshots of each response
- 📊 Logs all interactions

**Variables**:
- `chatbotMessage`: Current message being sent
- `testQueries`: Array of test messages
- `chatbotVisible`: Chatbot visibility status

### **3. FraudAnalysis.xaml - Batch Processing**
**Purpose**: Automates fraud analysis with CSV file upload

**What it does**:
- 📁 Navigates to Fraud Analysis page
- 📤 Uploads CSV file (`C:\CFD\datasets\ecommerce_transactions_5k.csv`)
- ⚙️ Starts batch processing
- ⏳ Waits for results
- 📊 Takes screenshot of results
- 💾 Exports results to CSV

**Variables**:
- `csvFilePath`: Path to transaction file
- `apiResponse`: API response data
- `fraudResults`: Processing results
- `fileUploaded`: Upload success status

---

## **⚙️ Prerequisites**

### **Before Running the Workflows**:

1. **Start Your Fraud Detection System**:
   ```bash
   # Terminal 1: Start the backend API
   cd C:\CFD\phase1_data_foundation
   python app.py
   
   # Terminal 2: Start the frontend
   cd C:\CFD\phase5_frontend
   npm start
   ```

2. **Verify System is Running**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

3. **Create Screenshots Folder**:
   ```bash
   mkdir C:\CFD\UiPath_Screenshots
   ```

4. **Ensure CSV Files Exist**:
   - `C:\CFD\datasets\ecommerce_transactions_5k.csv`
   - `C:\CFD\datasets\banking_transactions_10k.csv`
   - `C:\CFD\datasets\retail_transactions_7k.csv`

---

## **▶️ How to Run**

### **Option 1: Run Main Workflow**
1. Open `Main.xaml` in UiPath Studio
2. Click **"Run"** (F5)
3. Watch as it opens your fraud detection system
4. Check the **Output** panel for logs

### **Option 2: Run Individual Workflows**
1. **For Chatbot Testing**: Open `ChatbotInteraction.xaml` → Run
2. **For Fraud Analysis**: Open `FraudAnalysis.xaml` → Run

### **Option 3: Run All Workflows in Sequence**
1. Open `Main.xaml`
2. Add **Invoke Workflow File** activities
3. Point to `ChatbotInteraction.xaml` and `FraudAnalysis.xaml`
4. Run the complete automation suite

---

## **📊 Expected Results**

### **Successful Run Will**:
- ✅ Open fraud detection system in Chrome
- ✅ Login as admin automatically
- ✅ Test chatbot with 5 different queries
- ✅ Upload and process transaction CSV file
- ✅ Generate screenshots in `C:\CFD\UiPath_Screenshots\`
- ✅ Export fraud analysis results
- ✅ Complete with success logs

### **Screenshots Generated**:
- `chatbot_response_YYYYMMDD_HHMMSS.png` (5 files)
- `fraud_results_YYYYMMDD_HHMMSS.png` (1 file)

### **Log Messages**:
```
🚀 Starting Fraud Detection Chatbot Integration Workflow
📄 Loading Fraud Detection System Dashboard...
🔐 Attempting Admin Login...
✅ Successfully logged in as Admin
🤖 Starting Chatbot Interaction Tests
💬 Testing query: Hello
✅ Query completed: Hello
🔍 Starting Fraud Analysis Workflow
📁 Uploading transaction file: C:\CFD\datasets\ecommerce_transactions_5k.csv
⚙️ Fraud analysis processing started...
📊 Fraud analysis results available
💾 Results exported successfully
🎉 Fraud Detection Chatbot Integration Workflow Completed Successfully!
```

---

## **🔧 Troubleshooting**

### **Common Issues & Solutions**:

**1. "Element not found" errors**:
- ✅ Ensure your fraud detection system is running
- ✅ Check that URLs are correct (localhost:3000)
- ✅ Verify Chrome browser is installed

**2. "File not found" errors**:
- ✅ Check CSV file paths in `FraudAnalysis.xaml`
- ✅ Create the screenshots directory
- ✅ Verify dataset files exist

**3. "Timeout" errors**:
- ✅ Increase timeout values in Target elements
- ✅ Add more delay activities if system is slow
- ✅ Check internet connection

**4. "Permission denied" errors**:
- ✅ Run UiPath Studio as Administrator
- ✅ Check file/folder permissions
- ✅ Ensure antivirus isn't blocking

### **Debugging Tips**:
1. **Use Debug Mode**: Click "Debug" instead of "Run"
2. **Add Breakpoints**: Click left margin in workflow
3. **Check Variables**: Use "Locals" panel during debug
4. **Slow Down**: Add more delays if system is slow
5. **Update Selectors**: Use UiPath's selector editor if elements change

---

## **🎯 Customization Options**

### **Modify for Your Environment**:

1. **Change URLs**:
   ```xml
   <!-- In Main.xaml, update the Assign activity -->
   <InArgument x:TypeArguments="x:String">"http://your-domain:3000"</InArgument>
   ```

2. **Add More Test Queries**:
   ```xml
   <!-- In ChatbotInteraction.xaml, update the ForEach Values -->
   Values="[{&quot;Hello&quot;, &quot;Your custom query&quot;, &quot;Another test&quot;}]"
   ```

3. **Use Different CSV Files**:
   ```xml
   <!-- In FraudAnalysis.xaml, update csvFilePath -->
   <InArgument x:TypeArguments="x:String">"C:\Your\Custom\File.csv"</InArgument>
   ```

4. **Change Screenshot Location**:
   ```xml
   <!-- Update FilePath in TakeScreenshot activities -->
   FilePath="[&quot;C:\Your\Custom\Path\screenshot.png&quot;]"
   ```

---

## **📈 Advanced Usage**

### **Integration with Other Systems**:
1. **Email Results**: Add Mail activities to send reports
2. **Database Logging**: Use Database activities to log results
3. **API Integration**: Use HTTP Request activities for external APIs
4. **Scheduled Runs**: Use UiPath Orchestrator for automation

### **Performance Optimization**:
1. **Parallel Processing**: Use Parallel activities for multiple workflows
2. **Error Handling**: Add more Try-Catch blocks
3. **Retry Logic**: Use Retry Scope for unreliable elements
4. **Resource Management**: Close browsers and clean up files

---

## **🎉 Success Indicators**

Your UiPath automation is working perfectly when you see:
- ✅ Chrome opens to your fraud detection system
- ✅ Admin login happens automatically
- ✅ Chatbot responds to all test queries
- ✅ CSV file uploads and processes successfully
- ✅ Screenshots are saved to the specified folder
- ✅ All log messages appear in Output panel
- ✅ No error messages in the execution

**Congratulations! Your fraud detection system is now fully automated with UiPath! 🚀**
