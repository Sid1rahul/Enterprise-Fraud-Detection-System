# 🤖 **UiPath Manual Setup Guide - Fraud Detection System**

## **🚨 Solution for Version Compatibility Error**

Since you're getting a version compatibility error, let's create the UiPath project manually in your UiPath Studio.

---

## **📋 Step-by-Step Manual Setup**

### **Step 1: Create New Project in UiPath Studio**

1. **Open UiPath Studio**
2. **Click "Process"** (not "Open a Local Project")
3. **Enter Project Details**:
   - **Name**: `FraudDetectionAutomation`
   - **Location**: `C:\Users\[YourUsername]\Documents\UiPath\`
   - **Description**: `Fraud Detection System Automation`
4. **Click "Create"**

### **Step 2: Install Required Packages**

1. **Go to "Manage Packages"** (in the ribbon)
2. **Install these packages**:
   - ✅ **UiPath.System.Activities** (latest version)
   - ✅ **UiPath.UIAutomation.Activities** (latest version)
   - ✅ **UiPath.WebAPI.Activities** (if available)

### **Step 3: Create Main Workflow**

1. **Delete the default Main.xaml content**
2. **Drag and drop activities** in this order:

---

## **🎯 Workflow Structure to Build**

### **Main Sequence Activities**:

```
📁 Main Sequence
├── 📝 Assign: Set SystemURL = "http://localhost:3000"
├── 📄 Log Message: "🚀 Starting Fraud Detection System Automation"
├── 🌐 Open Browser (Chrome)
│   ├── 📝 Assign: Set SystemURL = "http://localhost:3000"
│   ├── ⏱️ Delay: 5 seconds
│   ├── 📄 Log Message: "✅ System Opened Successfully!"
│   └── 🖱️ Click: "Admin Access" button (if visible)
└── 📄 Log Message: "🎉 Automation Completed!"
```

---

## **🔧 Detailed Activity Configuration**

### **1. Assign Activity (Set URL)**
- **Variable Name**: `SystemURL` (String)
- **Value**: `"http://localhost:3000"`

### **2. Log Message Activity (Start)**
- **Message**: `"🚀 Starting Fraud Detection System Automation"`
- **Level**: Info

### **3. Open Browser Activity**
- **Browser Type**: Chrome
- **URL**: `SystemURL` (variable)
- **Inside Browser Scope**:

#### **3a. Delay Activity**
- **Duration**: `00:00:05` (5 seconds)

#### **3b. Log Message Activity (Success)**
- **Message**: `"✅ System Opened Successfully!"`
- **Level**: Info

#### **3c. Click Activity (Optional - Admin Login)**
- **Target**: Use UI Explorer to select "Admin Access" button
- **Selector**: `<webctrl tag='BUTTON' text='Admin Access' />`

### **4. Log Message Activity (Complete)**
- **Message**: `"🎉 Automation Completed!"`
- **Level**: Info

---

## **🎨 Visual Workflow Layout**

```
┌─────────────────────────────────────────┐
│           Main Sequence                 │
├─────────────────────────────────────────┤
│ 1. 📝 Assign: SystemURL                │
│    └── "http://localhost:3000"         │
├─────────────────────────────────────────┤
│ 2. 📄 Log: "🚀 Starting..."           │
├─────────────────────────────────────────┤
│ 3. 🌐 Open Browser: Chrome             │
│    ├── URL: SystemURL                  │
│    └── Browser Scope:                  │
│        ├── ⏱️ Delay: 5 seconds        │
│        ├── 📄 Log: "✅ Opened!"       │
│        └── 🖱️ Click: Admin Button     │
├─────────────────────────────────────────┤
│ 4. 📄 Log: "🎉 Completed!"            │
└─────────────────────────────────────────┘
```

---

## **🚀 Advanced Workflow (Optional)**

If you want to test the chatbot, add these activities inside the Browser Scope:

### **Chatbot Testing Sequence**:

```
5. 🖱️ Click: Chatbot Icon
   └── Selector: <webctrl tag='BUTTON' class='chatbot-toggle' />

6. ⏱️ Delay: 2 seconds

7. 📝 Type Into: Chat Input
   ├── Target: <webctrl tag='INPUT' class='chat-input' />
   └── Text: "Hello, test the fraud detection system"

8. ⌨️ Send Hotkey: Enter
   └── Target: Chat Input

9. ⏱️ Delay: 3 seconds

10. 📸 Take Screenshot
    └── File Path: "C:\CFD\UiPath_Screenshots\chatbot_test.png"

11. 📄 Log: "🤖 Chatbot test completed"
```

---

## **📊 Variables to Create**

In the **Variables** panel, create these:

| Name | Type | Default Value | Scope |
|------|------|---------------|-------|
| `SystemURL` | String | `"http://localhost:3000"` | Main |
| `IsLoggedIn` | Boolean | `False` | Main |
| `ChatMessage` | String | `"Hello"` | Main |

---

## **🔍 Selectors for UI Elements**

### **Admin Login Button**:
```xml
<webctrl tag='BUTTON' text='Admin Access' />
```

### **Chatbot Icon**:
```xml
<webctrl tag='BUTTON' class='chatbot-toggle' />
```

### **Chat Input Field**:
```xml
<webctrl tag='INPUT' class='chat-input' />
```

### **Fraud Analysis Menu**:
```xml
<webctrl tag='A' text='Fraud Analysis' />
```

---

## **⚙️ Before Running the Workflow**

### **Prerequisites**:
1. **Start your fraud detection system**:
   ```bash
   # Terminal 1: Backend
   cd C:\CFD\phase1_data_foundation
   python app.py
   
   # Terminal 2: Frontend
   cd C:\CFD\phase5_frontend
   npm start
   ```

2. **Verify system is running**:
   - Open browser to `http://localhost:3000`
   - Ensure the system loads properly

3. **Create screenshots folder**:
   ```bash
   mkdir C:\CFD\UiPath_Screenshots
   ```

---

## **▶️ Running Your Workflow**

1. **Click "Run"** (F5) in UiPath Studio
2. **Watch the automation**:
   - Chrome opens to your fraud detection system
   - System loads automatically
   - Logs appear in Output panel
3. **Check results**:
   - Screenshots saved (if configured)
   - All log messages appear
   - No errors in execution

---

## **🎯 Expected Output**

### **Console Logs**:
```
🚀 Starting Fraud Detection System Automation
✅ System Opened Successfully!
🤖 Chatbot test completed (if added)
🎉 Automation Completed!
```

### **Visual Results**:
- ✅ Chrome browser opens
- ✅ Fraud detection system loads
- ✅ Admin login (if configured)
- ✅ Chatbot interaction (if added)
- ✅ Screenshots saved

---

## **🔧 Troubleshooting**

### **Common Issues**:

**1. "Element not found"**:
- Use **UI Explorer** to get correct selectors
- Add more **Delay** activities
- Check if system is running

**2. "Browser not opening"**:
- Install Chrome browser
- Check if port 3000 is available
- Verify system URL is correct

**3. "Timeout errors"**:
- Increase timeout in activities
- Add more delays between actions
- Check system performance

### **Debugging Tips**:
1. **Use Debug Mode**: Click "Debug" instead of "Run"
2. **Add Breakpoints**: Click left margin of activities
3. **Check Variables**: Use "Locals" panel
4. **Slow Down**: Add more delays if needed

---

## **🎉 Success Indicators**

Your automation is working when you see:
- ✅ Chrome opens to localhost:3000
- ✅ Fraud detection system loads
- ✅ All log messages in Output panel
- ✅ No error messages
- ✅ Screenshots saved (if configured)

**This manual approach will work with any version of UiPath Studio! 🚀**

---

## **📈 Next Steps**

Once basic automation works:
1. **Add more test scenarios**
2. **Include error handling** (Try-Catch)
3. **Add data-driven testing**
4. **Create reusable workflows**
5. **Schedule with UiPath Orchestrator**

**Your fraud detection system will be fully automated! 🎊**
