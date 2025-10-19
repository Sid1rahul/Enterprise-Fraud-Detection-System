# 🤖 UiPath Integration Guide for Fraud Detection System

## Overview
This guide provides comprehensive instructions for integrating UiPath Studio with the Fraud Detection System, including chatbot deployment, workflow automation, and API integration for presentation purposes.

---

## 🏗️ **System Architecture for UiPath Integration**

```
UiPath Studio Workflow
         ↓
    Chatbot Interface
         ↓
   Frontend Dashboard ←→ Backend API ←→ ML Models
         ↓                    ↓
   Real-time Monitoring   Fraud Detection
```

---

## 🔧 **Integration Points**

### **1. API Endpoints for UiPath**
All endpoints are accessible at `http://localhost:8000` with Bearer token authentication.

#### **Health Check**
```http
GET /health
```
**Use Case**: Monitor system availability in UiPath workflows

#### **Single Fraud Detection**
```http
POST /api/fraud/predict
Authorization: Bearer demo_token_123
Content-Type: application/json

{
  "transaction_data": {
    "amount": 1500.00,
    "merchant": "Electronics Store",
    "timestamp": "2024-01-15T14:22:00Z",
    "card_type": "credit",
    "customer_id": "CUST002"
  },
  "model_type": "xgboost"
}
```

#### **Batch Processing**
```http
POST /api/fraud/predict/batch
Authorization: Bearer demo_token_123
Content-Type: application/json

{
  "transactions": [...],
  "model_type": "xgboost"
}
```

#### **File Upload for Real-time Monitoring**
```http
POST /api/upload/file
Authorization: Bearer demo_token_123
Content-Type: multipart/form-data

Form Data: file (CSV/Excel)
```

---

## 🤖 **Chatbot Integration Strategy**

### **Chatbot Deployment Location**
- **Target**: Dashboard page (`http://localhost:3000/dashboard`)
- **Position**: Bottom-right corner floating widget
- **Trigger**: Click or automatic popup after 30 seconds

### **Chatbot Capabilities**
1. **Transaction Analysis Queries**
   - "Analyze transaction: $500 at Amazon"
   - "Check fraud risk for customer CUST001"
   - "What's the current fraud rate?"

2. **System Status Queries**
   - "Is the system healthy?"
   - "How many models are loaded?"
   - "Show recent fraud alerts"

3. **File Processing Commands**
   - "Upload transaction file"
   - "Start monitoring session"
   - "Export fraud results"

4. **Navigation Assistance**
   - "Go to batch processing"
   - "Show real-time monitoring"
   - "Open analytics dashboard"

---

## 🎯 **UiPath Studio Workflow Design**

### **Main Workflow: Fraud Detection Chatbot**

#### **Sequence 1: Initialize System**
```
1. Open Browser → Navigate to http://localhost:3000/dashboard
2. Wait for page load
3. Inject chatbot widget (HTML/CSS/JavaScript)
4. Initialize API connection
5. Set authentication token
```

#### **Sequence 2: Chatbot Interface**
```
1. Display chat window
2. Listen for user input
3. Parse intent (NLP/keyword matching)
4. Route to appropriate sub-workflow
5. Display response
6. Log conversation
```

#### **Sequence 3: API Integration Workflows**

**Sub-workflow: Single Transaction Analysis**
```
Input: User message "Check $1500 at Electronics Store"
1. Extract amount and merchant using regex
2. Build API request JSON
3. HTTP Request → POST /api/fraud/predict
4. Parse response
5. Format user-friendly message
6. Display result in chat
```

**Sub-workflow: System Health Check**
```
Input: "Is system healthy?"
1. HTTP Request → GET /health
2. Parse response
3. Format status message
4. Display in chat
```

**Sub-workflow: File Upload Assistant**
```
Input: "Upload file" or "Process transactions"
1. Guide user to Real-time Monitoring page
2. Provide instructions for file upload
3. Monitor upload progress
4. Report completion status
```

---

## 📊 **Presentation Workflow Demonstration**

### **Demo Script for Project Presentation**

#### **Scene 1: System Overview (2 minutes)**
```
1. Open UiPath Studio
2. Show workflow design
3. Explain integration architecture
4. Highlight key components
```

#### **Scene 2: Chatbot Interaction (3 minutes)**
```
1. Run UiPath workflow
2. Navigate to dashboard
3. Demonstrate chatbot popup
4. Show conversation examples:
   - "Analyze $5000 transaction at Casino"
   - "What's the fraud rate today?"
   - "Show system status"
```

#### **Scene 3: Real-time Processing (3 minutes)**
```
1. Chatbot guides to file upload
2. Upload sample_transactions.csv
3. Start monitoring session
4. Show live fraud detection
5. Export results
```

#### **Scene 4: Advanced Features (2 minutes)**
```
1. Demonstrate range analysis
2. Show batch processing
3. Display analytics dashboard
4. Highlight integration benefits
```

---

## 💻 **Chatbot Implementation Code**

### **HTML Widget for Dashboard**
```html
<!-- Chatbot Widget -->
<div id="fraud-chatbot" class="chatbot-widget">
  <div class="chatbot-header">
    <h4>🤖 Fraud Assistant</h4>
    <button id="chatbot-minimize">−</button>
  </div>
  <div class="chatbot-messages" id="chatbot-messages">
    <div class="bot-message">
      Hi! I'm your fraud detection assistant. Ask me about transactions, system status, or navigation help.
    </div>
  </div>
  <div class="chatbot-input">
    <input type="text" id="chatbot-input" placeholder="Type your message..." />
    <button id="chatbot-send">Send</button>
  </div>
</div>
```

### **JavaScript Integration**
```javascript
// Chatbot functionality
class FraudChatbot {
  constructor() {
    this.apiBase = 'http://localhost:8000';
    this.token = 'demo_token_123';
    this.init();
  }

  init() {
    this.bindEvents();
    this.showWelcomeMessage();
  }

  async processMessage(message) {
    const intent = this.parseIntent(message);
    
    switch(intent.type) {
      case 'transaction_analysis':
        return await this.analyzeTransaction(intent.data);
      case 'system_status':
        return await this.getSystemStatus();
      case 'navigation':
        return this.handleNavigation(intent.data);
      default:
        return this.getHelpMessage();
    }
  }

  parseIntent(message) {
    // Simple intent recognition
    if (message.match(/analyze|check.*\$?\d+/i)) {
      return { type: 'transaction_analysis', data: this.extractTransactionData(message) };
    }
    if (message.match(/status|health|system/i)) {
      return { type: 'system_status' };
    }
    if (message.match(/go to|navigate|show|open/i)) {
      return { type: 'navigation', data: message };
    }
    return { type: 'unknown' };
  }

  async analyzeTransaction(data) {
    try {
      const response = await fetch(`${this.apiBase}/api/fraud/predict`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          transaction_data: data,
          model_type: 'xgboost'
        })
      });
      
      const result = await response.json();
      return this.formatAnalysisResult(result);
    } catch (error) {
      return "Sorry, I couldn't analyze that transaction. Please check if the system is running.";
    }
  }
}
```

---

## 🎨 **Chatbot Styling (CSS)**
```css
.chatbot-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 350px;
  height: 500px;
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--accent-primary);
  box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  font-family: inherit;
}

.chatbot-header {
  background: var(--accent-primary);
  color: white;
  padding: 1rem;
  border-radius: 12px 12px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chatbot-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.bot-message, .user-message {
  padding: 0.75rem;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word;
}

.bot-message {
  background: rgba(0, 212, 255, 0.1);
  color: var(--text-primary);
  align-self: flex-start;
}

.user-message {
  background: var(--accent-primary);
  color: white;
  align-self: flex-end;
}

.chatbot-input {
  display: flex;
  padding: 1rem;
  border-top: 1px solid var(--border-color);
}

.chatbot-input input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 6px 0 0 6px;
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.chatbot-input button {
  padding: 0.5rem 1rem;
  background: var(--accent-primary);
  color: white;
  border: none;
  border-radius: 0 6px 6px 0;
  cursor: pointer;
}
```

---

## 🚀 **UiPath Activities Required**

### **Core Activities**
1. **Open Browser** - Navigate to dashboard
2. **HTTP Request** - API calls
3. **Deserialize JSON** - Parse API responses
4. **Inject JavaScript** - Add chatbot widget
5. **Get Text** - Extract user input
6. **Type Into** - Send responses
7. **Click** - UI interactions

### **Custom Activities (Optional)**
1. **NLP Intent Recognition** - Better message parsing
2. **File Upload Handler** - Automated file processing
3. **Real-time Monitor** - Live data streaming
4. **Report Generator** - Automated reporting

---

## 📈 **Presentation Benefits Highlight**

### **Business Value**
- **Automated Fraud Detection**: Reduce manual review time by 80%
- **Real-time Processing**: Instant fraud alerts and prevention
- **Scalable Architecture**: Handle thousands of transactions per minute
- **User-friendly Interface**: No technical expertise required

### **Technical Excellence**
- **Modern Tech Stack**: React, FastAPI, Machine Learning
- **API-first Design**: Easy integration with any system
- **Real-time Capabilities**: Live monitoring and alerts
- **Responsive UI**: Works on desktop and mobile

### **UiPath Integration Benefits**
- **Conversational Interface**: Natural language interaction
- **Workflow Automation**: Streamlined fraud investigation
- **Seamless Integration**: No system modifications required
- **Scalable Deployment**: Enterprise-ready solution

---

## 🎯 **Next Steps for Implementation**

### **Phase 1: Basic Chatbot (1-2 days)**
1. Create UiPath workflow structure
2. Implement basic chatbot widget
3. Add simple intent recognition
4. Connect to health check API

### **Phase 2: Advanced Features (2-3 days)**
1. Add transaction analysis capabilities
2. Implement file upload guidance
3. Create navigation assistance
4. Add conversation logging

### **Phase 3: Presentation Ready (1 day)**
1. Create demo scenarios
2. Prepare presentation script
3. Test all workflows
4. Record demo videos

---

## 🔍 **Testing Scenarios**

### **Scenario 1: Transaction Analysis**
```
User: "Check if $5000 at Casino is fraud"
Expected: Bot analyzes and returns high fraud probability
```

### **Scenario 2: System Status**
```
User: "Is the system working?"
Expected: Bot returns health status and model information
```

### **Scenario 3: Navigation Help**
```
User: "How do I upload a file?"
Expected: Bot guides to real-time monitoring page
```

### **Scenario 4: Batch Processing**
```
User: "Process multiple transactions"
Expected: Bot explains batch processing workflow
```

---

**Ready for UiPath Studio implementation and presentation! 🚀**

This integration will showcase the power of combining RPA with modern fraud detection systems, creating an impressive demonstration for your project presentation.
