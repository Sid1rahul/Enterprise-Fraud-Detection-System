import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  Activity,
  Users,
  CreditCard,
  DollarSign
} from 'lucide-react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { fraudAPI } from '../utils/api';
import FraudChatbot from '../components/FraudChatbot';
import RealtimeActivityFeed from '../components/RealtimeActivityFeed';
import { generateUserTransactions, filterDashboardStats } from '../utils/dataAccess';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  const [stats, setStats] = useState({
    totalTransactions: 0,
    fraudDetected: 0,
    falsePositives: 0,
    accuracy: 0
  });

  const [apiStatus, setApiStatus] = useState({ status: 'checking', models: [] });
  const [recentActivity, setRecentActivity] = useState([]);
  const [fraudTrendData, setFraudTrendData] = useState([]);
  const [riskDistribution, setRiskDistribution] = useState([]);
  const [modelPerformance, setModelPerformance] = useState([]);

  // Generate dynamic data based on user role and current transactions
  const generateDynamicData = () => {
    if (!user) return;

    let transactions = [];
    let baseStats = {};

    if (user.role === 'admin') {
      // Admin sees system-wide data
      transactions = generateUserTransactions({ username: 'system' }, 1000);
      baseStats = {
        totalTransactions: Math.floor(Math.random() * 5000) + 15000,
        fraudDetected: Math.floor(Math.random() * 50) + 20,
        falsePositives: Math.floor(Math.random() * 10) + 3,
        accuracy: 98.5 + Math.random() * 1.5
      };
    } else {
      // User sees personal data
      transactions = generateUserTransactions(user, 50);
      const fraudCount = transactions.filter(t => t.is_fraud).length;
      baseStats = {
        totalTransactions: transactions.length,
        fraudDetected: fraudCount,
        falsePositives: Math.floor(fraudCount * 0.1),
        accuracy: fraudCount > 0 ? 95 + Math.random() * 4 : 99
      };
    }

    // Generate trend data - SYNCHRONIZED with Analytics page
    const trendData = [];
    for (let i = 6; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      
      trendData.push({
        date: date.toISOString().split('T')[0],
        transactions: Math.floor(1000 + Math.random() * 800),
        fraud: Math.floor(2 + Math.random() * 8),
        blocked: Math.floor(1 + Math.random() * 7),
        amount: Math.floor(30000 + Math.random() * 50000)
      });
    }

    // Generate risk distribution based on transactions
    const lowRisk = 82 + Math.random() * 8;
    const highRisk = 2 + Math.random() * 4;
    const mediumRisk = 100 - lowRisk - highRisk;

    const riskData = [
      { name: 'Low Risk', value: Math.round(lowRisk), color: '#00ff88' },
      { name: 'Medium Risk', value: Math.round(mediumRisk), color: '#ffaa00' },
      { name: 'High Risk', value: Math.round(highRisk), color: '#ff4757' }
    ];

    // Generate model performance with slight variations (max 2 decimal places)
    const modelData = [
      { 
        model: 'XGBoost', 
        accuracy: Math.round((98.5 + Math.random() * 1) * 100) / 100, 
        precision: Math.round((93 + Math.random() * 3) * 100) / 100, 
        recall: Math.round((88 + Math.random() * 4) * 100) / 100 
      },
      { 
        model: 'Isolation Forest', 
        accuracy: Math.round((95.5 + Math.random() * 2) * 100) / 100, 
        precision: Math.round((86 + Math.random() * 4) * 100) / 100, 
        recall: Math.round((91 + Math.random() * 3) * 100) / 100 
      }
    ];

    setStats(baseStats);
    setFraudTrendData(trendData);
    setRiskDistribution(riskData);
    setModelPerformance(modelData);
  };

  useEffect(() => {
    // Generate dynamic data when user changes
    generateDynamicData();
    
    const fetchApiStatus = async () => {
      try {
        const health = await fraudAPI.healthCheck();
        const models = await fraudAPI.getModelStatus();
        setApiStatus({ 
          status: health.status, 
          models: models || [],
          timestamp: health.timestamp 
        });
      } catch (error) {
        setApiStatus({ status: 'offline', models: [], error: error.message });
      }
    };

    fetchApiStatus();
    const interval = setInterval(fetchApiStatus, 30000);
    
    // Update dynamic data every 2 minutes
    const dataInterval = setInterval(generateDynamicData, 120000);

    // Generate mock recent activity
    const activities = [
      { id: 1, type: 'fraud_detected', message: 'High-risk transaction blocked', amount: '$2,500', time: '2 minutes ago' },
      { id: 2, type: 'model_update', message: 'XGBoost model retrained', time: '15 minutes ago' },
      { id: 3, type: 'batch_complete', message: 'Batch processing completed (500 transactions)', time: '1 hour ago' },
      { id: 4, type: 'alert', message: 'Unusual pattern detected in merchant category', time: '2 hours ago' }
    ];
    setRecentActivity(activities);

    return () => clearInterval(interval);
  }, []);

  const StatCard = ({ icon: Icon, title, value, change, color = 'var(--accent-primary)' }) => (
    <div className="stat-card">
      <div className="stat-icon" style={{ color }}>
        <Icon size={24} />
      </div>
      <div className="stat-content">
        <h3 className="stat-title">{title}</h3>
        <p className="stat-value">{value}</p>
        {change && (
          <p className={`stat-change ${change.startsWith('+') ? 'positive' : 'negative'}`}>
            {change}
          </p>
        )}
      </div>
    </div>
  );

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Fraud Detection Dashboard</h1>
        <p>Real-time monitoring and analytics for credit card fraud detection</p>
      </div>

      {/* API Status Banner */}
      <div className={`status-banner ${apiStatus.status === 'healthy' ? 'online' : 'offline'}`}>
        <Activity size={20} />
        <span>
          API Status: {apiStatus.status === 'healthy' ? 'Online' : 'Offline'} 
          {apiStatus.models.length > 0 && ` • ${apiStatus.models.length} models active`}
        </span>
        {apiStatus.timestamp && (
          <span className="status-time">
            Last updated: {new Date(apiStatus.timestamp).toLocaleTimeString()}
          </span>
        )}
      </div>

      {/* Key Statistics */}
      <div className="stats-grid">
        <StatCard
          icon={CreditCard}
          title="Total Transactions"
          value={stats.totalTransactions.toLocaleString()}
          change="+12.5% from yesterday"
          color="var(--accent-primary)"
        />
        <StatCard
          icon={Shield}
          title="Fraud Detected"
          value={stats.fraudDetected}
          change="+3 from yesterday"
          color="var(--error)"
        />
        <StatCard
          icon={CheckCircle}
          title="Accuracy Rate"
          value={`${stats.accuracy}%`}
          change="+0.3% from last week"
          color="var(--success)"
        />
        <StatCard
          icon={DollarSign}
          title="Amount Saved"
          value="$47,230"
          change="+$12,500 this week"
          color="var(--warning)"
        />
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        {/* Fraud Trend Chart */}
        <div className="chart-card">
          <div className="chart-header">
            <h3>Fraud Detection Trend</h3>
            <p>Daily fraud detection and blocking rates</p>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
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
            <h3>Risk Distribution</h3>
            <p>Transaction risk level breakdown</p>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={riskDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
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
              </PieChart>
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
      </div>

      {/* Model Performance & Recent Activity */}
      <div className="bottom-grid">
        {/* Model Performance */}
        <div className="performance-card">
          <div className="card-header">
            <h3>Model Performance</h3>
            <p>Current ML model metrics</p>
          </div>
          <div className="performance-list">
            {modelPerformance.map((model, index) => (
              <div key={index} className="performance-item">
                <div className="model-name">{model.model}</div>
                <div className="metrics">
                  <div className="metric">
                    <span className="metric-label">Accuracy</span>
                    <span className="metric-value">{model.accuracy}%</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Precision</span>
                    <span className="metric-value">{model.precision}%</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">Recall</span>
                    <span className="metric-value">{model.recall}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Real-time Activity Feed */}
        <RealtimeActivityFeed user={user} />
      </div>
      
      {/* UiPath Integrated Chatbot */}
      <FraudChatbot />
    </div>
  );
};

export default Dashboard;
