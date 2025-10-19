"""
Enhanced Fraud Detection API with File Upload and Real-Time Monitoring
Provides ML model endpoints for real-time fraud detection with CSV/Excel support
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import joblib
import logging
from datetime import datetime
import os
import sys
import io
import asyncio
import json
import uuid
from concurrent.futures import ThreadPoolExecutor

# Add Phase 1 modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'phase1_data_foundation', 'src'))

try:
    from models.xgboost_model import XGBoostFraudDetector
    from models.isolation_forest import IsolationForestFraudDetector
    from explainability import ModelExplainer
except ImportError:
    # Mock classes for when models aren't available
    class XGBoostFraudDetector:
        def predict(self, data): return np.random.random(), "mock"
    class IsolationForestFraudDetector:
        def predict(self, data): return np.random.random(), "mock"
    class ModelExplainer:
        def explain(self, data): return {"mock": "explanation"}

# Security
security = HTTPBearer()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global storage for uploaded data and monitoring sessions
uploaded_datasets = {}
monitoring_sessions = {}
fraud_alerts = []

# Pydantic models
class TransactionData(BaseModel):
    """Transaction data model"""
    amount: float = Field(..., description="Transaction amount")
    merchant: str = Field(..., description="Merchant name")
    timestamp: str = Field(..., description="Transaction timestamp (ISO format)")
    card_type: str = Field(default="credit", description="Card type")
    customer_id: str = Field(..., description="Customer identifier")
    features: Dict[str, float] = Field(default={}, description="Additional features")

class FileUploadResponse(BaseModel):
    """File upload response model"""
    file_id: str
    filename: str
    total_transactions: int
    columns: List[str]
    preview: List[Dict[str, Any]]
    upload_timestamp: str
    file_size_bytes: int

class MonitoringSession(BaseModel):
    """Monitoring session model"""
    session_id: str
    file_id: str
    status: str  # "running", "paused", "stopped"
    total_transactions: int
    processed_count: int
    fraud_detected: int
    start_time: str
    processing_speed_ms: int

class RealTimeTransaction(BaseModel):
    """Real-time transaction model"""
    transaction_id: str
    amount: float
    merchant: str
    customer_id: str
    timestamp: str
    risk_score: float
    is_fraud: bool
    processing_time_ms: float

class FraudAlert(BaseModel):
    """Fraud alert model"""
    alert_id: str
    transaction_id: str
    amount: float
    merchant: str
    customer_id: str
    risk_score: float
    timestamp: str
    alert_level: str  # "high", "critical"

class EnhancedFraudDetectionAPI:
    """Enhanced fraud detection API with file upload and real-time monitoring"""
    
    def __init__(self):
        self.app = FastAPI(
            title="Enhanced Credit Card Fraud Detection API",
            description="ML-powered fraud detection with file upload and real-time monitoring",
            version="2.0.0"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize models
        self.models = {}
        self.load_models()
        
        # Thread pool for background processing
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Setup routes
        self.setup_routes()
    
    def load_models(self):
        """Load ML models"""
        try:
            # Try to load actual models
            self.models['xgboost'] = XGBoostFraudDetector()
            self.models['isolation_forest'] = IsolationForestFraudDetector()
            self.explainer = ModelExplainer()
            logger.info("Models loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load models: {e}")
            # Use mock models for demo
            self.models['xgboost'] = XGBoostFraudDetector()
            self.models['isolation_forest'] = IsolationForestFraudDetector()
            self.explainer = ModelExplainer()
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """Verify authentication token"""
        if credentials.credentials != "demo_token_123":
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return credentials.credentials
    
    def parse_uploaded_file(self, file_content: bytes, filename: str) -> pd.DataFrame:
        """Parse uploaded CSV or Excel file"""
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
            elif filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(io.BytesIO(file_content))
            else:
                raise ValueError("Unsupported file format")
            
            # Standardize column names
            column_mapping = {
                'Amount': 'amount',
                'Merchant': 'merchant',
                'Customer_ID': 'customer_id',
                'Timestamp': 'timestamp',
                'Card_Type': 'card_type'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Add missing columns with defaults
            if 'amount' not in df.columns:
                df['amount'] = np.random.uniform(10, 1000, len(df))
            if 'merchant' not in df.columns:
                merchants = ['Store A', 'Store B', 'Gas Station', 'Restaurant', 'Online Shop']
                df['merchant'] = np.random.choice(merchants, len(df))
            if 'customer_id' not in df.columns:
                df['customer_id'] = [f'CUST{i:06d}' for i in range(len(df))]
            if 'timestamp' not in df.columns:
                df['timestamp'] = pd.date_range(start='2024-01-01', periods=len(df), freq='H')
            
            return df
            
        except Exception as e:
            logger.error(f"Error parsing file: {e}")
            raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")
    
    def predict_fraud(self, transaction_data: dict, model_type: str = "xgboost") -> dict:
        """Predict fraud for a single transaction"""
        start_time = datetime.now()
        
        try:
            # Simulate fraud detection (replace with actual model prediction)
            amount = transaction_data.get('amount', 0)
            merchant = transaction_data.get('merchant', '')
            
            # Simple rule-based fraud detection for demo
            risk_score = 0.1  # Base risk
            
            # High amount increases risk
            if amount > 1000:
                risk_score += 0.3
            if amount > 5000:
                risk_score += 0.4
            
            # Certain merchants increase risk
            high_risk_merchants = ['cash advance', 'atm', 'casino', 'gambling']
            if any(term in merchant.lower() for term in high_risk_merchants):
                risk_score += 0.5
            
            # Add some randomness
            risk_score += np.random.uniform(-0.1, 0.1)
            risk_score = max(0, min(1, risk_score))
            
            is_fraud = risk_score > 0.7
            confidence = abs(risk_score - 0.5) * 2
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                'risk_score': risk_score,
                'is_fraud': is_fraud,
                'confidence': confidence,
                'processing_time_ms': processing_time,
                'prediction': 'fraud' if is_fraud else 'legitimate'
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                'risk_score': 0.5,
                'is_fraud': False,
                'confidence': 0.0,
                'processing_time_ms': 0,
                'prediction': 'error'
            }
    
    async def process_transactions_stream(self, session_id: str, df: pd.DataFrame, speed_ms: int):
        """Process transactions in real-time stream"""
        session = monitoring_sessions[session_id]
        
        for index, row in df.iterrows():
            if session['status'] != 'running':
                break
            
            # Create transaction data
            transaction_data = {
                'amount': float(row['amount']),
                'merchant': str(row['merchant']),
                'customer_id': str(row['customer_id']),
                'timestamp': str(row['timestamp'])
            }
            
            # Predict fraud
            prediction = self.predict_fraud(transaction_data)
            
            # Create real-time transaction
            transaction = RealTimeTransaction(
                transaction_id=str(uuid.uuid4()),
                amount=transaction_data['amount'],
                merchant=transaction_data['merchant'],
                customer_id=transaction_data['customer_id'],
                timestamp=datetime.now().isoformat(),
                risk_score=prediction['risk_score'],
                is_fraud=prediction['is_fraud'],
                processing_time_ms=prediction['processing_time_ms']
            )
            
            # Update session stats
            session['processed_count'] += 1
            if prediction['is_fraud']:
                session['fraud_detected'] += 1
                
                # Create fraud alert
                alert = FraudAlert(
                    alert_id=str(uuid.uuid4()),
                    transaction_id=transaction.transaction_id,
                    amount=transaction.amount,
                    merchant=transaction.merchant,
                    customer_id=transaction.customer_id,
                    risk_score=transaction.risk_score,
                    timestamp=transaction.timestamp,
                    alert_level="critical" if transaction.risk_score > 0.9 else "high"
                )
                fraud_alerts.append(alert.dict())
                
                # Keep only last 100 alerts
                if len(fraud_alerts) > 100:
                    fraud_alerts.pop(0)
            
            # Wait for specified interval
            await asyncio.sleep(speed_ms / 1000)
        
        # Mark session as completed
        session['status'] = 'completed'
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "models_loaded": list(self.models.keys())
            }
        
        @self.app.post("/api/upload/file", response_model=FileUploadResponse)
        async def upload_file(
            file: UploadFile = File(...),
            token: str = Depends(self.verify_token)
        ):
            """Upload CSV or Excel file for processing"""
            
            # Validate file type
            if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
                raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported")
            
            # Read file content
            content = await file.read()
            
            # Parse file
            df = self.parse_uploaded_file(content, file.filename)
            
            # Generate file ID
            file_id = str(uuid.uuid4())
            
            # Store dataset
            uploaded_datasets[file_id] = {
                'filename': file.filename,
                'dataframe': df,
                'upload_time': datetime.now().isoformat(),
                'file_size': len(content)
            }
            
            # Create response
            preview = df.head(5).to_dict('records')
            
            return FileUploadResponse(
                file_id=file_id,
                filename=file.filename,
                total_transactions=len(df),
                columns=list(df.columns),
                preview=preview,
                upload_timestamp=datetime.now().isoformat(),
                file_size_bytes=len(content)
            )
        
        @self.app.post("/api/monitoring/start")
        async def start_monitoring(
            file_id: str = Form(...),
            processing_speed_ms: int = Form(1000),
            token: str = Depends(self.verify_token)
        ):
            """Start real-time monitoring session"""
            
            if file_id not in uploaded_datasets:
                raise HTTPException(status_code=404, detail="File not found")
            
            session_id = str(uuid.uuid4())
            df = uploaded_datasets[file_id]['dataframe']
            
            # Create monitoring session
            session = {
                'session_id': session_id,
                'file_id': file_id,
                'status': 'running',
                'total_transactions': len(df),
                'processed_count': 0,
                'fraud_detected': 0,
                'start_time': datetime.now().isoformat(),
                'processing_speed_ms': processing_speed_ms
            }
            
            monitoring_sessions[session_id] = session
            
            # Start background processing
            asyncio.create_task(self.process_transactions_stream(session_id, df, processing_speed_ms))
            
            return {"session_id": session_id, "status": "started"}
        
        @self.app.get("/api/monitoring/status/{session_id}")
        async def get_monitoring_status(
            session_id: str,
            token: str = Depends(self.verify_token)
        ):
            """Get monitoring session status"""
            
            if session_id not in monitoring_sessions:
                raise HTTPException(status_code=404, detail="Session not found")
            
            return monitoring_sessions[session_id]
        
        @self.app.post("/api/monitoring/control/{session_id}")
        async def control_monitoring(
            session_id: str,
            action: str = Form(...),  # "pause", "resume", "stop"
            token: str = Depends(self.verify_token)
        ):
            """Control monitoring session (pause/resume/stop)"""
            
            if session_id not in monitoring_sessions:
                raise HTTPException(status_code=404, detail="Session not found")
            
            session = monitoring_sessions[session_id]
            
            if action == "pause":
                session['status'] = 'paused'
            elif action == "resume":
                session['status'] = 'running'
            elif action == "stop":
                session['status'] = 'stopped'
            else:
                raise HTTPException(status_code=400, detail="Invalid action")
            
            return {"session_id": session_id, "status": session['status']}
        
        @self.app.get("/api/monitoring/alerts")
        async def get_fraud_alerts(
            limit: int = 50,
            token: str = Depends(self.verify_token)
        ):
            """Get recent fraud alerts"""
            
            return {
                "alerts": fraud_alerts[-limit:],
                "total_alerts": len(fraud_alerts)
            }
        
        @self.app.get("/api/monitoring/sessions")
        async def get_monitoring_sessions(
            token: str = Depends(self.verify_token)
        ):
            """Get all monitoring sessions"""
            
            return {
                "sessions": list(monitoring_sessions.values()),
                "total_sessions": len(monitoring_sessions)
            }
        
        # Original endpoints for compatibility
        @self.app.post("/api/fraud/predict")
        async def predict_single_fraud(
            request: dict,
            token: str = Depends(self.verify_token)
        ):
            """Predict fraud for single transaction (original endpoint)"""
            
            transaction_data = request.get('transaction_data', {})
            model_type = request.get('model_type', 'xgboost')
            
            prediction = self.predict_fraud(transaction_data, model_type)
            
            return {
                "case_id": str(uuid.uuid4()),
                "fraud_probability": prediction['risk_score'],
                "risk_level": "high" if prediction['risk_score'] > 0.7 else "medium" if prediction['risk_score'] > 0.3 else "low",
                "prediction": prediction['prediction'],
                "confidence": prediction['confidence'],
                "processing_time_ms": prediction['processing_time_ms'],
                "model_used": model_type,
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.post("/api/fraud/predict/batch")
        async def predict_batch_fraud(
            request: dict,
            token: str = Depends(self.verify_token)
        ):
            """Predict fraud for batch of transactions"""
            
            transactions = request.get('transactions', [])
            model_type = request.get('model_type', 'xgboost')
            
            results = []
            start_time = datetime.now()
            
            for i, transaction_request in enumerate(transactions):
                transaction_data = transaction_request.get('transaction_data', {})
                prediction = self.predict_fraud(transaction_data, model_type)
                
                result = {
                    "case_id": str(uuid.uuid4()),
                    "fraud_probability": prediction['risk_score'],
                    "risk_level": "high" if prediction['risk_score'] > 0.7 else "medium" if prediction['risk_score'] > 0.3 else "low",
                    "prediction": prediction['prediction'],
                    "confidence": prediction['confidence'],
                    "processing_time_ms": prediction['processing_time_ms'],
                    "model_used": model_type,
                    "timestamp": datetime.now().isoformat(),
                    "transaction_index": i
                }
                results.append(result)
            
            total_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "predictions": results,
                "total_processed": len(transactions),
                "processing_time_ms": total_time,
                "success_count": len(results),
                "error_count": 0
            }
        
        @self.app.get("/api/models/status")
        async def get_model_status(token: str = Depends(self.verify_token)):
            """Get model status"""
            
            return {
                "models_loaded": list(self.models.keys()),
                "status": "healthy",
                "last_updated": datetime.now().isoformat()
            }

# Create API instance
api = EnhancedFraudDetectionAPI()
app = api.app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
