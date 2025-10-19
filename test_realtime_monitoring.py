#!/usr/bin/env python3
"""
Test script for Real-Time Monitoring API
Demonstrates file upload and monitoring functionality
"""

import requests
import json
import time
import os

# API configuration
BASE_URL = "http://localhost:8000"
TOKEN = "demo_token_123"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_health():
    """Test API health"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"📊 Models loaded: {data['models_loaded']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def upload_file():
    """Upload CSV file for processing"""
    print("\n📁 Uploading sample transaction file...")
    
    file_path = "C:/CFD/sample_transactions.csv"
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    try:
        with open(file_path, 'rb') as file:
            files = {'file': ('sample_transactions.csv', file, 'text/csv')}
            response = requests.post(
                f"{BASE_URL}/api/upload/file",
                headers=HEADERS,
                files=files
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ File uploaded successfully!")
            print(f"📋 File ID: {data['file_id']}")
            print(f"📊 Total transactions: {data['total_transactions']}")
            print(f"📝 Columns: {', '.join(data['columns'])}")
            print(f"💾 File size: {data['file_size_bytes']} bytes")
            
            # Show preview
            print("\n📋 Data preview:")
            for i, row in enumerate(data['preview'][:3]):
                print(f"  Row {i+1}: ${row.get('amount', 'N/A')} at {row.get('merchant', 'N/A')}")
            
            return data['file_id']
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def start_monitoring(file_id):
    """Start real-time monitoring session"""
    print(f"\n🔄 Starting monitoring session for file: {file_id}")
    
    try:
        data = {
            'file_id': file_id,
            'processing_speed_ms': 500  # Process every 500ms
        }
        
        response = requests.post(
            f"{BASE_URL}/api/monitoring/start",
            headers=HEADERS,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            session_id = result['session_id']
            print(f"✅ Monitoring started!")
            print(f"🆔 Session ID: {session_id}")
            return session_id
        else:
            print(f"❌ Failed to start monitoring: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Monitoring start error: {e}")
        return None

def monitor_session(session_id, duration=15):
    """Monitor the session for specified duration"""
    print(f"\n📈 Monitoring session for {duration} seconds...")
    
    start_time = time.time()
    last_processed = 0
    
    while time.time() - start_time < duration:
        try:
            # Get session status
            response = requests.get(
                f"{BASE_URL}/api/monitoring/status/{session_id}",
                headers=HEADERS
            )
            
            if response.status_code == 200:
                status = response.json()
                
                # Show progress if new transactions processed
                if status['processed_count'] > last_processed:
                    print(f"📊 Progress: {status['processed_count']}/{status['total_transactions']} "
                          f"(Fraud: {status['fraud_detected']}) - Status: {status['status']}")
                    last_processed = status['processed_count']
                
                # Check if completed
                if status['status'] in ['completed', 'stopped']:
                    print(f"✅ Session completed!")
                    print(f"📈 Final stats:")
                    print(f"  - Total processed: {status['processed_count']}")
                    print(f"  - Fraud detected: {status['fraud_detected']}")
                    fraud_rate = (status['fraud_detected'] / status['processed_count'] * 100) if status['processed_count'] > 0 else 0
                    print(f"  - Fraud rate: {fraud_rate:.1f}%")
                    break
            
            time.sleep(2)  # Check every 2 seconds
            
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
            break

def get_fraud_alerts():
    """Get recent fraud alerts"""
    print(f"\n🚨 Checking fraud alerts...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/monitoring/alerts?limit=10",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            data = response.json()
            alerts = data['alerts']
            
            print(f"🚨 Found {len(alerts)} fraud alerts:")
            
            for alert in alerts[:5]:  # Show first 5
                risk_pct = alert['risk_score'] * 100
                print(f"  - ${alert['amount']:.2f} at {alert['merchant']} "
                      f"(Risk: {risk_pct:.1f}%, Customer: {alert['customer_id']})")
            
            return len(alerts)
        else:
            print(f"❌ Failed to get alerts: {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ Alerts error: {e}")
        return 0

def main():
    """Main test function"""
    print("🚀 Real-Time Monitoring System Test")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health():
        print("❌ API not available. Make sure the enhanced backend is running.")
        return
    
    # Test 2: File upload
    file_id = upload_file()
    if not file_id:
        print("❌ File upload failed. Cannot proceed with monitoring test.")
        return
    
    # Test 3: Start monitoring
    session_id = start_monitoring(file_id)
    if not session_id:
        print("❌ Failed to start monitoring session.")
        return
    
    # Test 4: Monitor progress
    monitor_session(session_id, duration=20)
    
    # Test 5: Check fraud alerts
    alert_count = get_fraud_alerts()
    
    print(f"\n🎉 Test completed successfully!")
    print(f"📊 Summary:")
    print(f"  - File uploaded: ✅")
    print(f"  - Monitoring started: ✅") 
    print(f"  - Fraud alerts generated: {alert_count}")
    print(f"\n💡 You can now test the frontend at: http://localhost:3000/real-time-monitoring")

if __name__ == "__main__":
    main()
