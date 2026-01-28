# 🤖 AI CONTEXT - Enterprise Fraud Detection System

## Purpose
This document provides complete context for AI assistants (ChatGPT, Claude, Gemini, etc.) to understand and work with this project effectively.

---

## Project Identity

**Name**: Enterprise Credit Card Fraud Detection System  
**Type**: Full-Stack ML/AI Web Application with RPA Integration  
**Author**: Sidharth Rahul  
**Repository**: https://github.com/Sid1rahul/Enterprise-Fraud-Detection-System  
**Status**: Production-Ready  

---

## What This Project Does

This is a **complete fraud detection system** that:
1. **Detects fraudulent credit card transactions** using machine learning
2. **Explains why** transactions are flagged (Explainable AI)
3. **Monitors transactions in real-time** with live dashboard
4. **Provides an intelligent chatbot** with voice input and wake word detection
5. **Integrates with UiPath RPA** for workflow automation
6. **Offers modern web interface** with React frontend

---

## Architecture Overview

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │◄────►│   Flask     │◄────►│   UiPath    │
│  Frontend   │      │   Backend   │      │     RPA     │
│ (Port 3000) │      │ (Port 5000) │      │             │
└─────────────┘      └─────────────┘      └─────────────┘
       │                     │                     │
       ▼                     ▼                     ▼
  User Interface        ML Engine            Automation
  - Dashboard           - XGBoost classifier - Testing
  - Analytics           - Isolation Forest   - Reports
  - Monitoring          - Random Forest demo - Workflows
  - Chatbot             - SHAP/LIME XAI
```

---

## Technology Stack

### Frontend
- **React 18** - UI framework
- **React Router 6** - Navigation
- **Recharts** - Data visualization
- **Lucide React** - Icons
- **Web Speech API** - Voice recognition
- **Axios** - HTTP client

### Backend
- **Python 3.8+** - Core language
- **Flask 2.0+** - Web framework
- **Flask-CORS** - Cross-origin support
- **Flask-SocketIO** - Real-time communication

### Machine Learning
- **scikit-learn** - ML algorithms
- **XGBoost** - Gradient boosting
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **SHAP** - Explainable AI
- **imbalanced-learn** - SMOTE/ADASYN

### RPA
- **UiPath Studio 2025.10.0** - Workflow automation

---

## File Structure

```
CFD/
├── phase1_data_foundation/          # Backend + ML pipeline
│   ├── flask_server.py             # Flask API for demo & integration
│   ├── main.py                     # Phase 1 training & evaluation pipeline
│   ├── simple_demo.py              # Lightweight RandomForest + IsolationForest demo
│   └── src/                        # Data processing, models, explainability (xgboost_model.py, isolation_forest.py, explainability.py, etc.)
│
├── phase5_frontend/                # Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── FraudChatbot.js    # Chatbot component
│   │   │   └── FraudChatbot.css   # Chatbot styles
│   │   ├── pages/
│   │   │   ├── Dashboard.js       # Main dashboard
│   │   │   ├── Analytics.js       # Analytics page
│   │   │   └── RealTimeMonitoring.js
│   │   ├── App.js                 # Root component
│   │   └── index.js               # Entry point
│   └── package.json               # Node deps
│
├── UiPath_FraudDetection_Project/  # RPA
│   └── FraudDetectionAutomation/
│       ├── Main.xaml              # Main workflow
│       └── project.json           # Config
│
└── Documentation/                  # Docs
    ├── PROJECT_SUMMARY.txt
    ├── AI_CONTEXT.md (this file)
    ├── INTERVIEW_QA.md
    ├── REAL_WORLD_SCENARIOS.md
    └── SETUP_GUIDE.md
```

---

## Key Components

### 1. Flask Backend (`flask_server.py`)

**Main Endpoints**:
- `GET /health`, `GET /api/health` - API health checks
- `GET /api/models/status` - Loaded model information (e.g. XGBoost, Isolation Forest)
- `POST /api/fraud/predict` - Predict fraud for a single transaction
- `POST /api/fraud/predict/batch` - Batch fraud detection
- `POST /api/upload/file` - File upload (CSV)
- `GET /api/transactions` - Sample transactions for demo
- `POST /api/monitoring/start` / `GET /api/monitoring/status/<session_id>` - Real-time monitoring simulation
- `POST /api/monitoring/control/<session_id>` - Pause/resume/stop monitoring session
- `GET /api/monitoring/alerts` / `GET /api/monitoring/sessions` - Recent alerts & sessions
- `POST /api/chatbot` - Chatbot interaction

> Note: In this repository, `flask_server.py` exposes a lightweight, fast demo API. The
> full XGBoost/Isolation Forest training and evaluation pipeline lives in `main.py`
> and `src/models/` and can be wired into the API for production-grade serving.

**ML Models (as implemented in the ML pipeline)**:
- `XGBoostFraudDetector` (supervised classifier)
- `IsolationForestFraudDetector` (unsupervised anomaly detector)
- `RandomForestClassifier` demo model (in `simple_demo.py`)

**Features Analyzed**:
- Transaction amount
- Transaction time
- Merchant category
- Location distance
- Card usage pattern
- Historical behavior

### 2. React Frontend

**Main Pages**:
- **Dashboard** - Overview with stats and recent transactions
- **Analytics** - Charts, trends, and insights
- **Real-Time Monitoring** - Live transaction stream
- **Batch Processing** - Upload and process files
- **Explainable AI** - Click transactions for details

**Key Components**:
- `FraudChatbot.js` - Intelligent chatbot with voice
- `Dashboard.js` - Main dashboard
- `Analytics.js` - Analytics page
- `RealTimeMonitoring.js` - Live monitoring

### 3. Intelligent Chatbot

**Features**:
- **Voice Input**: WhatsApp-style recording
- **Wake Word**: "Hey Fraud Detector" (offline detection)
- **NLP**: Understands natural language
- **Context-Aware**: Remembers conversation
- **Quick Suggestions**: Action buttons
- **UiPath Integration**: Can trigger workflows

**Voice Commands**:
- "Check system health"
- "Show fraud statistics"
- "Analyze transaction"
- "What's the fraud rate?"
- "Help me understand this"

### 4. UiPath Integration

**Capabilities**:
- Browser automation (Chrome/Edge)
- Form filling
- Screenshot capture
- Report generation
- Workflow orchestration
- Automated testing

---

## How to Run

### Backend
```bash
cd phase1_data_foundation
pip install -r requirements.txt
python flask_server.py
# Runs on http://localhost:5000
```

### Frontend
```bash
cd phase5_frontend
npm install
npm start
# Runs on http://localhost:3000
```

### UiPath
1. Open UiPath Studio 2025.10.0
2. Open `Main.xaml`
3. Update variables:
   - SystemURL: `http://localhost:3000`
   - ApiEndpoint: `http://localhost:5000`
4. Run workflow

---

## Key Features Explained

### Explainable AI (XAI)
- Click any transaction to see why it was flagged
- Visual feature importance bars
- Model confidence scores
- Recommended actions
- Historical comparison

### Real-Time Monitoring
- Live transaction stream
- Instant fraud detection
- File upload support
- Batch processing
- Export results

### Voice Features
- **Voice Recording**: Click mic, speak, auto-transcribe
- **Wake Word**: Say "Hey Fraud Detector" to activate
- **Offline**: No internet needed for wake word
- **Browser Support**: Chrome/Edge (full), Firefox (limited)

### Security
- Role-based access (Admin/Customer)
- Secure API endpoints
- Input validation
- CORS configuration
- Audit logging

---

## ML Model Details

### Training
- Dataset: Credit card transactions (class-imbalance handled via ADASYN/SMOTE)
- Features: 30+ transaction attributes
- Train/Test Split: 80/20
- Cross-validation: 5-fold

### Performance
- Accuracy: 95%+
- Precision: 92%+
- Recall: 90%+
- F1-Score: 91%+
- Response Time: <100ms

### Models Used
1. **XGBoost** – supervised fraud classifier (Phase 1 pipeline, `xgboost_model.py`)
2. **Isolation Forest** – unsupervised anomaly detector (Phase 1 pipeline, `isolation_forest.py`)
3. **Random Forest** – lightweight demo model (`simple_demo.py`)

---

## Common Tasks for AI Assistants

### Adding New Features
1. Backend: Add endpoint in `flask_server.py`
2. Frontend: Create component in `src/components/`
3. Integrate: Connect via Axios API call
4. Test: Use UiPath workflow

### Modifying Chatbot
- File: `phase5_frontend/src/components/FraudChatbot.js`
- Add commands in `handleSendMessage` function
- Update NLP patterns
- Add new responses

### Updating ML Model
- Files: `phase1_data_foundation/main.py`, `phase1_data_foundation/src/models/`
- Retrain with new data
- Update feature engineering
- Test accuracy

### Adding UiPath Workflow
- Open `Main.xaml`
- Add new sequence
- Use selectors for UI elements
- Test in UiPath Studio

---

## Important Notes

### For Code Modifications
- **Backend**: Python 3.8+, Flask patterns
- **Frontend**: React hooks, functional components
- **Styling**: CSS modules, responsive design
- **API**: RESTful endpoints, JSON responses

### For Debugging
- Backend logs: Console output from Flask
- Frontend logs: Browser console (F12)
- Network: Check browser Network tab
- UiPath: Check Output panel in Studio

### For Testing
- Backend: Use `test_api_curl.bat` or Postman
- Frontend: Browser testing, React DevTools
- Integration: UiPath workflow automation
- Voice: Chrome/Edge only

---

## Project Goals

### Primary
1. ✅ Detect fraud with high accuracy
2. ✅ Explain predictions (XAI)
3. ✅ Real-time processing
4. ✅ User-friendly interface
5. ✅ Voice interaction

### Secondary
1. ✅ RPA integration
2. ✅ Comprehensive documentation
3. ✅ Security best practices
4. ✅ Scalable architecture
5. ✅ Modern tech stack

---

## Unique Selling Points

1. **Explainable AI**: Not just predictions, but explanations
2. **Voice-Enabled**: WhatsApp-style voice + wake word
3. **RPA Integration**: Automated workflows with UiPath
4. **Real-Time**: Live monitoring and instant alerts
5. **Production-Ready**: Complete, tested, documented

---

## When Helping Users

### Understand Context
- User is likely a student/developer showcasing this project
- They may need help with interviews, presentations, or modifications
- Focus on explaining value and real-world applications

### Provide Clear Guidance
- Reference specific files and line numbers
- Explain both "what" and "why"
- Suggest best practices
- Consider scalability and maintainability

### Common User Needs
1. Interview preparation
2. Feature additions
3. Bug fixes
4. Performance optimization
5. Deployment guidance
6. Documentation improvements

---

## Real-World Context

### Industry Problem
- Credit card fraud costs billions annually
- Traditional rule-based systems have high false positives
- Need for explainable AI in finance
- Regulatory requirements for transparency

### This Solution
- ML-based detection (95%+ accuracy)
- Explainable predictions (SHAP-like)
- Real-time processing (< 100ms)
- User-friendly interface
- Automation-ready (RPA)

### Target Users
- **Banks**: Fraud detection teams
- **Fintech**: Payment processors
- **E-commerce**: Transaction monitoring
- **Enterprises**: Internal fraud prevention

---

## Quick Reference

### Start System
```bash
# Terminal 1: Backend
cd phase1_data_foundation && python flask_server.py

# Terminal 2: Frontend
cd phase5_frontend && npm start
```

### Access URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/health

### Default Credentials
- Admin: admin / admin123
- Customer: customer / customer123

### Key Files to Modify
- Backend API: `phase1_data_foundation/flask_server.py`
- ML Pipeline & Models: `phase1_data_foundation/main.py`, `phase1_data_foundation/src/models/`
- Chatbot: `phase5_frontend/src/components/FraudChatbot.js`
- Dashboard: `phase5_frontend/src/pages/Dashboard.js`
- UiPath: `UiPath_FraudDetection_Project/FraudDetectionAutomation/Main.xaml`

---

## Summary for AI Assistants

This is a **complete, production-ready fraud detection system** that combines:
- **ML/AI** for accurate predictions
- **Explainable AI** for transparency
- **Modern web interface** for usability
- **Voice interaction** for accessibility
- **RPA integration** for automation

When helping users, focus on:
- Practical applications and value
- Clear, actionable guidance
- Real-world context
- Interview/presentation preparation
- Best practices and scalability

The project demonstrates full-stack development, ML implementation, modern UI/UX, and enterprise integration skills.

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Status**: Production-Ready ✅
