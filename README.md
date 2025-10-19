# 🚀 **Enterprise Credit Card Fraud Detection System**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![UiPath](https://img.shields.io/badge/UiPath-RPA-orange.svg)](https://uipath.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 **Project Overview**
A **production-ready, enterprise-grade credit card fraud detection system** featuring:
- 🤖 **Advanced Machine Learning** (XGBoost, Random Forest, Neural Networks)
- ⚡ **Real-Time Processing** with live transaction monitoring
- 🔐 **Role-Based Security** (Admin vs Customer access)
- 📊 **Interactive Dashboard** with explainable AI
- 💬 **Intelligent Chatbot** for user assistance
- 🔄 **UiPath Integration** for workflow automation
- 🎨 **Modern UI/UX** with fixed navigation and responsive design

## 🏗️ **System Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │   Flask Backend │    │  UiPath RPA     │
│   (Port 3000)   │◄──►│   (Port 5000)   │◄──►│  Automation     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Interface│    │  ML Models &    │    │  Browser        │
│   • Dashboard   │    │  APIs           │    │  Automation     │
│   • Analytics   │    │  • XGBoost      │    │  • Screenshots  │
│   • Monitoring  │    │  • Fraud API    │    │  • Form Filling │
│   • Chatbot     │    │  • File Upload  │    │  • Reporting    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 **Project Structure**
```
CFD/
├── 📊 phase1_data_foundation/       # Backend API & ML Models
│   ├── flask_server.py             # Main Flask application
│   ├── fraud_detection_model.py    # ML model implementation
│   └── utils/                      # Utility functions
├── 🎨 phase5_frontend/             # React Frontend Application  
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   ├── pages/                  # Main application pages
│   │   └── utils/                  # Frontend utilities
│   └── package.json               # Node.js dependencies
├── 🤖 UiPath_Workflows/            # RPA Automation Files
│   ├── Main.xaml                  # Primary workflow
│   └── project.json               # UiPath project config
├── 📚 Documentation/               # Comprehensive docs
│   ├── COMPREHENSIVE_PROJECT_DOCUMENTATION.md
│   └── UIPATH_CONNECTION_SUMMARY.md
└── 📋 README.md                   # This file
```

## ✨ **Key Features**

### 🔍 **Explainable AI**
- **SHAP-like Visualizations**: Click any transaction to see why it was flagged
- **Feature Importance**: Visual bars showing impact of each factor
- **Model Confidence**: AI confidence levels for each prediction
- **Recommended Actions**: Clear guidance on next steps

### 🖥️ **Modern UI/UX**
- **Fixed Navigation**: Sidebar stays in place while scrolling
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-Time Updates**: Live transaction monitoring with stable counts
- **Interactive Elements**: Click transactions for detailed analysis

### 🔒 **Security & Access Control**
- **Role-Based Authentication**: Admin vs Customer access levels
- **Secure API Endpoints**: Protected routes with proper validation
- **Data Privacy**: Compliance with banking security standards

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Node.js 16+
- UiPath Studio (for RPA workflows)

### **Backend Setup**
```bash
cd phase1_data_foundation
pip install flask pandas scikit-learn xgboost
python flask_server.py
# Server runs on http://localhost:5000
```

### **Frontend Setup**
```bash
cd phase5_frontend
npm install
npm start
# Application runs on http://localhost:3000
```

### **UiPath Setup**
1. Open UiPath Studio
2. Open `UiPath_Workflows/Main.xaml`
3. Update variables:
   - `SystemURL`: `http://localhost:3000`
   - `ApiEndpoint`: `http://localhost:5000`
4. Run the workflow

## 📊 **Usage Examples**

### **Real-Time Monitoring**
1. Upload CSV file with transaction data
2. Click "Start Monitoring" 
3. Watch live transaction processing
4. Click any transaction for detailed AI explanation

### **Batch Processing**
1. Go to Batch Processing page
2. Add transactions manually or upload file
3. Click "Process Batch"
4. View results and export reports

### **Analytics Dashboard**
1. Navigate to Analytics page
2. Use time range filters
3. Click "Refresh" for latest data
4. Export charts and reports

## 🤝 **Contributing**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**
**Sidharth Rahul** - [GitHub](https://github.com/Sid1rahul)

## 🙏 **Acknowledgments**
- Machine Learning models inspired by industry best practices
- UI/UX design following modern banking application standards
- RPA integration using UiPath automation platform

## Technology Stack
- Python, scikit-learn, XGBoost, SHAP, ADASYN
- UiPath Studio & Orchestrator
- React.js, Node.js, PostgreSQL
- Docker, Kubernetes
