import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  PieChart, 
  Calendar,
  Download,
  Filter,
  RefreshCw
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  PieChart as RechartsPieChart, 
  Pie, 
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import './Analytics.css';

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7d');
  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  // Mock data for charts
  const fraudTrendData = [
    { date: '2024-01-01', transactions: 1200, fraud: 3, blocked: 2, amount: 45000 },
    { date: '2024-01-02', transactions: 1350, fraud: 5, blocked: 4, amount: 52000 },
    { date: '2024-01-03', transactions: 1100, fraud: 2, blocked: 2, amount: 38000 },
    { date: '2024-01-04', transactions: 1450, fraud: 7, blocked: 6, amount: 67000 },
    { date: '2024-01-05', transactions: 1600, fraud: 4, blocked: 3, amount: 58000 },
    { date: '2024-01-06', transactions: 1300, fraud: 6, blocked: 5, amount: 49000 },
    { date: '2024-01-07', transactions: 1800, fraud: 8, blocked: 7, amount: 72000 }
  ];

  const merchantRiskData = [
    { merchant: 'Online Electronics', risk: 8.5, transactions: 450, fraudCount: 12 },
    { merchant: 'Cash Advance', risk: 9.2, transactions: 120, fraudCount: 8 },
    { merchant: 'Gas Stations', risk: 2.1, transactions: 890, fraudCount: 3 },
    { merchant: 'Grocery Stores', risk: 1.5, transactions: 1200, fraudCount: 2 },
    { merchant: 'Restaurants', risk: 2.8, transactions: 670, fraudCount: 4 },
    { merchant: 'ATM Withdrawals', risk: 6.7, transactions: 340, fraudCount: 9 }
  ];

  const hourlyPatternData = [
    { hour: '00', normal: 45, fraud: 8 },
    { hour: '02', normal: 23, fraud: 12 },
    { hour: '04', normal: 18, fraud: 15 },
    { hour: '06', normal: 67, fraud: 5 },
    { hour: '08', normal: 156, fraud: 3 },
    { hour: '10', normal: 234, fraud: 2 },
    { hour: '12', normal: 289, fraud: 4 },
    { hour: '14', normal: 267, fraud: 3 },
    { hour: '16', normal: 245, fraud: 5 },
    { hour: '18', normal: 198, fraud: 7 },
    { hour: '20', normal: 167, fraud: 9 },
    { hour: '22', normal: 123, fraud: 11 }
  ];

  const modelPerformanceData = [
    { metric: 'Accuracy', xgboost: 98.7, isolation_forest: 96.3, ensemble: 99.1 },
    { metric: 'Precision', xgboost: 94.2, isolation_forest: 87.5, ensemble: 95.8 },
    { metric: 'Recall', xgboost: 89.1, isolation_forest: 92.8, ensemble: 91.5 },
    { metric: 'F1-Score', xgboost: 91.5, isolation_forest: 90.1, ensemble: 93.6 },
    { metric: 'AUC', xgboost: 97.3, isolation_forest: 94.8, ensemble: 98.2 }
  ];

  const riskDistribution = [
    { name: 'Low Risk', value: 85, color: '#00ff88' },
    { name: 'Medium Risk', value: 12, color: '#ffaa00' },
    { name: 'High Risk', value: 3, color: '#ff4757' }
  ];

  const handleRefresh = async () => {
    setRefreshing(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setRefreshing(false);
  };

  const refreshData = async () => {
    setRefreshing(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Update timestamp and potentially fetch new data
    setLastUpdated(new Date());
    setRefreshing(false);
  };

  const exportData = () => {
    const csvContent = [
      ['Date', 'Transactions', 'Fraud Detected', 'Blocked', 'Amount'],
      ...fraudTrendData.map(row => [
        row.date,
        row.transactions,
        row.fraud,
        row.blocked,
        row.amount
      ])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fraud_analytics_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="analytics">
      <div className="page-header">
        <div className="header-content">
          <BarChart3 className="header-icon" />
          <div>
            <h1>Analytics & Reports</h1>
            <p>Comprehensive insights and performance metrics for fraud detection</p>
          </div>
        </div>
        
        <div className="header-controls">
          <div className="time-range-selector">
            <select 
              value={timeRange} 
              onChange={(e) => setTimeRange(e.target.value)}
              className="form-input form-select"
            >
              <option value="1d">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
            </select>
          </div>
          
          <div className="refresh-info">
            <div className="last-updated">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </div>
            <button 
              onClick={refreshData} 
              disabled={refreshing}
              className="btn btn-secondary"
            >
              <RefreshCw size={20} className={refreshing ? 'spinning' : ''} />
              {refreshing ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
          <button onClick={exportData} className="btn btn-primary">
            <Download size={20} />
            Export
          </button>
        </div>
      </div>

      <div className="analytics-grid">
        {/* Fraud Trend Analysis */}
        <div className="chart-card large">
          <div className="chart-header">
            <div className="header-info">
              <TrendingUp size={20} />
              <div>
                <h3>Fraud Detection Trends</h3>
                <p>Daily fraud detection and prevention metrics</p>
              </div>
            </div>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={350}>
              <AreaChart data={fraudTrendData}>
                <defs>
                  <linearGradient id="fraudGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--error)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--error)" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="blockedGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--success)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--success)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="date" stroke="var(--text-muted)" />
                <YAxis stroke="var(--text-muted)" />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'var(--bg-card)',
                    border: '1px solid var(--accent-primary)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)'
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="fraud"
                  stroke="var(--error)"
                  fillOpacity={1}
                  fill="url(#fraudGradient)"
                  name="Fraud Detected"
                />
                <Area
                  type="monotone"
                  dataKey="blocked"
                  stroke="var(--success)"
                  fillOpacity={1}
                  fill="url(#blockedGradient)"
                  name="Successfully Blocked"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Distribution */}
        <div className="chart-card">
          <div className="chart-header">
            <div className="header-info">
              <PieChart size={20} />
              <div>
                <h3>Risk Distribution</h3>
                <p>Transaction risk levels</p>
              </div>
            </div>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <RechartsPieChart>
                <Pie
                  data={riskDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {riskDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'var(--bg-card)',
                    border: '1px solid var(--accent-primary)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)'
                  }}
                />
              </RechartsPieChart>
            </ResponsiveContainer>
            <div className="pie-legend">
              {riskDistribution.map((item, index) => (
                <div key={index} className="legend-item">
                  <div className="legend-color" style={{ backgroundColor: item.color }}></div>
                  <span>{item.name}: {item.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Merchant Risk Analysis */}
        <div className="chart-card">
          <div className="chart-header">
            <div className="header-info">
              <BarChart3 size={20} />
              <div>
                <h3>Merchant Risk Analysis</h3>
                <p>Risk levels by merchant category</p>
              </div>
            </div>
          </div>
          <div className="merchant-risk-list">
            {merchantRiskData.map((merchant, index) => (
              <div key={index} className="merchant-item">
                <div className="merchant-info">
                  <span className="merchant-name">{merchant.merchant}</span>
                  <span className="merchant-stats">
                    {merchant.transactions} transactions • {merchant.fraudCount} fraud cases
                  </span>
                </div>
                <div className="risk-indicator">
                  <div className="risk-bar">
                    <div 
                      className="risk-fill"
                      style={{ 
                        width: `${merchant.risk * 10}%`,
                        backgroundColor: merchant.risk > 7 ? 'var(--error)' : 
                                       merchant.risk > 4 ? 'var(--warning)' : 'var(--success)'
                      }}
                    ></div>
                  </div>
                  <span className="risk-value">{merchant.risk}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Hourly Pattern Analysis */}
        <div className="chart-card">
          <div className="chart-header">
            <div className="header-info">
              <Calendar size={20} />
              <div>
                <h3>Hourly Fraud Patterns</h3>
                <p>Fraud occurrence by time of day</p>
              </div>
            </div>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={hourlyPatternData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="hour" stroke="var(--text-muted)" />
                <YAxis stroke="var(--text-muted)" />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'var(--bg-card)',
                    border: '1px solid var(--accent-primary)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)'
                  }}
                />
                <Bar dataKey="normal" fill="var(--success)" name="Normal Transactions" />
                <Bar dataKey="fraud" fill="var(--error)" name="Fraud Transactions" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Model Performance Comparison */}
        <div className="chart-card large">
          <div className="chart-header">
            <div className="header-info">
              <TrendingUp size={20} />
              <div>
                <h3>Model Performance Comparison</h3>
                <p>Comparative analysis of ML model metrics</p>
              </div>
            </div>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={modelPerformanceData}>
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis dataKey="metric" tick={{ fill: 'var(--text-muted)', fontSize: 12 }} />
                <PolarRadiusAxis 
                  angle={90} 
                  domain={[80, 100]} 
                  tick={{ fill: 'var(--text-muted)', fontSize: 10 }}
                />
                <Radar
                  name="XGBoost"
                  dataKey="xgboost"
                  stroke="var(--accent-primary)"
                  fill="var(--accent-primary)"
                  fillOpacity={0.1}
                  strokeWidth={2}
                />
                <Radar
                  name="Isolation Forest"
                  dataKey="isolation_forest"
                  stroke="var(--warning)"
                  fill="var(--warning)"
                  fillOpacity={0.1}
                  strokeWidth={2}
                />
                <Radar
                  name="Ensemble"
                  dataKey="ensemble"
                  stroke="var(--success)"
                  fill="var(--success)"
                  fillOpacity={0.1}
                  strokeWidth={2}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'var(--bg-card)',
                    border: '1px solid var(--accent-primary)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)'
                  }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          <div className="radar-legend">
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: 'var(--accent-primary)' }}></div>
              <span>XGBoost</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: 'var(--warning)' }}></div>
              <span>Isolation Forest</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: 'var(--success)' }}></div>
              <span>Ensemble</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
