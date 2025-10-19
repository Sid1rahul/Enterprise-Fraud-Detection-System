// Data Access Control Utility
// Implements role-based data filtering and access restrictions

export const USER_ROLES = {
  ADMIN: 'admin',
  USER: 'user'
};

export const PERMISSIONS = {
  VIEW_ALL_TRANSACTIONS: 'view_all_transactions',
  VIEW_OWN_TRANSACTIONS: 'view_own_transactions',
  MANAGE_SYSTEM: 'manage_system',
  EXPORT_DATA: 'export_data',
  USER_MANAGEMENT: 'user_management',
  BATCH_PROCESSING: 'batch_processing',
  REAL_TIME_MONITORING: 'real_time_monitoring',
  ANALYTICS_ADVANCED: 'analytics_advanced'
};

// Role-based permissions mapping
export const ROLE_PERMISSIONS = {
  [USER_ROLES.ADMIN]: [
    PERMISSIONS.VIEW_ALL_TRANSACTIONS,
    PERMISSIONS.MANAGE_SYSTEM,
    PERMISSIONS.EXPORT_DATA,
    PERMISSIONS.USER_MANAGEMENT,
    PERMISSIONS.BATCH_PROCESSING,
    PERMISSIONS.REAL_TIME_MONITORING,
    PERMISSIONS.ANALYTICS_ADVANCED
  ],
  [USER_ROLES.USER]: [
    PERMISSIONS.VIEW_OWN_TRANSACTIONS,
    PERMISSIONS.REAL_TIME_MONITORING
  ]
};

/**
 * Check if user has specific permission
 */
export const hasPermission = (user, permission) => {
  if (!user || !user.role) return false;
  
  const userPermissions = ROLE_PERMISSIONS[user.role] || [];
  return userPermissions.includes(permission);
};

/**
 * Filter transactions based on user role and permissions
 */
export const filterTransactionData = (transactions, user) => {
  if (!user || !transactions) return [];
  
  // Admin and Analyst can see all transactions
  if (hasPermission(user, PERMISSIONS.VIEW_ALL_TRANSACTIONS)) {
    return transactions;
  }
  
  // Regular users can only see their own transactions
  if (hasPermission(user, PERMISSIONS.VIEW_OWN_TRANSACTIONS)) {
    // Filter by user ID or customer ID
    return transactions.filter(transaction => 
      transaction.customer_id === user.username ||
      transaction.user_id === user.username ||
      transaction.created_by === user.username
    );
  }
  
  return [];
};

/**
 * Filter dashboard statistics based on user role
 */
export const filterDashboardStats = (stats, user) => {
  if (!user || !stats) return stats;
  
  // Admin sees all stats
  if (user.role === USER_ROLES.ADMIN) {
    return stats;
  }
  
  // Analyst sees most stats but not user management data
  if (user.role === USER_ROLES.ANALYST) {
    const { userCount, ...filteredStats } = stats;
    return filteredStats;
  }
  
  // Regular users see limited stats
  if (user.role === USER_ROLES.USER) {
    return {
      totalTransactions: stats.personalTransactions || 0,
      fraudDetected: stats.personalFraudDetected || 0,
      accuracy: stats.accuracy || 0,
      // Hide sensitive system-wide metrics
      falsePositives: undefined,
      systemHealth: undefined
    };
  }
  
  return {};
};

/**
 * Filter activity feed based on user role
 */
export const filterActivityFeed = (activities, user) => {
  if (!user || !activities) return [];
  
  // Admin sees all activities
  if (user.role === USER_ROLES.ADMIN) {
    return activities;
  }
  
  // Analyst sees fraud and system activities but not user activities
  if (user.role === USER_ROLES.ANALYST) {
    return activities.filter(activity => 
      !['user_activity', 'security_alert'].includes(activity.type)
    );
  }
  
  // Regular users see only fraud detection activities
  if (user.role === USER_ROLES.USER) {
    return activities.filter(activity => 
      ['fraud_detected', 'batch_complete'].includes(activity.type)
    );
  }
  
  return [];
};

/**
 * Generate user-specific sample transactions
 */
export const generateUserTransactions = (user, count = 10) => {
  const transactions = [];
  const userPrefix = user.username.toUpperCase();
  
  for (let i = 0; i < count; i++) {
    const amount = Math.floor(Math.random() * 2000) + 50;
    const merchants = ['Amazon', 'Walmart', 'Target', 'Starbucks', 'Gas Station', 'Restaurant', 'Grocery Store'];
    const merchant = merchants[Math.floor(Math.random() * merchants.length)];
    
    transactions.push({
      id: `${userPrefix}_${Date.now()}_${i}`,
      customer_id: user.username,
      amount: amount,
      merchant: merchant,
      timestamp: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
      card_type: Math.random() > 0.5 ? 'credit' : 'debit',
      location: 'Local',
      fraud_probability: Math.random(),
      is_fraud: Math.random() > 0.9, // 10% fraud rate
      user_id: user.username,
      created_by: user.username
    });
  }
  
  return transactions.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
};

/**
 * Check if user can access specific page/feature
 */
export const canAccessFeature = (user, feature) => {
  const featurePermissions = {
    'batch-processing': PERMISSIONS.BATCH_PROCESSING,
    'real-time-monitoring': PERMISSIONS.REAL_TIME_MONITORING,
    'analytics': PERMISSIONS.ANALYTICS_ADVANCED,
    'user-management': PERMISSIONS.USER_MANAGEMENT,
    'system-settings': PERMISSIONS.MANAGE_SYSTEM
  };
  
  const requiredPermission = featurePermissions[feature];
  return requiredPermission ? hasPermission(user, requiredPermission) : true;
};

/**
 * Get user-appropriate navigation items
 */
export const getNavigationItems = (user) => {
  const allItems = [
    { path: '/dashboard', label: 'Dashboard', icon: 'BarChart3', permission: null },
    { path: '/fraud-detection', label: 'Fraud Detection', icon: 'Shield', permission: null },
    { path: '/batch-processing', label: 'Batch Processing', icon: 'Layers', permission: PERMISSIONS.BATCH_PROCESSING },
    { path: '/real-time-monitoring', label: 'Real-Time Monitoring', icon: 'Activity', permission: PERMISSIONS.REAL_TIME_MONITORING },
    { path: '/analytics', label: 'Analytics', icon: 'TrendingUp', permission: PERMISSIONS.ANALYTICS_ADVANCED },
    { path: '/settings', label: 'Settings', icon: 'Settings', permission: PERMISSIONS.MANAGE_SYSTEM }
  ];
  
  return allItems.filter(item => 
    !item.permission || hasPermission(user, item.permission)
  );
};

/**
 * Sanitize sensitive data based on user role
 */
export const sanitizeData = (data, user, dataType) => {
  if (!user || !data) return data;
  
  switch (dataType) {
    case 'transaction':
      if (user.role === USER_ROLES.USER) {
        // Remove sensitive fields for regular users
        const { internal_notes, risk_factors, model_details, ...sanitized } = data;
        return sanitized;
      }
      return data;
      
    case 'user_info':
      if (user.role !== USER_ROLES.ADMIN) {
        // Non-admin users can't see other users' sensitive info
        const { email, phone, address, ...sanitized } = data;
        return sanitized;
      }
      return data;
      
    case 'system_metrics':
      if (user.role === USER_ROLES.USER) {
        // Regular users see limited system metrics
        const { cpu_usage, memory_usage, database_stats, ...sanitized } = data;
        return sanitized;
      }
      return data;
      
    default:
      return data;
  }
};

export default {
  USER_ROLES,
  PERMISSIONS,
  ROLE_PERMISSIONS,
  hasPermission,
  filterTransactionData,
  filterDashboardStats,
  filterActivityFeed,
  generateUserTransactions,
  canAccessFeature,
  getNavigationItems,
  sanitizeData
};
