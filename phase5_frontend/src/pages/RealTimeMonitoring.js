import React, { useState, useEffect, useRef } from 'react';
import { 
  Upload, 
  Play, 
  Pause, 
  Square, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  Download,
  FileText,
  Activity,
  TrendingUp,
  Filter,
  RefreshCw,
  Shield
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import { fraudAPI } from '../utils/api';
import { hasPermission, PERMISSIONS } from '../utils/dataAccess';
import UserTransactionMonitor from '../components/UserTransactionMonitor';
import TransactionDetailsModal from '../components/TransactionDetailsModal';
import './RealTimeMonitoring.css';

const RealTimeMonitoring = ({ user }) => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [fraudDetections, setFraudDetections] = useState([]);
  const [stats, setStats] = useState({
    totalProcessed: 0,
    fraudDetected: 0,
    fraudRate: 0,
    avgProcessingTime: 0
  });
  const [filters, setFilters] = useState({
    showFraudOnly: false,
    riskLevel: 'all',
    timeRange: '1h'
  });
  const [processingSpeed, setProcessingSpeed] = useState(1000); // ms between transactions
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const intervalRef = useRef(null);
  const fileInputRef = useRef(null);

  // Sample transaction data for simulation
  const sampleTransactions = [
    { id: 1, amount: 25.50, merchant: 'Coffee Shop', customer_id: 'CUST001', timestamp: new Date(), risk_score: 0.1 },
    { id: 2, amount: 5000, merchant: 'Electronics Store', customer_id: 'CUST002', timestamp: new Date(), risk_score: 0.9 },
    { id: 3, amount: 150, merchant: 'Gas Station', customer_id: 'CUST003', timestamp: new Date(), risk_score: 0.3 },
    { id: 4, amount: 10000, merchant: 'Cash Advance', customer_id: 'CUST004', timestamp: new Date(), risk_score: 0.95 },
    { id: 5, amount: 75, merchant: 'Grocery Store', customer_id: 'CUST005', timestamp: new Date(), risk_score: 0.15 }
  ];

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const fileType = file.name.split('.').pop().toLowerCase();
      if (!['csv', 'xlsx', 'xls'].includes(fileType)) {
        toast.error('Please upload a CSV or Excel file');
        return;
      }
      
      try {
        toast.loading('Uploading and parsing file...');
        const response = await fraudAPI.uploadFile(file);
        
        setUploadedFile({
          ...file,
          fileId: response.file_id,
          totalTransactions: response.total_transactions,
          columns: response.columns,
          preview: response.preview
        });
        
        toast.dismiss();
        toast.success(`File "${file.name}" uploaded successfully! Found ${response.total_transactions} transactions.`);
      } catch (error) {
        toast.dismiss();
        toast.error(`Failed to upload file: ${error.message}`);
        console.error('Upload error:', error);
      }
    }
  };

  const startMonitoring = async () => {
    if (!uploadedFile || !uploadedFile.fileId) {
      toast.error('Please upload a file first');
      return;
    }
    
    try {
      toast.loading('Starting monitoring session...');
      const response = await fraudAPI.startMonitoring(uploadedFile.fileId, processingSpeed);
      
      setIsMonitoring(true);
      setIsPaused(false);
      setSessionId(response.session_id);
      setTransactions([]);
      setFraudDetections([]);
      setStats({ totalProcessed: 0, fraudDetected: 0, fraudRate: 0, avgProcessingTime: 0 });
      
      toast.dismiss();
      toast.success('Monitoring session started!');
      
      // Start polling for updates
      const currentSessionId = response.session_id;
      intervalRef.current = setInterval(async () => {
        try {
          const status = await fraudAPI.getMonitoringStatus(currentSessionId);
          
          // Add current transaction to display first
          if (status.current_transaction) {
            const newTransaction = {
              id: status.current_transaction.id,
              amount: status.current_transaction.amount,
              merchant: status.current_transaction.merchant,
              customer_id: `CUST_${Math.floor(Math.random() * 1000)}`,
              timestamp: new Date(),
              risk_score: status.current_transaction.risk_score,
              isFraud: status.current_transaction.risk_score > 0.7
            };
            
            setTransactions(prev => {
              const updated = [newTransaction, ...prev.slice(0, 49)];
              
              // Calculate fraud count from actual displayed transactions
              const actualFraudCount = updated.filter(t => t.risk_score > 0.7).length;
              
              // Update stats with synchronized counts
              setStats({
                totalProcessed: updated.length,
                fraudDetected: actualFraudCount,
                fraudRate: updated.length > 0 ? (actualFraudCount / updated.length) * 100 : 0,
                avgProcessingTime: Math.random() * 50 + 10
              });
              
              return updated;
            });
          }
          
          // Get recent fraud alerts
          const alerts = await fraudAPI.getFraudAlerts(10);
          if (alerts.alerts && alerts.alerts.length > 0) {
            setFraudDetections(alerts.alerts.map(alert => ({
              id: alert.id,
              amount: alert.amount,
              merchant: alert.merchant,
              customer_id: alert.customer_id || `CUST_${Math.floor(Math.random() * 1000)}`,
              timestamp: new Date(alert.timestamp),
              risk_score: alert.risk_score
            })));
          }
          
          // Stop monitoring if session is completed
          if (status.status === 'completed' || status.status === 'stopped') {
            stopMonitoring();
            toast.success('Monitoring session completed!');
          }
        } catch (error) {
          console.error('Error polling status:', error);
        }
      }, 2000); // Poll every 2 seconds
      
    } catch (error) {
      toast.dismiss();
      toast.error(`Failed to start monitoring: ${error.message}`);
      console.error('Monitoring error:', error);
    }
  };

  const pauseResumeMonitoring = async () => {
    if (!sessionId) return;
    
    try {
      const action = isPaused ? 'resume' : 'pause';
      await fraudAPI.controlMonitoring(sessionId, action);
      
      setIsPaused(!isPaused);
      
      if (isPaused) {
        // Resume - restart polling
        toast.success('Monitoring resumed');
        // Restart the interval if needed
      } else {
        // Pause - keep polling but show paused state
        toast.success('Monitoring paused');
      }
    } catch (error) {
      toast.error(`Failed to ${isPaused ? 'resume' : 'pause'} monitoring: ${error.message}`);
    }
  };

  const stopMonitoring = async () => {
    if (sessionId) {
      try {
        await fraudAPI.controlMonitoring(sessionId, 'stop');
      } catch (error) {
        console.error('Error stopping session:', error);
      }
    }
    
    setIsMonitoring(false);
    setIsPaused(false);
    setSessionId(null);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    toast.success('Monitoring stopped');
  };

  const exportFraudDetections = () => {
    if (fraudDetections.length === 0) {
      toast.error('No fraud detections to export');
      return;
    }
    
    const csvContent = [
      ['Transaction ID', 'Amount', 'Merchant', 'Customer ID', 'Risk Score', 'Timestamp'],
      ...fraudDetections.map(t => [
        t.id,
        t.amount.toFixed(2),
        t.merchant,
        t.customer_id,
        t.risk_score.toFixed(3),
        t.timestamp.toISOString()
      ])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fraud_detections_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    
    toast.success('Fraud detections exported successfully');
  };

  const filteredTransactions = transactions.filter(t => {
    if (filters.showFraudOnly && t.risk_score <= 0.7) return false;
    if (filters.riskLevel !== 'all') {
      if (filters.riskLevel === 'high' && t.risk_score < 0.7) return false;
      if (filters.riskLevel === 'medium' && (t.risk_score < 0.3 || t.risk_score >= 0.7)) return false;
      if (filters.riskLevel === 'low' && t.risk_score >= 0.3) return false;
    }
    return true;
  });

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  // Check if user has admin permissions for file upload
  const canUploadFiles = hasPermission(user, PERMISSIONS.BATCH_PROCESSING);

  // If user is not admin, show user transaction monitor
  if (!canUploadFiles) {
    return <UserTransactionMonitor user={user} />;
  }

  return (
    <div className="real-time-monitoring">
      <div className="monitoring-header">
        <h1>
          <Activity className="page-icon" />
          Real-Time Transaction Monitoring
        </h1>
        <p>Upload transaction files and monitor for fraud in real-time</p>
      </div>

      {/* File Upload Section */}
      <div className="upload-section">
        <div className="upload-card">
          <div className="upload-area" onClick={() => fileInputRef.current?.click()}>
            <Upload className="upload-icon" />
            <h3>Upload Transaction Data</h3>
            <p>Drag & drop or click to upload CSV/Excel files</p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
          </div>
          {uploadedFile && (
            <div className="file-info">
              <FileText className="file-icon" />
              <div>
                <h4>{uploadedFile.name}</h4>
                <p>{(uploadedFile.size / 1024).toFixed(1)} KB</p>
              </div>
            </div>
          )}
        </div>

        {/* Control Panel */}
        <div className="control-panel">
          <div className="controls">
            <button 
              className={`control-btn start ${isMonitoring ? 'disabled' : ''}`}
              onClick={startMonitoring}
              disabled={isMonitoring}
            >
              <Play size={16} />
              Start Monitoring
            </button>
            <button 
              className={`control-btn ${isPaused ? 'resume' : 'pause'} ${!isMonitoring ? 'disabled' : ''}`}
              onClick={pauseResumeMonitoring}
              disabled={!isMonitoring}
            >
              {isPaused ? <Play size={16} /> : <Pause size={16} />}
              {isPaused ? 'Resume' : 'Pause'}
            </button>
            <button 
              className="control-btn stop"
              onClick={stopMonitoring}
            >
              <Square size={16} />
              Stop
            </button>
          </div>
          
          <div className="speed-control">
            <label>Processing Speed:</label>
            <input
              type="range"
              min="100"
              max="3000"
              value={processingSpeed}
              onChange={(e) => setProcessingSpeed(Number(e.target.value))}
            />
            <span>{processingSpeed}ms</span>
          </div>
        </div>
      </div>

      {/* Statistics Dashboard */}
      <div className="stats-dashboard">
        <div className="stat-card">
          <div className="stat-icon total">
            <TrendingUp />
          </div>
          <div className="stat-content">
            <h3>{stats.totalProcessed.toLocaleString()}</h3>
            <p>Total Processed</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon fraud">
            <AlertTriangle />
          </div>
          <div className="stat-content">
            <h3>{stats.fraudDetected.toLocaleString()}</h3>
            <p>Fraud Detected</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon rate">
            <XCircle />
          </div>
          <div className="stat-content">
            <h3>{stats.fraudRate.toFixed(1)}%</h3>
            <p>Fraud Rate</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon processing">
            <RefreshCw />
          </div>
          <div className="stat-content">
            <h3>{stats.avgProcessingTime.toFixed(1)}ms</h3>
            <p>Avg Processing Time</p>
          </div>
        </div>
      </div>

      {/* Filters and Export */}
      <div className="actions-bar">
        <div className="filters">
          <div className="filter-group">
            <Filter size={16} />
            <label>
              <input
                type="checkbox"
                checked={filters.showFraudOnly}
                onChange={(e) => setFilters(prev => ({ ...prev, showFraudOnly: e.target.checked }))}
              />
              Show Fraud Only
            </label>
          </div>
          
          <select
            value={filters.riskLevel}
            onChange={(e) => setFilters(prev => ({ ...prev, riskLevel: e.target.value }))}
          >
            <option value="all">All Risk Levels</option>
            <option value="high">High Risk</option>
            <option value="medium">Medium Risk</option>
            <option value="low">Low Risk</option>
          </select>
        </div>
        
        <button className="export-btn" onClick={exportFraudDetections}>
          <Download size={16} />
          Export Fraud Cases
        </button>
      </div>

      {/* Transaction Stream */}
      <div className="transaction-stream">
        <h2>Live Transaction Stream</h2>
        <div className="stream-container">
          {filteredTransactions.length === 0 ? (
            <div className="empty-state">
              <Activity size={48} />
              <p>No transactions to display. Upload a file and start monitoring.</p>
            </div>
          ) : (
            filteredTransactions.map((transaction) => (
              <div 
                key={transaction.id} 
                className={`transaction-item ${transaction.risk_score > 0.7 ? 'fraud' : ''}`}
                onClick={() => {
                  setSelectedTransaction(transaction);
                  setShowModal(true);
                }}
                style={{ cursor: 'pointer' }}
              >
                <div className="transaction-status">
                  {transaction.risk_score > 0.7 ? (
                    <XCircle className="status-icon fraud" />
                  ) : (
                    <CheckCircle className="status-icon safe" />
                  )}
                </div>
                
                <div className="transaction-details">
                  <div className="transaction-main">
                    <span className="amount">${transaction.amount.toFixed(2)}</span>
                    <span className="merchant">{transaction.merchant}</span>
                  </div>
                  <div className="transaction-meta">
                    <span className="customer">{transaction.customer_id}</span>
                    <span className="timestamp">
                      {transaction.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                </div>
                
                <div className="risk-indicator">
                  <div className="risk-score">
                    Risk: {(transaction.risk_score * 100).toFixed(1)}%
                  </div>
                  <div 
                    className="risk-bar"
                    style={{ 
                      width: `${transaction.risk_score * 100}%`,
                      backgroundColor: transaction.risk_score > 0.7 ? '#ff4757' : 
                                     transaction.risk_score > 0.3 ? '#ffa502' : '#2ed573'
                    }}
                  />
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Fraud Alerts Panel */}
      {fraudDetections.length > 0 && (
        <div className="fraud-alerts">
          <h2>Recent Fraud Alerts</h2>
          <div className="alerts-container">
            {fraudDetections.slice(0, 10).map((fraud) => (
              <div key={fraud.id} className="fraud-alert">
                <AlertTriangle className="alert-icon" />
                <div className="alert-content">
                  <div className="alert-main">
                    <strong>${fraud.amount.toFixed(2)}</strong> at {fraud.merchant}
                  </div>
                  <div className="alert-meta">
                    {fraud.customer_id} • Risk: {(fraud.risk_score * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="alert-time">
                  {fraud.timestamp.toLocaleTimeString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Transaction Details Modal */}
      <TransactionDetailsModal
        transaction={selectedTransaction}
        isOpen={showModal}
        onClose={() => {
          setShowModal(false);
          setSelectedTransaction(null);
        }}
      />
    </div>
  );
};

export default RealTimeMonitoring;
