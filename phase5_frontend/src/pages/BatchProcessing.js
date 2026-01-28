import React, { useState } from 'react';
import { 
  Layers, 
  Upload, 
  Download, 
  Play, 
  Pause, 
  RotateCcw,
  FileText,
  AlertTriangle,
  CheckCircle,
  Clock,
  Trash2,
  Plus,
  Lock,
  Shield
} from 'lucide-react';
import toast from 'react-hot-toast';
import { fraudAPI, formatBatchData, generateMockBatch, getRiskLevelBadge, formatCurrencyINR } from '../utils/api';
import { hasPermission, PERMISSIONS } from '../utils/dataAccess';
import UserTransactionMonitor from '../components/UserTransactionMonitor';
import './BatchProcessing.css';

const BatchProcessing = ({ user }) => {
  const [transactions, setTransactions] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [results, setResults] = useState(null);
  const [progress, setProgress] = useState(0);

  const addTransaction = () => {
    const newTransaction = {
      id: Date.now(),
      amount: '',
      merchant: '',
      cardType: 'credit',
      customerId: ''
    };
    setTransactions([...transactions, newTransaction]);
  };

  const removeTransaction = (id) => {
    setTransactions(transactions.filter(t => t.id !== id));
  };

  const updateTransaction = (id, field, value) => {
    setTransactions(transactions.map(t => 
      t.id === id ? { ...t, [field]: value } : t
    ));
  };

  const generateMockData = () => {
    const mockTransactions = generateMockBatch(10).map((transaction, index) => ({
      id: Date.now() + index,
      ...transaction
    }));
    setTransactions(mockTransactions);
    toast.success('Generated 10 mock transactions');
  };

  const clearAll = () => {
    setTransactions([]);
    setResults(null);
    setProgress(0);
    toast.success('All data cleared');
  };

  const processBatch = async () => {
    if (transactions.length === 0) {
      toast.error('Please add some transactions first');
      return;
    }

    // Validate transactions
    const invalidTransactions = transactions.filter(t => !t.amount || !t.merchant);
    if (invalidTransactions.length > 0) {
      toast.error(`${invalidTransactions.length} transactions are missing required fields`);
      return;
    }

    setProcessing(true);
    setProgress(0);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const batchData = formatBatchData(transactions);
      const response = await fraudAPI.predictFraudBatch(batchData);
      
      clearInterval(progressInterval);
      setProgress(100);
      
      // Transform backend response to match frontend expectations
      const transformedResults = {
        success_count: response.total_processed || transactions.length,
        processing_time_ms: (response.processing_time || 0.5) * 1000,
        predictions: response.results ? response.results.map(result => ({
          fraud_probability: result.fraud_probability || 0,
          risk_level: result.risk_level || 'low',
          prediction: result.is_fraud ? 'fraud' : 'approve',
          confidence: result.fraud_probability || 0,
          processing_time_ms: 150
        })) : []
      };
      
      setResults(transformedResults);
      
      // Show summary toast
      const fraudCount = transformedResults.predictions.filter(p => p.prediction === 'fraud').length;
      const reviewCount = transformedResults.predictions.filter(p => p.prediction === 'review').length;
      
      if (fraudCount > 0) {
        toast.error(`Batch complete: ${fraudCount} fraud cases detected, ${reviewCount} need review`);
      } else {
        toast.success(`Batch complete: ${transformedResults.success_count} transactions processed successfully`);
      }
      
    } catch (error) {
      toast.error(`Batch processing failed: ${error.message}`);
      console.error('Batch processing error:', error);
    } finally {
      setProcessing(false);
      setTimeout(() => setProgress(0), 2000);
    }
  };

  const exportResults = () => {
    if (!results) return;
    
    const csvData = results.predictions.map((result, index) => ({
      'Transaction ID': index + 1,
      'Merchant': transactions[index]?.merchant || 'Unknown',
      'Amount': transactions[index]?.amount || 0,
      'Fraud Probability': (result.fraud_probability * 100).toFixed(2) + '%',
      'Risk Level': result.risk_level,
      'Prediction': result.prediction,
      'Confidence': (result.confidence * 100).toFixed(2) + '%',
      'Processing Time (ms)': result.processing_time_ms
    }));
    
    const csvContent = [
      Object.keys(csvData[0]).join(','),
      ...csvData.map(row => Object.values(row).join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fraud_detection_results_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    toast.success('Results exported to CSV');
  };

  // Check if user has admin permissions for batch processing
  const canProcessBatch = hasPermission(user, PERMISSIONS.BATCH_PROCESSING);

  // If user is not admin, show access restricted message
  if (!canProcessBatch) {
    return (
      <div className="access-restricted">
        <div className="restriction-content">
          <Lock size={64} className="restriction-icon" />
          <h2>Access Restricted</h2>
          <p>Batch processing is only available to administrators.</p>
          <p>As a customer, you can view your transaction history in the Real-Time Monitoring section.</p>
          <div className="suggestion">
            <Shield size={20} />
            <span>Contact your bank administrator for advanced fraud analysis features.</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="batch-processing">
      <div className="page-header">
        <div className="header-content">
          <Layers className="header-icon" />
          <div>
            <h1>Batch Processing</h1>
            <p>Process multiple transactions simultaneously for fraud detection</p>
          </div>
        </div>
        
        <div className="header-actions">
          <button onClick={generateMockData} className="btn btn-secondary">
            <FileText size={20} />
            Generate Mock Data
          </button>
          <button onClick={clearAll} className="btn btn-ghost">
            <Trash2 size={20} />
            Clear All
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      {processing && (
        <div className="progress-section">
          <div className="progress-header">
            <span>Processing {transactions.length} transactions...</span>
            <span>{progress}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      )}

      <div className="batch-layout">
        {/* Transaction Input Section */}
        <div className="input-section">
          <div className="section-header">
            <h2>Transaction List</h2>
            <div className="section-actions">
              <button onClick={addTransaction} className="btn btn-primary btn-sm">
                <Plus size={16} />
                Add Transaction
              </button>
            </div>
          </div>

          <div className="transactions-container">
            {transactions.length === 0 ? (
              <div className="empty-state">
                <Upload size={48} />
                <h3>No Transactions Added</h3>
                <p>Add transactions manually or generate mock data to get started</p>
                <button onClick={addTransaction} className="btn btn-primary">
                  <Plus size={20} />
                  Add First Transaction
                </button>
              </div>
            ) : (
              <div className="transactions-list">
                <div className="transactions-header">
                  <span className="header-cell">Amount</span>
                  <span className="header-cell">Merchant</span>
                  <span className="header-cell">Card Type</span>
                  <span className="header-cell">Customer ID</span>
                  <span className="header-cell">Actions</span>
                </div>
                
                {transactions.map((transaction, index) => (
                  <div key={transaction.id} className="transaction-row">
                    <div className="row-number">{index + 1}</div>
                    <input
                      type="number"
                      placeholder="0.00"
                      value={transaction.amount}
                      onChange={(e) => updateTransaction(transaction.id, 'amount', e.target.value)}
                      className="transaction-input amount-input"
                      step="0.01"
                      min="0"
                    />
                    <input
                      type="text"
                      placeholder="Merchant name"
                      value={transaction.merchant}
                      onChange={(e) => updateTransaction(transaction.id, 'merchant', e.target.value)}
                      className="transaction-input"
                    />
                    <select
                      value={transaction.cardType}
                      onChange={(e) => updateTransaction(transaction.id, 'cardType', e.target.value)}
                      className="transaction-input transaction-select"
                    >
                      <option value="credit">Credit</option>
                      <option value="debit">Debit</option>
                      <option value="prepaid">Prepaid</option>
                    </select>
                    <input
                      type="text"
                      placeholder="CUST_12345"
                      value={transaction.customerId}
                      onChange={(e) => updateTransaction(transaction.id, 'customerId', e.target.value)}
                      className="transaction-input"
                    />
                    <button
                      onClick={() => removeTransaction(transaction.id)}
                      className="btn btn-ghost btn-sm remove-btn"
                      title="Remove transaction"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {transactions.length > 0 && (
            <div className="batch-actions">
              <button
                onClick={processBatch}
                disabled={processing}
                className="btn btn-primary btn-lg"
              >
                {processing ? (
                  <>
                    <div className="spinner"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    <Play size={20} />
                    Process Batch ({transactions.length} transactions)
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {/* Results Section */}
        {results && (
          <div className="results-section">
            <div className="section-header">
              <h2>Processing Results</h2>
              <div className="section-actions">
                <button onClick={exportResults} className="btn btn-secondary btn-sm">
                  <Download size={16} />
                  Export CSV
                </button>
              </div>
            </div>

            {/* Summary Stats */}
            <div className="results-summary">
              <div className="summary-card">
                <div className="summary-icon success">
                  <CheckCircle size={24} />
                </div>
                <div className="summary-content">
                  <span className="summary-value">{results.success_count}</span>
                  <span className="summary-label">Successful</span>
                </div>
              </div>
              
              <div className="summary-card">
                <div className="summary-icon error">
                  <AlertTriangle size={24} />
                </div>
                <div className="summary-content">
                  <span className="summary-value">
                    {results.predictions.filter(p => p.prediction === 'fraud').length}
                  </span>
                  <span className="summary-label">Fraud Detected</span>
                </div>
              </div>
              
              <div className="summary-card">
                <div className="summary-icon warning">
                  <Clock size={24} />
                </div>
                <div className="summary-content">
                  <span className="summary-value">
                    {results.predictions.filter(p => p.prediction === 'review').length}
                  </span>
                  <span className="summary-label">Need Review</span>
                </div>
              </div>
              
              <div className="summary-card">
                <div className="summary-icon info">
                  <RotateCcw size={24} />
                </div>
                <div className="summary-content">
                  <span className="summary-value">{results.processing_time_ms.toFixed(0)}ms</span>
                  <span className="summary-label">Total Time</span>
                </div>
              </div>
            </div>

            {/* Results List */}
            <div className="results-list">
              <div className="results-header">
                <span className="header-cell">#</span>
                <span className="header-cell">Transaction</span>
                <span className="header-cell">Fraud Probability</span>
                <span className="header-cell">Risk Level</span>
                <span className="header-cell">Decision</span>
                <span className="header-cell">Confidence</span>
              </div>
              
              {results.predictions.map((result, index) => {
                const transaction = transactions[index];
                return (
                  <div key={index} className={`result-row ${result.prediction}`}>
                    <div className="result-number">{index + 1}</div>
                    <div className="result-transaction">
                      <div className="transaction-merchant">{transaction?.merchant || 'Unknown'}</div>
                      <div className="transaction-amount">{formatCurrencyINR(transaction?.amount || 0)}</div>
                    </div>
                    <div className="result-probability">
                      <div className="probability-bar-small">
                        <div 
                          className="probability-fill-small"
                          style={{ 
                            width: `${result.fraud_probability * 100}%`,
                            backgroundColor: result.fraud_probability > 0.6 ? 'var(--error)' : 
                                           result.fraud_probability > 0.3 ? 'var(--warning)' : 'var(--success)'
                          }}
                        ></div>
                      </div>
                      <span className="probability-text-small">
                        {(result.fraud_probability * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className={`result-risk ${getRiskLevelBadge(result.risk_level)}`}>
                      {result.risk_level}
                    </div>
                    <div className={`result-decision ${result.prediction}`}>
                      <div className={`decision-icon ${result.prediction}`}>
                        {result.prediction === 'fraud' && <AlertTriangle size={16} />}
                        {result.prediction === 'approve' && <CheckCircle size={16} />}
                        {result.prediction === 'review' && <Clock size={16} />}
                        {result.prediction === 'monitor' && <Clock size={16} />}
                      </div>
                      <span>{result.prediction}</span>
                    </div>
                    <div className="result-confidence">
                      {(result.confidence * 100).toFixed(1)}%
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BatchProcessing;
