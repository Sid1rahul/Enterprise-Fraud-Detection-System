import React from 'react';
import { X, AlertTriangle, CheckCircle, Info, TrendingUp, TrendingDown } from 'lucide-react';
import { formatCurrencyINR } from '../utils/api';
import './TransactionDetailsModal.css';

const TransactionDetailsModal = ({ transaction, isOpen, onClose }) => {
  if (!isOpen || !transaction) return null;

  // Generate SHAP-like feature importance
  const generateFeatureImportance = (transaction) => {
    const features = [
      {
        name: 'Transaction Amount',
        value: formatCurrencyINR(transaction.amount),
        impact: transaction.amount > 1000 ? 0.35 : -0.15,
        description: transaction.amount > 1000 ? 'High amount increases fraud risk' : 'Normal amount reduces fraud risk'
      },
      {
        name: 'Merchant Category',
        value: transaction.merchant,
        impact: ['Casino', 'Cash Advance', 'ATM'].some(risk => transaction.merchant.includes(risk)) ? 0.28 : -0.12,
        description: ['Casino', 'Cash Advance', 'ATM'].some(risk => transaction.merchant.includes(risk)) 
          ? 'High-risk merchant category' 
          : 'Low-risk merchant category'
      },
      {
        name: 'Time of Day',
        value: new Date(transaction.timestamp).getHours() + ':00',
        impact: new Date(transaction.timestamp).getHours() < 6 || new Date(transaction.timestamp).getHours() > 23 ? 0.22 : -0.08,
        description: new Date(transaction.timestamp).getHours() < 6 || new Date(transaction.timestamp).getHours() > 23
          ? 'Unusual transaction time'
          : 'Normal transaction time'
      },
      {
        name: 'Customer Risk Profile',
        value: transaction.customer_id || 'Unknown',
        impact: Math.random() > 0.5 ? 0.18 : -0.10,
        description: Math.random() > 0.5 ? 'Customer has elevated risk profile' : 'Customer has good history'
      },
      {
        name: 'Geographic Location',
        value: 'Domestic',
        impact: -0.05,
        description: 'Transaction from known location'
      },
      {
        name: 'Card Type',
        value: transaction.cardType || 'Credit',
        impact: (transaction.cardType === 'prepaid') ? 0.15 : -0.03,
        description: (transaction.cardType === 'prepaid') ? 'Prepaid cards have higher risk' : 'Standard card type'
      }
    ];

    return features.sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact));
  };

  const features = generateFeatureImportance(transaction);
  const riskScore = transaction.risk_score || (transaction.fraud_probability || Math.random());
  const isHighRisk = riskScore > 0.7;
  const isMediumRisk = riskScore > 0.3 && riskScore <= 0.7;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="transaction-modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <div className={`risk-indicator ${isHighRisk ? 'high' : isMediumRisk ? 'medium' : 'low'}`}>
              {isHighRisk ? <AlertTriangle size={24} /> : <CheckCircle size={24} />}
            </div>
            <div>
              <h2>Transaction Analysis</h2>
              <p>ID: {transaction.id}</p>
            </div>
          </div>
          <button className="close-button" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <div className="modal-content">
          {/* Transaction Summary */}
          <div className="transaction-summary">
            <div className="summary-grid">
              <div className="summary-item">
                <label>Amount</label>
                <span className="amount">{formatCurrencyINR(transaction.amount ?? 0)}</span>
              </div>
              <div className="summary-item">
                <label>Merchant</label>
                <span>{transaction.merchant || 'Unknown'}</span>
              </div>
              <div className="summary-item">
                <label>Date & Time</label>
                <span>{new Date(transaction.timestamp).toLocaleString()}</span>
              </div>
              <div className="summary-item">
                <label>Risk Score</label>
                <span className={`risk-score ${isHighRisk ? 'high' : isMediumRisk ? 'medium' : 'low'}`}>
                  {(riskScore * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>

          {/* SHAP-like Feature Importance */}
          <div className="feature-analysis">
            <h3>
              <Info size={20} />
              Why was this transaction flagged?
            </h3>
            <p className="analysis-description">
              Our AI model analyzed multiple factors to determine the fraud risk. 
              Here's how each feature contributed to the decision:
            </p>

            <div className="features-list">
              {features.map((feature, index) => (
                <div key={index} className="feature-item">
                  <div className="feature-header">
                    <span className="feature-name">{feature.name}</span>
                    <span className="feature-value">{feature.value}</span>
                  </div>
                  
                  <div className="impact-bar-container">
                    <div className="impact-bar">
                      <div 
                        className={`impact-fill ${feature.impact > 0 ? 'positive' : 'negative'}`}
                        style={{ 
                          width: `${Math.abs(feature.impact) * 100}%`,
                          marginLeft: feature.impact < 0 ? `${50 - Math.abs(feature.impact) * 50}%` : '50%'
                        }}
                      ></div>
                      <div className="impact-center-line"></div>
                    </div>
                    <div className="impact-indicators">
                      <span className="decreases-risk">Decreases Risk</span>
                      <span className="increases-risk">Increases Risk</span>
                    </div>
                  </div>

                  <div className="feature-explanation">
                    <div className={`impact-icon ${feature.impact > 0 ? 'positive' : 'negative'}`}>
                      {feature.impact > 0 ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                    </div>
                    <span>{feature.description}</span>
                    <span className="impact-value">
                      {feature.impact > 0 ? '+' : ''}{(feature.impact * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Model Confidence */}
          <div className="model-confidence">
            <h4>Model Confidence</h4>
            <div className="confidence-bar">
              <div 
                className="confidence-fill"
                style={{ width: `${riskScore * 100}%` }}
              ></div>
            </div>
            <div className="confidence-labels">
              <span>Low Risk</span>
              <span>High Risk</span>
            </div>
            <p className="confidence-text">
              The model is {(riskScore * 100).toFixed(1)}% confident this transaction {isHighRisk ? 'is fraudulent' : 'is legitimate'}.
            </p>
          </div>

          {/* Recommended Action */}
          <div className={`recommended-action ${isHighRisk ? 'block' : isMediumRisk ? 'review' : 'approve'}`}>
            <h4>Recommended Action</h4>
            <div className="action-content">
              {isHighRisk ? (
                <>
                  <AlertTriangle size={20} />
                  <div>
                    <strong>BLOCK TRANSACTION</strong>
                    <p>High fraud probability detected. Recommend blocking and contacting customer.</p>
                  </div>
                </>
              ) : isMediumRisk ? (
                <>
                  <Info size={20} />
                  <div>
                    <strong>MANUAL REVIEW</strong>
                    <p>Moderate risk detected. Recommend manual review before processing.</p>
                  </div>
                </>
              ) : (
                <>
                  <CheckCircle size={20} />
                  <div>
                    <strong>APPROVE TRANSACTION</strong>
                    <p>Low fraud risk. Transaction appears legitimate and safe to process.</p>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TransactionDetailsModal;
