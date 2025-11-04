"""
Simple Flask API Server for Fraud Detection System
"""

from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# Simple CORS handling without flask_cors
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Sample data for demonstration
sample_transactions = [
    {"id": "TXN_001", "amount": 89.99, "merchant": "Amazon", "status": "approved", "risk_score": 0.12},
    {"id": "TXN_002", "amount": 1250.00, "merchant": "Best Buy", "status": "approved", "risk_score": 0.25},
    {"id": "TXN_003", "amount": 3500.00, "merchant": "Casino Royal", "status": "flagged", "risk_score": 0.95}
]

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Fraud Detection API is running'
    })

@app.route('/api/health', methods=['GET'])
def api_health_check():
    """API Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Fraud Detection API is running'
    })

@app.route('/api/models/status', methods=['GET'])
def get_model_status():
    """Get model status"""
    return jsonify({
        'models_loaded': ['XGBoost', 'Isolation Forest'],
        'models': [
            {
                'name': 'XGBoost',
                'status': 'active',
                'accuracy': 98.7,
                'last_trained': '2024-01-15T10:30:00'
            },
            {
                'name': 'Isolation Forest',
                'status': 'active',
                'accuracy': 96.3,
                'last_trained': '2024-01-15T10:30:00'
            }
        ]
    })

@app.route('/api/fraud/detect', methods=['POST'])
def detect_fraud():
    """Detect fraud in transaction"""
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        
        # Simple fraud detection logic
        risk_score = min(amount / 10000, 0.99)
        is_fraud = risk_score > 0.7
        
        return jsonify({
            'fraud_probability': risk_score,
            'is_fraud': is_fraud,
            'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.3 else 'low',
            'decision': 'BLOCK' if is_fraud else 'ALLOW'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get sample transactions"""
    return jsonify(sample_transactions)

@app.route('/api/batch/process', methods=['POST'])
def process_batch():
    """Process batch of transactions"""
    try:
        # Simulate batch processing
        return jsonify({
            'processed': 100,
            'fraud_detected': 5,
            'processing_time': 2.5,
            'status': 'completed'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/upload/file', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Simulate file processing
        return jsonify({
            'file_id': 'FILE_123',
            'filename': file.filename,
            'size': len(file.read()),
            'status': 'uploaded',
            'message': 'File uploaded successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/fraud/predict', methods=['POST'])
def predict_fraud():
    """Predict fraud for single transaction"""
    try:
        data = request.json
        amount = float(data.get('transaction_data', {}).get('amount', 0))
        
        # Simple fraud detection logic
        risk_score = min(amount / 10000, 0.99)
        is_fraud = risk_score > 0.7
        
        return jsonify({
            'fraud_probability': risk_score,
            'is_fraud': is_fraud,
            'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.3 else 'low',
            'decision': 'BLOCK' if is_fraud else 'ALLOW',
            'model_used': 'XGBoost',
            'processing_time': 0.15
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/fraud/predict/batch', methods=['POST'])
def predict_fraud_batch():
    """Predict fraud for batch of transactions"""
    try:
        data = request.json
        transactions = data.get('transactions', [])
        
        results = []
        for i, txn in enumerate(transactions):
            amount = float(txn.get('transaction_data', {}).get('amount', 0))
            risk_score = min(amount / 10000, 0.99)
            is_fraud = risk_score > 0.7
            
            results.append({
                'transaction_id': i,
                'fraud_probability': risk_score,
                'is_fraud': is_fraud,
                'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.3 else 'low',
                'decision': 'BLOCK' if is_fraud else 'ALLOW'
            })
        
        return jsonify({
            'results': results,
            'total_processed': len(transactions),
            'fraud_detected': sum(1 for r in results if r['is_fraud']),
            'processing_time': len(transactions) * 0.05
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/monitoring/start', methods=['POST'])
def start_monitoring():
    """Start monitoring session"""
    try:
        file_id = request.form.get('file_id', 'FILE_123')
        processing_speed = int(request.form.get('processing_speed_ms', 1000))
        
        session_id = f"SESSION_{file_id}_{int(datetime.now().timestamp())}"
        
        # Initialize session in global storage
        monitoring_sessions[session_id] = {
            'processed_count': 0,
            'fraud_detected': 0,
            'start_time': datetime.now(),
            'last_update': datetime.now(),
            'file_id': file_id,
            'processing_speed': processing_speed
        }
        
        return jsonify({
            'session_id': session_id,
            'status': 'started',
            'file_id': file_id,
            'processing_speed_ms': processing_speed,
            'message': 'Monitoring session started successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Global session storage for consistent counts
monitoring_sessions = {}

@app.route('/api/monitoring/status/<session_id>', methods=['GET'])
def get_monitoring_status(session_id):
    """Get monitoring session status"""
    try:
        import random
        
        # Initialize session if not exists
        if session_id not in monitoring_sessions:
            monitoring_sessions[session_id] = {
                'processed_count': 0,
                'fraud_detected': 0,
                'start_time': datetime.now(),
                'last_update': datetime.now()
            }
        
        session = monitoring_sessions[session_id]
        
        # Increment processed count gradually (simulate real processing)
        time_diff = (datetime.now() - session['last_update']).total_seconds()
        if time_diff >= 2:  # Update every 2 seconds
            session['processed_count'] += random.randint(1, 3)
            if random.random() < 0.1:  # 10% chance of fraud
                session['fraud_detected'] += 1
            session['last_update'] = datetime.now()
        
        merchants = ['Amazon', 'Walmart', 'Starbucks', 'Shell Gas', 'Best Buy', 'Target', 'McDonald\'s', 'Grocery Store']
        
        return jsonify({
            'session_id': session_id,
            'status': 'running',
            'processed_count': session['processed_count'],
            'fraud_detected': session['fraud_detected'],
            'current_transaction': {
                'id': f'TXN_{random.randint(1000, 9999)}',
                'amount': round(random.uniform(10, 5000), 2),
                'merchant': random.choice(merchants),
                'risk_score': round(random.uniform(0.1, 0.9), 3)
            },
            'uptime_seconds': int((datetime.now() - session['start_time']).total_seconds())
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/monitoring/control/<session_id>', methods=['POST'])
def control_monitoring(session_id):
    """Control monitoring session (pause/resume/stop)"""
    try:
        action = request.form.get('action', 'pause')
        
        return jsonify({
            'session_id': session_id,
            'action': action,
            'status': 'paused' if action == 'pause' else 'running' if action == 'resume' else 'stopped',
            'message': f'Monitoring session {action}d successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/monitoring/alerts', methods=['GET'])
def get_fraud_alerts():
    """Get recent fraud alerts"""
    try:
        limit = int(request.args.get('limit', 50))
        
        alerts = [
            {
                'id': 'ALERT_001',
                'timestamp': datetime.now().isoformat(),
                'transaction_id': 'TXN_789',
                'amount': 5000.00,
                'merchant': 'Suspicious Store',
                'risk_score': 0.95,
                'alert_type': 'high_risk'
            },
            {
                'id': 'ALERT_002', 
                'timestamp': datetime.now().isoformat(),
                'transaction_id': 'TXN_790',
                'amount': 2500.00,
                'merchant': 'Casino Royal',
                'risk_score': 0.87,
                'alert_type': 'fraud_detected'
            }
        ]
        
        return jsonify({
            'alerts': alerts[:limit],
            'total_count': len(alerts)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/monitoring/sessions', methods=['GET'])
def get_monitoring_sessions():
    """Get all monitoring sessions"""
    try:
        sessions = [
            {
                'session_id': 'SESSION_FILE_123_1697612345',
                'status': 'running',
                'file_id': 'FILE_123',
                'start_time': datetime.now().isoformat(),
                'processed_count': 156,
                'fraud_detected': 8
            }
        ]
        
        return jsonify({
            'sessions': sessions,
            'active_count': 1
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/chatbot', methods=['POST'])
def chatbot_interaction():
    """Handle chatbot interactions"""
    try:
        data = request.json
        message = data.get('message', '').lower().strip()
        
        # System health check
        if any(word in message for word in ['health', 'status', 'system']):
            return jsonify({
                'response': '✅ **System Status: HEALTHY**\n\n🔧 **API Status**: healthy\n📊 **Models Loaded**: XGBoost, Isolation Forest\n🕐 **Last Updated**: ' + datetime.now().strftime('%I:%M:%S %p') + '\n🌐 **Endpoint**: http://localhost:5000',
                'type': 'system_status'
            })
        
        # Fraud statistics
        elif any(word in message for word in ['statistic', 'stats', 'fraud rate', 'numbers']):
            return jsonify({
                'response': '📊 **Fraud Statistics**\n\n📈 Total Transactions: 1,234\n🚨 Fraud Detected: 45 (3.6%)\n✅ Legitimate: 1,189 (96.4%)\n⚡ Avg Processing Time: 87ms\n🎯 Model Accuracy: 95.2%',
                'type': 'statistics'
            })
        
        # Analyze transaction
        elif any(word in message for word in ['analyze', 'check transaction', 'transaction']):
            return jsonify({
                'response': '🔍 **Transaction Analysis**\n\nTo analyze a transaction, please provide:\n• Transaction ID\n• Amount\n• Merchant name\n• Location\n\nOr go to Real-Time Monitoring to upload a file.',
                'type': 'analysis_help'
            })
        
        # Upload file
        elif any(word in message for word in ['upload', 'file', 'csv', 'batch']):
            return jsonify({
                'response': '📁 **File Upload**\n\nYou can upload transaction files in:\n• CSV format\n• Excel format\n\nGo to **Real-Time Monitoring** page and click "Upload transaction file" button.',
                'type': 'upload_help'
            })
        
        # Show fraud
        elif any(word in message for word in ['show fraud', 'fraud list', 'fraudulent']):
            return jsonify({
                'response': '🚨 **Recent Fraud Alerts**\n\n1. TXN_789 - $5,000 - Risk: 95%\n2. TXN_790 - $2,500 - Risk: 87%\n3. TXN_791 - $3,200 - Risk: 82%\n\nView full details in the Dashboard.',
                'type': 'fraud_list'
            })
        
        # Help
        elif any(word in message for word in ['help', 'what can you do', 'commands']):
            return jsonify({
                'response': '💡 **I can help you with:**\n\n• Check system health\n• Show fraud statistics\n• Analyze transactions\n• Upload transaction files\n• View fraud alerts\n• Explain fraud detection\n\nJust ask me anything!',
                'type': 'help'
            })
        
        # Greetings
        elif any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
            return jsonify({
                'response': '👋 Hi! I\'m your Fraud Detection Assistant. I can help you analyze transactions, check system status, and view fraud statistics. How can I assist you today?',
                'type': 'greeting'
            })
        
        # Thanks
        elif any(word in message for word in ['thank', 'thanks', 'appreciate']):
            return jsonify({
                'response': '😊 You\'re welcome! Let me know if you need anything else.',
                'type': 'acknowledgment'
            })
        
        # Default response
        else:
            return jsonify({
                'response': 'Hi! I\'m your Fraud Detection Assistant. I can help you analyze transactions, check system health, view statistics, and more. Try asking:\n\n• "Check system health"\n• "Show fraud statistics"\n• "Help me analyze a transaction"\n• "What can you do?"',
                'type': 'default'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("🚀 Starting Fraud Detection API Server...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/api/health")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
