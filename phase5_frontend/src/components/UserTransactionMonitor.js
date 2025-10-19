import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  Calendar,
  DollarSign,
  MapPin,
  CreditCard,
  AlertTriangle,
  CheckCircle,
  Clock,
  RefreshCw,
  Eye,
  TrendingUp,
  TrendingDown
} from 'lucide-react';
import { generateUserTransactions } from '../utils/dataAccess';
import './UserTransactionMonitor.css';

const UserTransactionMonitor = ({ user }) => {
  const [transactions, setTransactions] = useState([]);
  const [filteredTransactions, setFilteredTransactions] = useState([]);
  const [filters, setFilters] = useState({
    search: '',
    dateRange: 'all',
    amountRange: 'all',
    category: 'all',
    fraudStatus: 'all'
  });
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState({
    total: 0,
    fraudulent: 0,
    totalAmount: 0,
    avgAmount: 0
  });

  // Generate user's transaction history
  useEffect(() => {
    if (user) {
      const userTransactions = generateUserTransactions(user, 50); // Generate 50 transactions
      setTransactions(userTransactions);
      setFilteredTransactions(userTransactions);
      calculateStats(userTransactions);
    }
  }, [user]);

  // Simulate real-time transaction updates (new transactions for the user)
  useEffect(() => {
    if (!user) return;

    const interval = setInterval(() => {
      // 20% chance of new transaction every 30 seconds
      if (Math.random() > 0.8) {
        const newTransaction = generateUserTransactions(user, 1)[0];
        newTransaction.id = `${user.username.toUpperCase()}_${Date.now()}_NEW`;
        newTransaction.timestamp = new Date().toISOString();
        newTransaction.isNew = true;

        setTransactions(prev => {
          const updated = [newTransaction, ...prev.slice(0, 49)]; // Keep max 50
          calculateStats(updated);
          return updated;
        });

        // Remove "new" status after 10 seconds
        setTimeout(() => {
          setTransactions(prev => 
            prev.map(t => 
              t.id === newTransaction.id 
                ? { ...t, isNew: false }
                : t
            )
          );
        }, 10000);
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [user]);

  // Apply filters whenever filters or transactions change
  useEffect(() => {
    applyFilters();
  }, [filters, transactions]);

  const calculateStats = (txns) => {
    const total = txns.length;
    const fraudulent = txns.filter(t => t.is_fraud).length;
    const totalAmount = txns.reduce((sum, t) => sum + t.amount, 0);
    const avgAmount = total > 0 ? totalAmount / total : 0;

    setStats({ total, fraudulent, totalAmount, avgAmount });
  };

  const applyFilters = () => {
    let filtered = [...transactions];

    // Search filter
    if (filters.search) {
      filtered = filtered.filter(t => 
        t.merchant.toLowerCase().includes(filters.search.toLowerCase()) ||
        t.location.toLowerCase().includes(filters.search.toLowerCase()) ||
        t.id.toLowerCase().includes(filters.search.toLowerCase())
      );
    }

    // Date range filter
    if (filters.dateRange !== 'all') {
      const now = new Date();
      let cutoffDate;
      
      switch (filters.dateRange) {
        case 'today':
          cutoffDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
          break;
        case 'week':
          cutoffDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
          break;
        case 'month':
          cutoffDate = new Date(now.getFullYear(), now.getMonth(), 1);
          break;
        default:
          cutoffDate = new Date(0);
      }
      
      filtered = filtered.filter(t => new Date(t.timestamp) >= cutoffDate);
    }

    // Amount range filter
    if (filters.amountRange !== 'all') {
      switch (filters.amountRange) {
        case 'small':
          filtered = filtered.filter(t => t.amount < 100);
          break;
        case 'medium':
          filtered = filtered.filter(t => t.amount >= 100 && t.amount < 500);
          break;
        case 'large':
          filtered = filtered.filter(t => t.amount >= 500);
          break;
      }
    }

    // Fraud status filter
    if (filters.fraudStatus !== 'all') {
      filtered = filtered.filter(t => 
        filters.fraudStatus === 'fraud' ? t.is_fraud : !t.is_fraud
      );
    }

    setFilteredTransactions(filtered);
  };

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  const refreshTransactions = () => {
    setIsLoading(true);
    setTimeout(() => {
      const refreshedTransactions = generateUserTransactions(user, 50);
      setTransactions(refreshedTransactions);
      setFilteredTransactions(refreshedTransactions);
      calculateStats(refreshedTransactions);
      setIsLoading(false);
    }, 1000);
  };

  const formatAmount = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const getTransactionIcon = (transaction) => {
    if (transaction.is_fraud) {
      return <AlertTriangle size={16} className="fraud-icon" />;
    }
    return <CheckCircle size={16} className="safe-icon" />;
  };

  if (!user) {
    return <div className="user-monitor-error">Please log in to view your transactions.</div>;
  }

  return (
    <div className="user-transaction-monitor">
      <div className="monitor-header">
        <div className="header-content">
          <h2>My Transaction History</h2>
          <p>Real-time view of your account activity</p>
        </div>
        <button 
          className={`refresh-btn ${isLoading ? 'loading' : ''}`}
          onClick={refreshTransactions}
          disabled={isLoading}
        >
          <RefreshCw size={16} />
          {isLoading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <CreditCard size={20} />
          </div>
          <div className="stat-content">
            <span className="stat-value">{stats.total}</span>
            <span className="stat-label">Total Transactions</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon fraud">
            <AlertTriangle size={20} />
          </div>
          <div className="stat-content">
            <span className="stat-value">{stats.fraudulent}</span>
            <span className="stat-label">Fraud Alerts</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">
            <DollarSign size={20} />
          </div>
          <div className="stat-content">
            <span className="stat-value">{formatAmount(stats.totalAmount)}</span>
            <span className="stat-label">Total Amount</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp size={20} />
          </div>
          <div className="stat-content">
            <span className="stat-value">{formatAmount(stats.avgAmount)}</span>
            <span className="stat-label">Average Amount</span>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="filters-section">
        <div className="search-box">
          <Search size={16} />
          <input
            type="text"
            placeholder="Search transactions..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
          />
        </div>
        
        <div className="filter-controls">
          <select
            value={filters.dateRange}
            onChange={(e) => handleFilterChange('dateRange', e.target.value)}
          >
            <option value="all">All Time</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>

          <select
            value={filters.amountRange}
            onChange={(e) => handleFilterChange('amountRange', e.target.value)}
          >
            <option value="all">All Amounts</option>
            <option value="small">Under $100</option>
            <option value="medium">$100 - $500</option>
            <option value="large">Over $500</option>
          </select>

          <select
            value={filters.fraudStatus}
            onChange={(e) => handleFilterChange('fraudStatus', e.target.value)}
          >
            <option value="all">All Transactions</option>
            <option value="safe">Safe Only</option>
            <option value="fraud">Fraud Alerts Only</option>
          </select>
        </div>
      </div>

      {/* Transaction List */}
      <div className="transactions-list">
        {filteredTransactions.length === 0 ? (
          <div className="empty-state">
            <Eye size={48} />
            <h3>No transactions found</h3>
            <p>Try adjusting your filters or check back later for new activity.</p>
          </div>
        ) : (
          filteredTransactions.map((transaction) => (
            <div 
              key={transaction.id} 
              className={`transaction-item ${transaction.is_fraud ? 'fraud' : 'safe'} ${transaction.isNew ? 'new' : ''}`}
            >
              <div className="transaction-icon">
                {getTransactionIcon(transaction)}
              </div>
              
              <div className="transaction-details">
                <div className="transaction-main">
                  <h4 className="merchant-name">{transaction.merchant}</h4>
                  <span className="transaction-amount">
                    {formatAmount(transaction.amount)}
                  </span>
                </div>
                
                <div className="transaction-meta">
                  <span className="transaction-location">
                    <MapPin size={12} />
                    {transaction.location}
                  </span>
                  <span className="transaction-card">
                    <CreditCard size={12} />
                    {transaction.card_type}
                  </span>
                  <span className="transaction-time">
                    <Clock size={12} />
                    {formatTimestamp(transaction.timestamp)}
                  </span>
                </div>
                
                {transaction.is_fraud && (
                  <div className="fraud-alert">
                    <AlertTriangle size={14} />
                    <span>Fraud Alert - Please verify this transaction</span>
                  </div>
                )}
              </div>
              
              {transaction.isNew && (
                <div className="new-badge">NEW</div>
              )}
            </div>
          ))
        )}
      </div>

      <div className="monitor-footer">
        <p>Showing {filteredTransactions.length} of {transactions.length} transactions</p>
        <p>Last updated: {new Date().toLocaleTimeString()}</p>
      </div>
    </div>
  );
};

export default UserTransactionMonitor;
