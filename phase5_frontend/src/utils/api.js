import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    // Add auth token (demo token for now)
    config.headers.Authorization = 'Bearer demo_token_123';
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle responses and errors
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    const errorMessage = error.response?.data?.detail || error.message || 'An error occurred';
    console.error('API Error:', errorMessage);
    return Promise.reject({
      message: errorMessage,
      status: error.response?.status,
      data: error.response?.data,
    });
  }
);

// API endpoints
export const fraudAPI = {
  // Health check
  healthCheck: () => api.get('/health'),
  
  // API info
  getApiInfo: () => api.get('/'),
  
  // Single fraud prediction
  predictFraud: (transactionData) => 
    api.post('/api/fraud/predict', transactionData),
  
  // Batch fraud prediction
  predictFraudBatch: (batchData) => 
    api.post('/api/fraud/predict/batch', batchData),
  
  // Model status
  getModelStatus: () => api.get('/api/models/status'),
  
  // Reload models
  reloadModels: () => api.post('/api/models/reload'),
  
  // File upload for real-time monitoring
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/upload/file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // Real-time monitoring endpoints
  startMonitoring: (fileId, processingSpeedMs = 1000) => {
    const formData = new FormData();
    formData.append('file_id', fileId);
    formData.append('processing_speed_ms', processingSpeedMs);
    return api.post('/api/monitoring/start', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  getMonitoringStatus: (sessionId) => 
    api.get(`/api/monitoring/status/${sessionId}`),
  
  controlMonitoring: (sessionId, action) => {
    const formData = new FormData();
    formData.append('action', action);
    return api.post(`/api/monitoring/control/${sessionId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  getFraudAlerts: (limit = 50) => 
    api.get(`/api/monitoring/alerts?limit=${limit}`),
  
  getMonitoringSessions: () => 
    api.get('/api/monitoring/sessions'),
};

// Helper functions for data formatting
export const formatTransactionData = (formData) => {
  return {
    transaction_data: {
      amount: parseFloat(formData.amount),
      merchant: formData.merchant,
      timestamp: formData.timestamp || new Date().toISOString(),
      card_type: formData.cardType || 'credit',
      customer_id: formData.customerId || `CUST_${Date.now()}`,
      features: formData.features || {},
    },
    customer_data: formData.customerData ? {
      customer_id: formData.customerData.customerId,
      risk_profile: formData.customerData.riskProfile || 'medium',
      age_group: formData.customerData.ageGroup || 'unknown',
      location: formData.customerData.location || 'unknown',
    } : undefined,
    model_type: formData.modelType || 'xgboost',
    explain: formData.explain || false,
  };
};

export const formatBatchData = (transactions) => {
  return {
    transactions: transactions.map(transaction => ({
      transaction_data: {
        amount: parseFloat(transaction.amount),
        merchant: transaction.merchant,
        timestamp: transaction.timestamp || new Date().toISOString(),
        card_type: transaction.cardType || 'credit',
        customer_id: transaction.customerId || `CUST_${Date.now()}`,
        features: transaction.features || {},
      },
      model_type: transaction.modelType || 'xgboost',
    })),
    model_type: 'xgboost',
    include_explanations: false,
  };
};

// Risk level mapping
export const getRiskLevelColor = (riskLevel) => {
  const colors = {
    minimal: 'var(--success)',
    low: 'var(--info)',
    medium: 'var(--warning)',
    high: 'var(--error)',
    critical: 'var(--error)',
  };
  return colors[riskLevel] || 'var(--text-muted)';
};

export const getRiskLevelBadge = (riskLevel) => {
  const badges = {
    minimal: 'badge-success',
    low: 'badge-info',
    medium: 'badge-warning',
    high: 'badge-error',
    critical: 'badge-error',
  };
  return badges[riskLevel] || 'badge-info';
};

// Prediction interpretation
export const interpretPrediction = (prediction) => {
  const interpretations = {
    approve: {
      message: 'Transaction approved - Low fraud risk',
      icon: '✅',
      color: 'var(--success)',
    },
    monitor: {
      message: 'Transaction flagged for monitoring',
      icon: '👁️',
      color: 'var(--info)',
    },
    review: {
      message: 'Transaction requires manual review',
      icon: '⚠️',
      color: 'var(--warning)',
    },
    fraud: {
      message: 'Transaction blocked - High fraud risk',
      icon: '🚨',
      color: 'var(--error)',
    },
    error: {
      message: 'Error processing transaction',
      icon: '❌',
      color: 'var(--error)',
    },
  };
  return interpretations[prediction] || interpretations.error;
};

// Mock data generators for testing
export const generateMockTransaction = () => {
  const merchants = [
    'Amazon', 'Walmart', 'Target', 'Starbucks', 'McDonald\'s',
    'Shell Gas Station', 'Best Buy', 'Home Depot', 'Grocery Store',
    'Online Electronics', 'Cash Advance ATM', 'Luxury Store'
  ];
  
  const cardTypes = ['credit', 'debit', 'prepaid'];
  
  return {
    amount: (Math.random() * 5000 + 10).toFixed(2),
    merchant: merchants[Math.floor(Math.random() * merchants.length)],
    timestamp: new Date().toISOString(),
    cardType: cardTypes[Math.floor(Math.random() * cardTypes.length)],
    customerId: `CUST_${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`,
    features: {
      V1: (Math.random() - 0.5) * 4,
      V2: (Math.random() - 0.5) * 4,
      V3: (Math.random() - 0.5) * 4,
      V4: (Math.random() - 0.5) * 4,
    },
  };
};

export const generateMockBatch = (count = 5) => {
  return Array.from({ length: count }, () => generateMockTransaction());
};

export default api;
