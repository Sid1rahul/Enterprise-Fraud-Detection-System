# 🔧 UiPath Browser Extension Fix

## Quick Solution

### Option 1: Install Chrome Extension
1. Open Chrome
2. Go to: chrome://extensions/
3. Search Chrome Web Store for "UiPath Web Automation"
4. Install and enable the extension
5. Restart UiPath Studio

### Option 2: Use Edge Browser (Recommended)
In your UiPath workflow:
1. Change Browser Type from "Chrome" to "Edge"
2. Edge has better UiPath compatibility
3. No extension needed

### Option 3: Use Internet Explorer
1. Change Browser Type to "IE"
2. Most reliable for UiPath automation
3. Built-in support

## Manual Commands (If UiPath fails)

Instead of UiPath automation, run these manually:

**Terminal 1 (Backend):**
```
cd C:\CFD\phase1_data_foundation
python flask_server.py
```

**Terminal 2 (Frontend):**
```
cd C:\CFD\phase5_frontend
npm start
```

**Then open browser manually to:**
- http://localhost:3000

Your fraud detection system will work perfectly without UiPath automation.

## Browser Extension URLs
- **Chrome**: chrome://extensions/
- **Edge**: edge://extensions/
- **Firefox**: about:addons

The system works great manually - UiPath automation is just a bonus feature!
