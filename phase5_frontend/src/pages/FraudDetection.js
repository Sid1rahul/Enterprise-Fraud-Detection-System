import React, { useState } from 'react';
import { 
  Shield, 
  CreditCard, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  DollarSign,
  MapPin,
  User,
  Zap,
  BarChart3,
  FileText,
  Upload,
  Play
} from 'lucide-react';
import toast from 'react-hot-toast';
import { fraudAPI, formatTransactionData, interpretPrediction, getRiskLevelBadge, generateMockTransaction } from '../utils/api';
import './FraudDetection.css';

const FraudDetection = () => {
  const [formData, setFormData] = useState({
    amount: '',
    merchant: '',
    cardType: 'credit',
    customerId: '',
    modelType: 'xgboost',
    explain: true
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  
  // Transaction range selection state
  const [rangeMode, setRangeMode] = useState(false);
  const [rangeData, setRangeData] = useState({
    startAmount: '',
    endAmount: '',
    merchants: '',
    count: 10
  });
  const [rangeResults, setRangeResults] = useState([]);
  const [rangeLoading, setRangeLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.amount || !formData.merchant) {
      toast.error('Please fill in all required fields');
      return;
    }

    setLoading(true);
    
    try {
      const transactionData = formatTransactionData(formData);
      const response = await fraudAPI.predictFraud(transactionData);
      
      setResult(response);
      
      // Add to history
      const historyItem = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        transaction: formData,
        result: response
      };
      setHistory(prev => [historyItem, ...prev.slice(0, 9)]); // Keep last 10
      
      // Show toast based on result
      const interpretation = interpretPrediction(response.prediction);
      if (response.prediction === 'fraud') {
        toast.error(interpretation.message);
      } else if (response.prediction === 'review') {
        toast((t) => (
          <div className="toast-content">
            <AlertTriangle size={20} />
            <span>{interpretation.message}</span>
          </div>
        ));
      } else {
        toast.success(interpretation.message);
      }
      
    } catch (error) {
      toast.error(`Prediction failed: ${error.message}`);
      console.error('Prediction error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateMock = () => {
    const mockData = generateMockTransaction();
    setFormData(prev => ({
      ...prev,
      amount: mockData.amount,
      merchant: mockData.merchant,
      cardType: mockData.cardType,
      customerId: mockData.customerId
    }));
    toast.success('Mock transaction data generated');
  };

  const handleClear = () => {
    setFormData({
      amount: '',
      merchant: '',
      cardType: 'credit',
      customerId: '',
      modelType: 'xgboost',
      explain: true
    });
    setResult(null);
    toast.success('Form cleared');
  };

  const handleRangeInputChange = (e) => {
    const { name, value } = e.target;
    setRangeData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const generateRangeTransactions = () => {
    const { startAmount, endAmount, merchants, count } = rangeData;
    const merchantList = merchants ? merchants.split(',').map(m => m.trim()) : 
      ['Amazon', 'Walmart', 'Gas Station', 'Restaurant', 'Coffee Shop', 'Electronics Store'];
    
    const transactions = [];
    for (let i = 0; i < count; i++) {
      const amount = startAmount && endAmount ? 
        (parseFloat(startAmount) + Math.random() * (parseFloat(endAmount) - parseFloat(startAmount))).toFixed(2) :
        (Math.random() * 5000 + 10).toFixed(2);
      
      transactions.push({
        amount: parseFloat(amount),
        merchant: merchantList[Math.floor(Math.random() * merchantList.length)],
        cardType: ['credit', 'debit'][Math.floor(Math.random() * 2)],
        customerId: `CUST_${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`,
        timestamp: new Date().toISOString()
      });
    }
    return transactions;
  };

  const analyzeTransactionRange = async () => {
    setRangeLoading(true);
    
    try {
      const transactions = generateRangeTransactions();
      const batchData = {
        transactions: transactions.map(transaction => ({
          transaction_data: {
            amount: transaction.amount,
            merchant: transaction.merchant,
            timestamp: transaction.timestamp,
            card_type: transaction.cardType,
            customer_id: transaction.customerId
          },
          model_type: formData.modelType
        })),
        model_type: formData.modelType,
        include_explanations: false
      };

      const response = await fraudAPI.predictFraudBatch(batchData);
      
      const results = response.predictions.map((prediction, index) => ({
        ...transactions[index],
        ...prediction
      }));

      setRangeResults(results);
      toast.success(`Analyzed ${results.length} transactions in range`);
    } catch (error) {
      console.error('Range analysis error:', error);
      toast.error(`Failed to analyze transaction range: ${error.message}`);
    } finally {
      setRangeLoading(false);
    }
  };

  return (
    <div className="fraud-detection">
      <div className="page-header">
        <div className="header-content">
          <Shield className="header-icon" />
          <div>
            <h1>Fraud Detection</h1>
            <p>Analyze individual transactions for fraud risk using advanced ML models</p>
          </div>
        </div>
      </div>

      <div className="detection-layout">
        {/* Transaction Form */}
        <div className="form-section">
          <div className="section-header">
            <CreditCard size={20} />
            <h2>Transaction Details</h2>
          </div>
          
          <form onSubmit={handleSubmit} className="transaction-form">
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">
                  <DollarSign size={16} />
                  Transaction Amount *
                </label>
                <input
                  type="number"
                  name="amount"
                  value={formData.amount}
                  onChange={handleInputChange}
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  className="form-input"
                  required
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">
                  <MapPin size={16} />
                  Merchant Name *
                </label>
                <input
                  type="text"
                  name="merchant"
                  value={formData.merchant}
                  onChange={handleInputChange}
                  placeholder="e.g., Amazon, Walmart, Gas Station"
                  className="form-input"
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">
                  <CreditCard size={16} />
                  Card Type
                </label>
                <select
                  name="cardType"
                  value={formData.cardType}
                  onChange={handleInputChange}
                  className="form-input form-select"
                >
                  <option value="credit">Credit Card</option>
                  <option value="debit">Debit Card</option>
                  <option value="prepaid">Prepaid Card</option>
                </select>
              </div>
              
              <div className="form-group">
                <label className="form-label">
                  <User size={16} />
                  Customer ID
                </label>
                <input
                  type="text"
                  name="customerId"
                  value={formData.customerId}
                  onChange={handleInputChange}
                  placeholder="e.g., CUST_12345"
                  className="form-input"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">
                  <BarChart3 size={16} />
                  ML Model
                </label>
                <select
                  name="modelType"
                  value={formData.modelType}
                  onChange={handleInputChange}
                  className="form-input form-select"
                >
                  <option value="xgboost">XGBoost (Recommended)</option>
                  <option value="isolation_forest">Isolation Forest</option>
                </select>
              </div>
              
              <div className="form-group checkbox-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="explain"
                    checked={formData.explain}
                    onChange={handleInputChange}
                    className="checkbox-input"
                  />
                  <span className="checkbox-custom"></span>
                  Include explanation
                </label>
              </div>
            </div>

            <div className="form-actions">
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary btn-lg"
              >
                {loading ? (
                  <>
                    <div className="spinner"></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Zap size={20} />
                    Analyze Transaction
                  </>
                )}
              </button>
              
              <button
                type="button"
                onClick={handleGenerateMock}
                className="btn btn-secondary"
              >
                Generate Mock Data
              </button>
              
              <button
                type="button"
                onClick={handleClear}
                className="btn btn-ghost"
              >
                Clear Form
              </button>
            </div>
          </form>
        </div>

        {/* Transaction Range Analysis */}
        <div className="form-section">
          <div className="section-header">
            <FileText size={20} />
            <h2>Transaction Range Analysis</h2>
            <div className="section-toggle">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={rangeMode}
                  onChange={(e) => setRangeMode(e.target.checked)}
                  className="toggle-input"
                />
                <span className="toggle-slider"></span>
                Enable Range Mode
              </label>
            </div>
          </div>
          
          {rangeMode && (
            <div className="range-form">
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">
                    <DollarSign size={16} />
                    Amount Range
                  </label>
                  <div className="range-inputs">
                    <input
                      type="number"
                      name="startAmount"
                      value={rangeData.startAmount}
                      onChange={handleRangeInputChange}
                      placeholder="Min (e.g., 100)"
                      step="0.01"
                      min="0"
                      className="form-input range-input"
                    />
                    <span className="range-separator">to</span>
                    <input
                      type="number"
                      name="endAmount"
                      value={rangeData.endAmount}
                      onChange={handleRangeInputChange}
                      placeholder="Max (e.g., 5000)"
                      step="0.01"
                      min="0"
                      className="form-input range-input"
                    />
                  </div>
                </div>
                
                <div className="form-group">
                  <label className="form-label">
                    <MapPin size={16} />
                    Merchants (Optional)
                  </label>
                  <input
                    type="text"
                    name="merchants"
                    value={rangeData.merchants}
                    onChange={handleRangeInputChange}
                    placeholder="e.g., Amazon, Walmart, Gas Station (comma-separated)"
                    className="form-input"
                  />
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">
                    <BarChart3 size={16} />
                    Number of Transactions
                  </label>
                  <input
                    type="number"
                    name="count"
                    value={rangeData.count}
                    onChange={handleRangeInputChange}
                    min="1"
                    max="100"
                    className="form-input"
                  />
                </div>
              </div>
              
              <div className="form-actions">
                <button
                  type="button"
                  onClick={analyzeTransactionRange}
                  disabled={rangeLoading}
                  className="btn btn-primary btn-lg"
                >
                  {rangeLoading ? (
                    <>
                      <div className="spinner"></div>
                      Analyzing Range...
                    </>
                  ) : (
                    <>
                      <Play size={20} />
                      Analyze Transaction Range
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Range Results */}
        {rangeResults.length > 0 && (
          <div className="results-section">
            <div className="section-header">
              <BarChart3 size={20} />
              <h2>Range Analysis Results ({rangeResults.length} transactions)</h2>
            </div>
            
            <div className="range-summary">
              <div className="summary-stats">
                <div className="stat-item">
                  <span className="stat-label">Total Analyzed</span>
                  <span className="stat-value">{rangeResults.length}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Fraud Detected</span>
                  <span className="stat-value fraud">
                    {rangeResults.filter(r => r.prediction === 'fraud').length}
                  </span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Fraud Rate</span>
                  <span className="stat-value">
                    {((rangeResults.filter(r => r.prediction === 'fraud').length / rangeResults.length) * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
            
            <div className="range-results-list">
              {rangeResults.map((result, index) => (
                <div key={index} className={`range-result-item ${result.prediction}`}>
                  <div className="result-info">
                    <div className="result-main">
                      <span className="amount">${result.amount.toFixed(2)}</span>
                      <span className="merchant">{result.merchant}</span>
                      <span className="customer">{result.customer_id}</span>
                    </div>
                    <div className="result-meta">
                      <span className={`prediction ${result.prediction}`}>
                        {result.prediction.toUpperCase()}
                      </span>
                      <span className="probability">
                        {(result.fraud_probability * 100).toFixed(1)}% risk
                      </span>
                    </div>
                  </div>
                  <div className="result-indicator">
                    {result.prediction === 'fraud' && <AlertTriangle size={16} />}
                    {result.prediction !== 'fraud' && <CheckCircle size={16} />}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="results-section">
            <div className="section-header">
              <Shield size={20} />
              <h2>Analysis Results</h2>
            </div>
            
            <div className="result-card">
              <div className="result-header">
                <div className="result-status">
                  <div className={`status-icon ${result.prediction}`}>
                    {result.prediction === 'fraud' && <AlertTriangle size={24} />}
                    {result.prediction === 'approve' && <CheckCircle size={24} />}
                    {result.prediction === 'review' && <Clock size={24} />}
                    {result.prediction === 'monitor' && <Shield size={24} />}
                  </div>
                  <div className="status-content">
                    <h3 className="status-title">
                      {interpretPrediction(result.prediction).message}
                    </h3>
                    <p className="case-id">Case ID: {result.case_id}</p>
                  </div>
                </div>
                <div className={`risk-badge ${getRiskLevelBadge(result.risk_level)}`}>
                  {result.risk_level.toUpperCase()} RISK
                </div>
              </div>

              <div className="result-metrics">
                <div className="metric-item">
                  <span className="metric-label">Fraud Probability</span>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill"
                      style={{ 
                        width: `${result.fraud_probability * 100}%`,
                        backgroundColor: result.fraud_probability > 0.6 ? 'var(--error)' : 
                                       result.fraud_probability > 0.3 ? 'var(--warning)' : 'var(--success)'
                      }}
                    ></div>
                    <span className="probability-text">
                      {(result.fraud_probability * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
                
                <div className="metric-item">
                  <span className="metric-label">Confidence</span>
                  <span className="metric-value">{(result.confidence * 100).toFixed(1)}%</span>
                </div>
                
                <div className="metric-item">
                  <span className="metric-label">Processing Time</span>
                  <span className="metric-value">{result.processing_time_ms}ms</span>
                </div>
                
                <div className="metric-item">
                  <span className="metric-label">Model Used</span>
                  <span className="metric-value">{result.model_used.toUpperCase()}</span>
                </div>
              </div>

              {result.explanation && (
                <div className="explanation-section">
                  <h4>Risk Factors</h4>
                  <div className="factors-list">
                    {result.explanation.top_factors?.map((factor, index) => (
                      <div key={index} className="factor-item">
                        <div className="factor-name">{factor.feature.replace('_', ' ')}</div>
                        <div className="factor-impact">
                          <div 
                            className="impact-bar"
                            style={{ 
                              width: `${Math.abs(factor.impact) * 100}%`,
                              backgroundColor: factor.impact > 0 ? 'var(--error)' : 'var(--success)'
                            }}
                          ></div>
                          <span className="impact-value">
                            {factor.impact > 0 ? '+' : ''}{(factor.impact * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                  {result.explanation.explanation_text && (
                    <p className="explanation-text">{result.explanation.explanation_text}</p>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* History Section */}
        {history.length > 0 && (
          <div className="history-section">
            <div className="section-header">
              <Clock size={20} />
              <h2>Recent Analyses</h2>
            </div>
            
            <div className="history-list">
              {history.map((item) => (
                <div key={item.id} className="history-item">
                  <div className="history-header">
                    <div className={`history-status ${item.result.prediction}`}>
                      {item.result.prediction === 'fraud' && <AlertTriangle size={16} />}
                      {item.result.prediction === 'approve' && <CheckCircle size={16} />}
                      {item.result.prediction === 'review' && <Clock size={16} />}
                      {item.result.prediction === 'monitor' && <Shield size={16} />}
                    </div>
                    <div className="history-details">
                      <span className="history-merchant">{item.transaction.merchant}</span>
                      <span className="history-amount">${item.transaction.amount}</span>
                    </div>
                    <div className="history-meta">
                      <span className={`history-risk ${getRiskLevelBadge(item.result.risk_level)}`}>
                        {item.result.risk_level}
                      </span>
                      <span className="history-time">
                        {new Date(item.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                  <div className="history-probability">
                    <div 
                      className="mini-probability-bar"
                      style={{ 
                        width: `${item.result.fraud_probability * 100}%`,
                        backgroundColor: item.result.fraud_probability > 0.6 ? 'var(--error)' : 
                                       item.result.fraud_probability > 0.3 ? 'var(--warning)' : 'var(--success)'
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FraudDetection;
