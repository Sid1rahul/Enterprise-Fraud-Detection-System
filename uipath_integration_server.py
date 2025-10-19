#!/usr/bin/env python3
"""
UiPath Studio Integration Server
Handles communication between UiPath workflows and the Fraud Detection Chatbot
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import json
import datetime
from pathlib import Path
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="UiPath Integration Server",
    description="Bridge between UiPath Studio and Fraud Detection System",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ChatMessage(BaseModel):
    user_message: str
    bot_response: str
    timestamp: str
    session_id: str

class UiPathWorkflow(BaseModel):
    workflow_name: str
    status: str
    last_execution: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class WorkflowExecution(BaseModel):
    workflow_name: str
    parameters: Dict[str, Any]
    execution_mode: str = "attended"  # attended or unattended

# In-memory storage (in production, use a database)
conversation_history: List[ChatMessage] = []
active_workflows: Dict[str, UiPathWorkflow] = {}
workflow_results: Dict[str, Dict[str, Any]] = {}

# Initialize with sample workflows
active_workflows = {
    "fraud_detection_chatbot": UiPathWorkflow(
        workflow_name="Fraud Detection Chatbot",
        status="ready",
        last_execution=None,
        parameters={
            "dashboard_url": "http://localhost:3000/dashboard",
            "api_endpoint": "http://localhost:8000",
            "auth_token": "demo_token_123"
        }
    ),
    "transaction_analyzer": UiPathWorkflow(
        workflow_name="Transaction Analyzer",
        status="ready",
        last_execution=None,
        parameters={
            "analysis_threshold": 0.7,
            "auto_approve_limit": 100.0
        }
    ),
    "fraud_report_generator": UiPathWorkflow(
        workflow_name="Fraud Report Generator",
        status="ready",
        last_execution=None,
        parameters={
            "report_format": "PDF",
            "include_charts": True
        }
    )
}

@app.get("/")
async def root():
    """Root endpoint with server information"""
    return {
        "service": "UiPath Integration Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "status": "/uipath/status",
            "workflows": "/uipath/workflows",
            "conversation": "/uipath/conversation",
            "execute": "/uipath/execute"
        },
        "connected_systems": {
            "fraud_detection_api": "http://localhost:8000",
            "frontend_dashboard": "http://localhost:3000"
        }
    }

@app.get("/uipath/status")
async def get_uipath_status():
    """Get UiPath Studio connection status"""
    return {
        "status": "connected",
        "studio_version": "2023.10.0",
        "robot_status": "available",
        "active_workflows": len(active_workflows),
        "workflow": {
            "name": "Fraud Detection Integration",
            "status": "ready",
            "last_updated": datetime.datetime.now().isoformat()
        },
        "capabilities": [
            "chatbot_integration",
            "api_automation",
            "report_generation",
            "data_processing"
        ]
    }

@app.get("/uipath/workflows")
async def get_workflows():
    """Get list of available UiPath workflows"""
    return {
        "workflows": list(active_workflows.values()),
        "total_count": len(active_workflows),
        "last_updated": datetime.datetime.now().isoformat()
    }

@app.post("/uipath/conversation")
async def log_conversation(message: ChatMessage):
    """Log chatbot conversation for UiPath workflow processing"""
    try:
        # Add timestamp if not provided
        if not message.timestamp:
            message.timestamp = datetime.datetime.now().isoformat()
        
        # Store conversation
        conversation_history.append(message)
        
        # Process message for workflow triggers
        workflow_action = await process_message_for_workflows(message)
        
        logger.info(f"Conversation logged: {message.user_message[:50]}...")
        
        return {
            "status": "logged",
            "message_id": len(conversation_history),
            "timestamp": message.timestamp,
            "workflow_triggered": workflow_action is not None,
            "action": workflow_action
        }
    except Exception as e:
        logger.error(f"Error logging conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/uipath/execute")
async def execute_workflow(execution: WorkflowExecution):
    """Execute a UiPath workflow with parameters"""
    try:
        workflow_name = execution.workflow_name
        
        if workflow_name not in active_workflows:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Simulate workflow execution
        execution_id = f"exec_{len(workflow_results) + 1}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Update workflow status
        active_workflows[workflow_name].status = "running"
        active_workflows[workflow_name].last_execution = datetime.datetime.now().isoformat()
        
        # Simulate processing time
        await asyncio.sleep(2)
        
        # Generate mock results based on workflow type
        result = await simulate_workflow_execution(workflow_name, execution.parameters)
        
        # Store results
        workflow_results[execution_id] = {
            "workflow_name": workflow_name,
            "execution_id": execution_id,
            "status": "completed",
            "start_time": active_workflows[workflow_name].last_execution,
            "end_time": datetime.datetime.now().isoformat(),
            "parameters": execution.parameters,
            "results": result
        }
        
        # Update workflow status
        active_workflows[workflow_name].status = "ready"
        
        logger.info(f"Workflow executed: {workflow_name}")
        
        return {
            "execution_id": execution_id,
            "status": "completed",
            "workflow_name": workflow_name,
            "results": result
        }
        
    except Exception as e:
        logger.error(f"Error executing workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/uipath/results/{execution_id}")
async def get_execution_results(execution_id: str):
    """Get results of a workflow execution"""
    if execution_id not in workflow_results:
        raise HTTPException(status_code=404, detail="Execution results not found")
    
    return workflow_results[execution_id]

@app.get("/uipath/conversation/history")
async def get_conversation_history(limit: int = 50):
    """Get recent conversation history"""
    return {
        "conversations": conversation_history[-limit:],
        "total_count": len(conversation_history),
        "last_updated": datetime.datetime.now().isoformat()
    }

async def process_message_for_workflows(message: ChatMessage) -> Optional[str]:
    """Process chatbot message to determine if any workflows should be triggered"""
    user_msg = message.user_message.lower()
    
    # Transaction analysis trigger
    if any(keyword in user_msg for keyword in ['analyze', 'check', 'fraud', 'transaction']):
        if '$' in user_msg or any(word in user_msg for word in ['dollar', 'amount']):
            return "transaction_analysis_workflow"
    
    # Report generation trigger
    if any(keyword in user_msg for keyword in ['report', 'generate', 'export', 'download']):
        return "report_generation_workflow"
    
    # System status trigger
    if any(keyword in user_msg for keyword in ['status', 'health', 'system']):
        return "system_monitoring_workflow"
    
    return None

async def simulate_workflow_execution(workflow_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate workflow execution and return mock results"""
    
    if "chatbot" in workflow_name.lower():
        return {
            "chatbot_deployed": True,
            "dashboard_integrated": True,
            "api_connected": True,
            "conversations_processed": len(conversation_history),
            "last_interaction": datetime.datetime.now().isoformat()
        }
    
    elif "analyzer" in workflow_name.lower():
        return {
            "transactions_analyzed": 150,
            "fraud_detected": 12,
            "fraud_rate": 8.0,
            "processing_time_ms": 2500,
            "accuracy": 95.2
        }
    
    elif "report" in workflow_name.lower():
        return {
            "report_generated": True,
            "format": parameters.get("report_format", "PDF"),
            "file_size_mb": 2.3,
            "pages": 15,
            "charts_included": parameters.get("include_charts", True),
            "generation_time_ms": 3200
        }
    
    else:
        return {
            "status": "completed",
            "execution_time_ms": 1500,
            "parameters_processed": len(parameters)
        }

@app.get("/uipath/health")
async def health_check():
    """Health check endpoint for UiPath integration"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "services": {
            "uipath_studio": "connected",
            "fraud_detection_api": "available",
            "chatbot_integration": "active"
        },
        "metrics": {
            "active_workflows": len(active_workflows),
            "total_conversations": len(conversation_history),
            "total_executions": len(workflow_results)
        }
    }

# WebSocket endpoint for real-time communication (optional)
@app.websocket("/ws/uipath")
async def websocket_endpoint(websocket):
    """WebSocket endpoint for real-time UiPath communication"""
    await websocket.accept()
    try:
        while True:
            # Send periodic status updates
            status = {
                "type": "status_update",
                "timestamp": datetime.datetime.now().isoformat(),
                "active_workflows": len(active_workflows),
                "recent_conversations": len(conversation_history)
            }
            await websocket.send_json(status)
            await asyncio.sleep(30)  # Send update every 30 seconds
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    print("🤖 Starting UiPath Integration Server...")
    print("📡 Server will be available at: http://localhost:8001")
    print("🔗 Connect your UiPath Studio workflows to this endpoint")
    print("💬 Chatbot integration ready for dashboard deployment")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        log_level="info"
    )
