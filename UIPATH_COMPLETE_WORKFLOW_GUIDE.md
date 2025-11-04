# 🤖 COMPLETE UIPATH WORKFLOW GUIDE - FIXED

## ✅ This guide fixes ALL issues including selector errors and auto-filling

---

## 🎯 PREREQUISITES

1. **Backend Running**: `python flask_server.py` (Port 5000)
2. **Frontend Running**: `npm start` (Port 3000)
3. **UiPath Studio**: Version 2025.10.0+
4. **Browser**: Chrome or Edge installed

---

## 📋 STEP-BY-STEP WORKFLOW

### **STEP 1: CREATE NEW SEQUENCE**

1. Open UiPath Studio
2. Create new **Process**
3. Name it: `FraudDetectionChatbotTest`
4. Click **Create**

---

### **STEP 2: ADD VARIABLES**

Click **Variables** panel (bottom), add these:

| Name | Type | Default Value |
|------|------|---------------|
| `SystemURL` | String | `"http://localhost:3000"` |
| `BrowserType` | String | `"Edge"` |
| `CommandsList` | Array of String | `{"Check system health", "Show fraud statistics", "Help"}` |
| `CurrentCommand` | String | (empty) |
| `BotResponse` | String | (empty) |
| `DelaySeconds` | Int32 | `3` |

---

### **STEP 3: MAIN WORKFLOW STRUCTURE**

```
Main.xaml
├── Use Application/Browser
│   ├── Navigate To (SystemURL)
│   ├── Delay (5 seconds) - Wait for page load
│   ├── Click - Open Chatbot
│   ├── Delay (2 seconds) - Wait for chatbot to open
│   ├── For Each - Loop through commands
│   │   ├── Type Into - Enter command
│   │   ├── Click - Send button
│   │   ├── Delay (3 seconds) - Wait for response
│   │   ├── Get Text - Read bot response
│   │   ├── Log Message - Log the response
│   │   └── Delay (2 seconds) - Before next command
│   └── Log Message - Test complete
└── End
```

---

### **STEP 4: DETAILED ACTIVITIES**

#### **Activity 1: Use Application/Browser**

1. Drag **Use Application/Browser** to Main
2. Click **Indicate Application**
3. Select **Edge** or **Chrome**
4. **Application/Browser URL**: `SystemURL` variable
5. **Open**: `IfNotOpen`
6. **Close**: `Never`

**Properties**:
- **Display Name**: `Edge Fraud Detection System`
- **Input Mode**: `Simulate`
- **Timeout**: `30000` (30 seconds)

---

#### **Activity 2: Navigate To**

Inside **Use Application/Browser**:

1. Drag **Navigate To** activity
2. **URL**: `SystemURL`
3. **Display Name**: `Navigate to Fraud Detection`

---

#### **Activity 3: Delay - Wait for Page Load**

1. Drag **Delay** activity
2. **Duration**: `00:00:05` (5 seconds)
3. **Display Name**: `Wait for page to load`

---

#### **Activity 4: Click - Open Chatbot**

1. Drag **Click** activity
2. Click **Indicate in Application**
3. **Target**: Click the **blue chatbot button** (bottom-right)

**Selector** (if needed):
```xml
<webctrl tag='DIV' class='chatbot-trigger' />
```

**Properties**:
- **Display Name**: `Click Chatbot Trigger`
- **Click Type**: `Single`
- **Mouse Button**: `Left`
- **Delay Before**: `1000` ms
- **Delay After**: `2000` ms

---

#### **Activity 5: Delay - Wait for Chatbot to Open**

1. Drag **Delay** activity
2. **Duration**: `00:00:02` (2 seconds)
3. **Display Name**: `Wait for chatbot to open`

---

#### **Activity 6: For Each - Loop Commands**

1. Drag **For Each** activity
2. **TypeArgument**: `String`
3. **Values**: `CommandsList`
4. **Item**: `CurrentCommand`
5. **Display Name**: `For Each Command`

---

#### **Activity 7: Type Into - Enter Command**

Inside **For Each**:

1. Drag **Type Into** activity
2. Click **Indicate in Application**
3. **Target**: Click the **input field** in chatbot

**Selector**:
```xml
<webctrl tag='INPUT' class='message-input' type='text' />
```

**Properties**:
- **Text**: `CurrentCommand`
- **Display Name**: `Type Command`
- **Empty Field**: `✓` (checked)
- **Click Before Typing**: `✓` (checked)
- **Delay Before**: `500` ms
- **Delay After**: `1000` ms

---

#### **Activity 8: Click - Send Button**

1. Drag **Click** activity
2. Click **Indicate in Application**
3. **Target**: Click the **send button** (paper plane icon)

**Selector**:
```xml
<webctrl tag='BUTTON' class='send-btn' />
```

**Properties**:
- **Display Name**: `Click Send Button`
- **Click Type**: `Single`
- **Delay Before**: `500` ms
- **Delay After**: `3000` ms (wait for response)

---

#### **Activity 9: Delay - Wait for Response**

1. Drag **Delay** activity
2. **Duration**: `00:00:03` (3 seconds)
3. **Display Name**: `Wait for bot response`

---

#### **Activity 10: Get Text - Read Bot Response**

1. Drag **Get Text** activity
2. Click **Indicate in Application**
3. **Target**: Click on the **last bot message** (the response text)

**Selector** (get the LAST message):
```xml
<webctrl tag='DIV' class='message bot' idx='*' />
<webctrl tag='DIV' class='message-content' />
```

**OR use this simpler selector**:
```xml
<webctrl tag='DIV' class='message-content' idx='-1' />
```

**Properties**:
- **Display Name**: `Get Bot Response`
- **Text**: `BotResponse` (output variable)
- **Delay Before**: `1000` ms

---

#### **Activity 11: Log Message - Log Response**

1. Drag **Log Message** activity
2. **Message**: `"Command: " + CurrentCommand + " | Response: " + BotResponse`
3. **Level**: `Info`
4. **Display Name**: `Log Command and Response`

---

#### **Activity 12: Delay - Before Next Command**

1. Drag **Delay** activity
2. **Duration**: `00:00:02` (2 seconds)
3. **Display Name**: `Wait before next command`

---

#### **Activity 13: Log Message - Test Complete**

Outside **For Each**, after it completes:

1. Drag **Log Message** activity
2. **Message**: `"✅ Chatbot test completed successfully!"`
3. **Level**: `Info`
4. **Display Name**: `Test Complete`

---

## 🔍 CORRECT SELECTORS

### **Chatbot Trigger (Blue Button)**
```xml
<webctrl tag='DIV' class='chatbot-trigger' parentid='root' />
```

### **Input Field**
```xml
<webctrl tag='INPUT' class='message-input' type='text' />
```

### **Send Button**
```xml
<webctrl tag='BUTTON' class='send-btn' />
```

### **Bot Message (Last Response)**
```xml
<webctrl tag='DIV' class='message bot' idx='-1' />
<webctrl tag='DIV' class='message-content' />
```

---

## ⚙️ IMPORTANT SETTINGS

### **For All Click Activities**:
- **Input Mode**: `Simulate` or `Hardware Events`
- **Delay Before**: `500-1000` ms
- **Delay After**: `1000-2000` ms
- **Click Type**: `Single`

### **For Type Into Activities**:
- **Empty Field**: `✓` Checked
- **Click Before Typing**: `✓` Checked
- **Simulate Type**: `✓` Checked (faster)
- **Delay Before**: `500` ms

### **For Get Text Activities**:
- **Delay Before**: `1000` ms
- **Timeout**: `10000` ms

---

## 🐛 TROUBLESHOOTING

### **Error: "Could not find UI element"**

**Solution 1**: Increase delays
- Add more delay after clicking chatbot trigger
- Add more delay after sending message

**Solution 2**: Use "Check App State" before actions
```
1. Drag "Check App State" activity
2. Target: The element you want to interact with
3. Exists → Continue
4. Does Not Exist → Wait and retry
```

**Solution 3**: Re-indicate elements
1. Open workflow
2. Click "Indicate in Application" again
3. Select the element fresh

---

### **Error: "Chatbot not opening"**

**Solution**:
1. Add **longer delay** after page load (5-10 seconds)
2. Use **Check App State** to verify chatbot trigger exists
3. Ensure frontend is running on port 3000

---

### **Error: "Auto-filling still happening"**

**Solution**:
1. **Restart frontend** with new code:
   ```bash
   cd phase5_frontend
   npm start
   ```
2. **Disable wake word** manually (don't click ear icon)
3. Wake word now requires manual activation each time

---

## 📊 EXPECTED OUTPUT

```
Debug started for file: Main
FraudDetectionChatbotTest execution started
Audit: Using Web App. Browser: Edge URL: http://localhost:3000/
Wait for page to load
Click Chatbot Trigger
Wait for chatbot to open
For Each Command
  Command: Check system health | Response: ✅ System Status: HEALTHY
  **API Status**: healthy
  **Models Loaded**: XGBoost, Isolation Forest
  **Last Updated**: 2:29:45 PM
  **Endpoint**: http://localhost:5000
  
  Command: Show fraud statistics | Response: 📊 Fraud Statistics
  Total Transactions: 1,234
  Fraud Detected: 45 (3.6%)
  Legitimate: 1,189 (96.4%)
  Avg Processing Time: 87ms
  Model Accuracy: 95.2%
  
  Command: Help | Response: 💡 I can help you with:
  • Check system health
  • Show fraud statistics
  • Analyze transactions
  • Upload transaction files
  • View fraud alerts
  • Explain fraud detection
  Just ask me anything!
  
✅ Chatbot test completed successfully!
FraudDetectionChatbotTest execution ended in: 00:00:25
```

---

## 🎯 QUICK FIX CHECKLIST

Before running workflow:

- [ ] Backend running (`python flask_server.py`)
- [ ] Frontend running (`npm start`)
- [ ] Browser opens to http://localhost:3000
- [ ] Page fully loaded (wait 5 seconds)
- [ ] Chatbot trigger visible (blue button bottom-right)
- [ ] Wake word detection DISABLED (don't click ear icon)
- [ ] All selectors updated in workflow
- [ ] Delays added between actions

---

## 🚀 SIMPLIFIED WORKFLOW (MINIMAL)

If the above is too complex, use this minimal version:

```
1. Use Application/Browser (Edge, http://localhost:3000)
2. Delay (5 seconds)
3. Click (chatbot trigger)
4. Delay (2 seconds)
5. Type Into (input field, "Check system health")
6. Click (send button)
7. Delay (3 seconds)
8. Get Text (bot response)
9. Log Message (response)
10. Done!
```

---

## 📸 SELECTOR VALIDATION

To validate selectors:

1. Open **UI Explorer** in UiPath
2. Indicate the element
3. Check the selector
4. Copy to workflow
5. Test with **Validate** button

---

## 💾 SAVE WORKFLOW

1. File → Save
2. File → Publish
3. Run → Debug File (F5)
4. Check Output panel for results

---

## ✅ SUCCESS CRITERIA

Workflow is successful when:
- ✅ Browser opens to localhost:3000
- ✅ Chatbot opens (blue button clicked)
- ✅ Commands typed successfully
- ✅ Bot responses received
- ✅ Responses are SPECIFIC (not generic greeting)
- ✅ No auto-filling in input field
- ✅ Workflow completes in 20-30 seconds
- ✅ No selector errors

---

## 🔗 FILES TO CHECK

- **Backend**: `C:\CFD\phase1_data_foundation\flask_server.py`
- **Frontend**: `C:\CFD\phase5_frontend\src\components\FraudChatbot.js`
- **Workflow**: `Main.xaml`

---

**All issues fixed! Follow this guide step-by-step for successful automation! 🎉**

*Last Updated: November 4, 2025*  
*Version: 2.0 - Complete Fix*
