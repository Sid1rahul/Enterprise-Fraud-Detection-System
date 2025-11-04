# 🚀 COMPLETE SETUP GUIDE - Fraud Detection System

## Step-by-Step Installation & Configuration

---

## 📋 PREREQUISITES

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **UiPath Studio 2025.10.0** (Optional) - [Download](https://www.uipath.com/product/studio)

### Recommended Tools
- **VS Code** - Code editor
- **Postman** - API testing
- **Chrome/Edge** - For voice features

### System Requirements
- **OS**: Windows 10/11, macOS, Linux
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 5GB free space
- **Internet**: For initial setup only

---

## 🔧 INSTALLATION

### STEP 1: CLONE REPOSITORY

```bash
git clone https://github.com/Sid1rahul/Enterprise-Fraud-Detection-System.git
cd Enterprise-Fraud-Detection-System
```

---

### STEP 2: BACKEND SETUP

#### 2.1 Navigate to Backend Directory
```bash
cd phase1_data_foundation
```

#### 2.2 Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies Installed**:
- Flask 2.0+
- Flask-CORS
- Flask-SocketIO
- scikit-learn
- XGBoost
- pandas
- numpy
- imbalanced-learn

#### 2.4 Verify Installation
```bash
python -c "import flask, sklearn, xgboost; print('All packages installed!')"
```

#### 2.5 Start Backend Server
```bash
python flask_server.py
```

**Expected Output**:
```
 * Running on http://127.0.0.1:5000
 * Loading ML models...
 * Models loaded successfully!
 * Server ready!
```

**Test Backend**:
Open browser: http://localhost:5000/health
Should see: `{"status": "healthy", "models_loaded": true}`

---

### STEP 3: FRONTEND SETUP

#### 3.1 Open New Terminal
Keep backend running, open new terminal

#### 3.2 Navigate to Frontend Directory
```bash
cd phase5_frontend
```

#### 3.3 Install Node Dependencies
```bash
npm install
```

**Dependencies Installed** (takes 2-3 minutes):
- React 18
- React Router 6
- Recharts
- Lucide React
- Axios
- And 1000+ sub-dependencies

#### 3.4 Start Frontend Server
```bash
npm start
```

**Expected Output**:
```
Compiled successfully!

You can now view fraud-detection-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000
```

**Browser Opens Automatically**: http://localhost:3000

---

### STEP 4: VERIFY SYSTEM

#### 4.1 Check Frontend
- Dashboard loads
- Sidebar navigation works
- Charts display
- No console errors (F12)

#### 4.2 Check Backend Connection
- Look for "🔗 UiPath Connected" or "⚠️ Standalone Mode" in chatbot
- Try chatbot: Type "hello"
- Should get response

#### 4.3 Test Fraud Detection
1. Go to "Real-Time Monitoring"
2. Click "Add Sample Transaction"
3. Click "Process Batch"
4. Should see results

#### 4.4 Test Voice Features (Chrome/Edge only)
1. Open chatbot (bottom-right)
2. Click microphone icon
3. Allow microphone permission
4. Speak: "Check system health"
5. Should transcribe and respond

#### 4.5 Test Wake Word (Optional)
1. Click ear icon (👂) next to chatbot
2. Icon turns blue with pulse
3. Say: "Hey Fraud Detector"
4. Chatbot should open automatically

---

### STEP 5: UIPATH SETUP (OPTIONAL)

#### 5.1 Install UiPath Studio
- Download from [uipath.com](https://www.uipath.com/product/studio)
- Install Community Edition (free)
- Version: 2025.10.0 or later

#### 5.2 Open Project
1. Launch UiPath Studio
2. Click "Open"
3. Navigate to: `CFD/UiPath_FraudDetection_Project/FraudDetectionAutomation`
4. Open `project.json`

#### 5.3 Install Dependencies
- UiPath will auto-install required packages
- Wait for completion (2-3 minutes)

#### 5.4 Configure Variables
Open `Main.xaml`, update variables:
- **SystemURL**: `http://localhost:3000`
- **ApiEndpoint**: `http://localhost:5000`
- **BrowserType**: `Chrome` or `Edge`

#### 5.5 Run Workflow
1. Click "Run" (F5)
2. Browser opens automatically
3. Workflow executes
4. Check Output panel for logs

---

## 🔐 DEFAULT CREDENTIALS

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full system access

### Customer Account
- **Username**: `customer`
- **Password**: `customer123`
- **Access**: Limited to own transactions

---

## 🌐 ACCESS URLS

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Docs**: http://localhost:5000/api/docs (if enabled)

---

## 📊 TESTING THE SYSTEM

### TEST 1: SINGLE TRANSACTION PREDICTION

**Using Postman/cURL**:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1500.00,
    "merchant": "Online Store",
    "location": "New York",
    "time": "14:30"
  }'
```

**Expected Response**:
```json
{
  "prediction": "legitimate",
  "confidence": 0.92,
  "risk_score": 15,
  "explanation": {
    "amount": "Normal",
    "location": "Expected",
    "time": "Typical"
  }
}
```

### TEST 2: BATCH PROCESSING

1. Go to http://localhost:3000/monitoring
2. Click "Upload CSV"
3. Select sample file (or create one)
4. Click "Process Batch"
5. View results

**Sample CSV Format**:
```csv
amount,merchant,location,time
150.00,Grocery Store,Local,10:30
5000.00,Electronics,Foreign,03:00
75.50,Restaurant,Local,19:00
```

### TEST 3: CHATBOT INTERACTION

**Text Commands**:
- "hello" → Greeting
- "check system health" → System status
- "show fraud statistics" → Stats
- "help" → Available commands

**Voice Commands** (Chrome/Edge):
- Click mic icon
- Say: "Check system health"
- Should transcribe and respond

### TEST 4: WAKE WORD DETECTION

1. Click ear icon (👂)
2. Icon turns blue
3. Say: "Hey Fraud Detector"
4. Chatbot opens
5. Say command
6. Bot responds

---

## 🐛 TROUBLESHOOTING

### ISSUE 1: Backend Won't Start

**Error**: `Port 5000 already in use`

**Solution**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

**Error**: `Module not found: flask`

**Solution**:
```bash
pip install -r requirements.txt
```

---

### ISSUE 2: Frontend Won't Start

**Error**: `npm ERR! code ENOENT`

**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**Error**: `Port 3000 already in use`

**Solution**:
```bash
# Kill process on port 3000
# Windows: netstat -ano | findstr :3000
# macOS/Linux: lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm start
```

---

### ISSUE 3: CORS Errors

**Error**: `Access-Control-Allow-Origin`

**Solution**:
1. Check Flask-CORS is installed: `pip install flask-cors`
2. Verify backend is running
3. Check browser console for exact error
4. Restart both servers

---

### ISSUE 4: Voice Features Not Working

**Error**: Microphone not detected

**Solution**:
1. Use Chrome or Edge (not Firefox/Safari)
2. Check microphone permissions in browser
3. Go to: chrome://settings/content/microphone
4. Allow localhost access
5. Refresh page

**Error**: Wake word not detecting

**Solution**:
1. Ensure ear icon is blue (active)
2. Speak clearly: "Hey Fraud Detector"
3. Check browser console for errors
4. Try variations: "Hey Fraud", "Fraud Detector"

---

### ISSUE 5: UiPath Connection Failed

**Error**: Workflow can't open browser

**Solution**:
1. Install Chrome/Edge extension
2. UiPath → Tools → Extensions
3. Enable for Chrome/Edge
4. Restart browser
5. Run workflow again

**Error**: Can't find elements

**Solution**:
1. Verify frontend is running (localhost:3000)
2. Update selectors in workflow
3. Use UI Explorer to find elements
4. Check browser zoom (should be 100%)

---

### ISSUE 6: ML Models Not Loading

**Error**: `Model file not found`

**Solution**:
1. Check if model files exist in `phase1_data_foundation/models/`
2. If missing, retrain models:
```bash
python fraud_detection_model.py --train
```
3. Restart backend

---

## ⚙️ CONFIGURATION

### Backend Configuration

**File**: `phase1_data_foundation/config.py` (create if needed)

```python
# Server Config
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000
DEBUG = True  # Set False for production

# CORS Config
CORS_ORIGINS = ['http://localhost:3000']

# Model Config
MODEL_PATH = './models/'
MODEL_VERSION = 'v1.0'

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'fraud_detection.log'
```

### Frontend Configuration

**File**: `phase5_frontend/src/config.js`

```javascript
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
export const WEBSOCKET_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:5000';
export const ENABLE_VOICE = true;
export const ENABLE_WAKE_WORD = true;
```

---

## 🚀 PRODUCTION DEPLOYMENT

### Backend (AWS EC2 Example)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Clone repo
git clone <repo-url>
cd phase1_data_foundation

# Install packages
pip3 install -r requirements.txt

# Run with Gunicorn
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_server:app
```

### Frontend (Netlify Example)

```bash
# Build for production
cd phase5_frontend
npm run build

# Deploy to Netlify
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

### Environment Variables

**Backend** (.env):
```
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
```

**Frontend** (.env.production):
```
REACT_APP_API_URL=https://api.yourapp.com
REACT_APP_WS_URL=wss://api.yourapp.com
```

---

## 📚 ADDITIONAL RESOURCES

### Documentation
- **PROJECT_SUMMARY.txt** - Complete overview
- **AI_CONTEXT.md** - For AI assistants
- **INTERVIEW_QA.md** - Interview Q&A
- **REAL_WORLD_SCENARIOS.md** - Use cases
- **WAKE_WORD_GUIDE.md** - Voice features
- **UIPATH_VOICE_CHATBOT_WORKFLOW.md** - RPA guide

### API Endpoints
- `POST /api/predict` - Single prediction
- `POST /api/predict_batch` - Batch prediction
- `POST /api/upload` - File upload
- `GET /api/transactions` - Get transactions
- `POST /api/chatbot` - Chatbot interaction
- `GET /health` - Health check

### Support
- **GitHub Issues**: Report bugs
- **Discussions**: Ask questions
- **Email**: Contact maintainer

---

## ✅ VERIFICATION CHECKLIST

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Repository cloned
- [ ] Backend dependencies installed
- [ ] Backend running on port 5000
- [ ] Frontend dependencies installed
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Dashboard loads correctly
- [ ] Chatbot responds to messages
- [ ] Voice recording works (Chrome/Edge)
- [ ] Wake word detection works (optional)
- [ ] UiPath workflow runs (optional)
- [ ] No console errors

---

## 🎓 NEXT STEPS

1. **Explore Features**: Try all pages and features
2. **Test API**: Use Postman to test endpoints
3. **Customize**: Modify code to fit your needs
4. **Deploy**: Push to production
5. **Monitor**: Set up logging and monitoring
6. **Scale**: Add load balancing, caching
7. **Improve**: Retrain models with new data

---

## 📞 SUPPORT

### Common Questions
- Check **INTERVIEW_QA.md** for detailed Q&A
- See **AI_CONTEXT.md** for technical details
- Read **REAL_WORLD_SCENARIOS.md** for use cases

### Getting Help
1. Check documentation first
2. Search GitHub issues
3. Ask in discussions
4. Contact maintainer

---

**Setup Complete! 🎉**

Your fraud detection system is now running and ready to use!

Access it at: http://localhost:3000

---

*Last Updated: November 2025*  
*Version: 1.0*  
*Status: Production-Ready ✅*
