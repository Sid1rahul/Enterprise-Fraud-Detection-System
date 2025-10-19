import React, { useState, useEffect, useRef } from 'react';
import { 
  Bell, 
  X, 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  Shield, 
  TrendingUp,
  Clock,
  Eye,
  Trash2
} from 'lucide-react';
import './NotificationCenter.css';

const NotificationCenter = ({ user }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const dropdownRef = useRef(null);

  // Sample notifications based on user role
  const generateNotifications = () => {
    const baseNotifications = [
      {
        id: 1,
        type: 'fraud_alert',
        title: 'High-Risk Transaction Detected',
        message: 'Transaction of $7,500 at Casino flagged with 95% fraud probability',
        timestamp: new Date(Date.now() - 5 * 60000).toISOString(),
        isRead: false,
        priority: 'high',
        data: { amount: 7500, merchant: 'Casino', riskScore: 0.95 }
      },
      {
        id: 2,
        type: 'system_update',
        title: 'Model Performance Update',
        message: 'XGBoost model accuracy improved to 96.2% after latest training',
        timestamp: new Date(Date.now() - 30 * 60000).toISOString(),
        isRead: false,
        priority: 'medium',
        data: { accuracy: 96.2, model: 'XGBoost' }
      },
      {
        id: 3,
        type: 'batch_complete',
        title: 'Batch Processing Complete',
        message: 'Successfully processed 150 transactions, 12 fraud cases detected',
        timestamp: new Date(Date.now() - 2 * 3600000).toISOString(),
        isRead: true,
        priority: 'low',
        data: { processed: 150, fraudDetected: 12 }
      }
    ];

    // Add role-specific notifications
    if (user?.role === 'admin') {
      baseNotifications.push(
        {
          id: 4,
          type: 'system_alert',
          title: 'System Health Check',
          message: 'All services operational. API response time: 45ms average',
          timestamp: new Date(Date.now() - 4 * 3600000).toISOString(),
          isRead: false,
          priority: 'low',
          data: { responseTime: 45, status: 'healthy' }
        },
        {
          id: 5,
          type: 'security_alert',
          title: 'New User Login',
          message: 'User "analyst" logged in from new location',
          timestamp: new Date(Date.now() - 6 * 3600000).toISOString(),
          isRead: true,
          priority: 'medium',
          data: { user: 'analyst', location: 'New York, NY' }
        }
      );
    }

    return baseNotifications.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  };

  useEffect(() => {
    const initialNotifications = generateNotifications();
    setNotifications(initialNotifications);
    setUnreadCount(initialNotifications.filter(n => !n.isRead).length);

    // Simulate real-time notifications
    const interval = setInterval(() => {
      if (Math.random() > 0.7) { // 30% chance every 30 seconds
        const newNotification = {
          id: Date.now(),
          type: Math.random() > 0.5 ? 'fraud_alert' : 'system_update',
          title: Math.random() > 0.5 ? 'New Fraud Alert' : 'System Update',
          message: Math.random() > 0.5 
            ? `Suspicious transaction of $${Math.floor(Math.random() * 5000 + 1000)} detected`
            : 'Model retrained with new data batch',
          timestamp: new Date().toISOString(),
          isRead: false,
          priority: Math.random() > 0.7 ? 'high' : 'medium',
          data: {}
        };

        setNotifications(prev => [newNotification, ...prev.slice(0, 19)]); // Keep max 20
        setUnreadCount(prev => prev + 1);
      }
    }, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, [user]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'fraud_alert':
        return <AlertTriangle size={16} />;
      case 'system_update':
        return <TrendingUp size={16} />;
      case 'batch_complete':
        return <CheckCircle size={16} />;
      case 'system_alert':
        return <Shield size={16} />;
      case 'security_alert':
        return <Shield size={16} />;
      default:
        return <Info size={16} />;
    }
  };

  const getPriorityClass = (priority) => {
    switch (priority) {
      case 'high':
        return 'priority-high';
      case 'medium':
        return 'priority-medium';
      case 'low':
        return 'priority-low';
      default:
        return 'priority-medium';
    }
  };

  const formatTimestamp = (timestamp) => {
    const now = new Date();
    const notificationTime = new Date(timestamp);
    const diffInMinutes = Math.floor((now - notificationTime) / (1000 * 60));

    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  const markAsRead = (notificationId) => {
    setNotifications(prev =>
      prev.map(notification =>
        notification.id === notificationId
          ? { ...notification, isRead: true }
          : notification
      )
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const markAllAsRead = () => {
    setNotifications(prev =>
      prev.map(notification => ({ ...notification, isRead: true }))
    );
    setUnreadCount(0);
  };

  const deleteNotification = (notificationId) => {
    setNotifications(prev => {
      const notification = prev.find(n => n.id === notificationId);
      if (notification && !notification.isRead) {
        setUnreadCount(count => Math.max(0, count - 1));
      }
      return prev.filter(n => n.id !== notificationId);
    });
  };

  const clearAllNotifications = () => {
    setNotifications([]);
    setUnreadCount(0);
  };

  return (
    <div className="notification-center" ref={dropdownRef}>
      <button
        className="notification-trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Notifications"
      >
        <Bell size={20} />
        {unreadCount > 0 && (
          <span className="notification-badge">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="notification-dropdown">
          <div className="notification-header">
            <div className="header-title">
              <h3>Notifications</h3>
              {unreadCount > 0 && (
                <span className="unread-count">{unreadCount} unread</span>
              )}
            </div>
            <div className="header-actions">
              {unreadCount > 0 && (
                <button
                  className="action-btn"
                  onClick={markAllAsRead}
                  title="Mark all as read"
                >
                  <Eye size={14} />
                </button>
              )}
              {notifications.length > 0 && (
                <button
                  className="action-btn"
                  onClick={clearAllNotifications}
                  title="Clear all"
                >
                  <Trash2 size={14} />
                </button>
              )}
              <button
                className="action-btn close-btn"
                onClick={() => setIsOpen(false)}
                title="Close"
              >
                <X size={14} />
              </button>
            </div>
          </div>

          <div className="notification-list">
            {notifications.length === 0 ? (
              <div className="empty-notifications">
                <Bell size={32} />
                <p>No notifications</p>
                <span>You're all caught up!</span>
              </div>
            ) : (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`notification-item ${!notification.isRead ? 'unread' : ''} ${getPriorityClass(notification.priority)}`}
                  onClick={() => !notification.isRead && markAsRead(notification.id)}
                >
                  <div className="notification-icon">
                    {getNotificationIcon(notification.type)}
                  </div>
                  <div className="notification-content">
                    <div className="notification-title">
                      {notification.title}
                      {!notification.isRead && <span className="unread-dot"></span>}
                    </div>
                    <div className="notification-message">
                      {notification.message}
                    </div>
                    <div className="notification-meta">
                      <span className="notification-time">
                        <Clock size={12} />
                        {formatTimestamp(notification.timestamp)}
                      </span>
                      <span className={`notification-priority ${getPriorityClass(notification.priority)}`}>
                        {notification.priority}
                      </span>
                    </div>
                  </div>
                  <button
                    className="delete-notification"
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteNotification(notification.id);
                    }}
                    title="Delete notification"
                  >
                    <X size={12} />
                  </button>
                </div>
              ))
            )}
          </div>

          {notifications.length > 0 && (
            <div className="notification-footer">
              <button className="view-all-btn">
                View All Notifications
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationCenter;
