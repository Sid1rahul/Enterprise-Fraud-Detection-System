import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  CheckCircle, 
  TrendingUp, 
  Shield, 
  Clock,
  DollarSign,
  User,
  MapPin,
  RefreshCw
} from 'lucide-react';
import './RealtimeActivityFeed.css';

const RealtimeActivityFeed = ({ user }) => {
  const [activities, setActivities] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Generate realistic activity based on user role
  const generateActivity = () => {
    const activityTypes = {
      fraud_detected: {
        icon: AlertTriangle,
        className: 'fraud_detected',
        messages: [
          'High-risk transaction blocked',
          'Suspicious card usage detected',
          'Unusual spending pattern flagged',
          'Cross-border transaction alert',
          'Multiple failed attempts detected'
        ],
        amounts: ['$2,500', '$7,800', '$1,200', '$15,000', '$950'],
        priority: 'high'
      },
      model_update: {
        icon: TrendingUp,
        className: 'model_update',
        messages: [
          'XGBoost model retrained',
          'Fraud detection accuracy improved',
          'New features added to model',
          'Model performance optimized',
          'Algorithm updated successfully'
        ],
        priority: 'medium'
      },
      batch_complete: {
        icon: CheckCircle,
        className: 'batch_complete',
        messages: [
          'Batch processing completed',
          'Transaction analysis finished',
          'Daily report generated',
          'Risk assessment completed',
          'Data validation successful'
        ],
        priority: 'low'
      },
      system_alert: {
        icon: Shield,
        className: 'system_alert',
        messages: [
          'System health check passed',
          'API response time optimized',
          'Database backup completed',
          'Security scan completed',
          'Performance metrics updated'
        ],
        priority: 'low'
      },
      user_activity: {
        icon: User,
        className: 'user_activity',
        messages: [
          'New user session started',
          'Analyst logged in',
          'Report accessed by user',
          'Dashboard view updated',
          'Settings modified'
        ],
        priority: 'low'
      }
    };

    // Filter activities based on user role
    let availableTypes = Object.keys(activityTypes);
    if (user?.role !== 'admin') {
      // Non-admin users see limited activity types
      availableTypes = availableTypes.filter(type => 
        !['system_alert', 'user_activity'].includes(type)
      );
    }

    const randomType = availableTypes[Math.floor(Math.random() * availableTypes.length)];
    const activityType = activityTypes[randomType];
    const randomMessage = activityType.messages[Math.floor(Math.random() * activityType.messages.length)];

    const activity = {
      id: Date.now() + Math.random(),
      type: randomType,
      icon: activityType.icon,
      className: activityType.className,
      message: randomMessage,
      timestamp: new Date(),
      priority: activityType.priority,
      isNew: true
    };

    // Add amount for fraud activities
    if (randomType === 'fraud_detected') {
      activity.amount = activityType.amounts[Math.floor(Math.random() * activityType.amounts.length)];
      activity.location = ['New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Phoenix, AZ'][Math.floor(Math.random() * 5)];
    }

    // Add metrics for other activities
    if (randomType === 'batch_complete') {
      activity.count = Math.floor(Math.random() * 500) + 50;
    }

    if (randomType === 'model_update') {
      activity.accuracy = (95 + Math.random() * 4).toFixed(1) + '%';
    }

    return activity;
  };

  useEffect(() => {
    // Initialize with some activities
    const initialActivities = Array.from({ length: 5 }, (_, index) => {
      const activity = generateActivity();
      activity.id = index + 1;
      activity.timestamp = new Date(Date.now() - (index * 5 * 60000)); // 5 minutes apart
      activity.isNew = false;
      return activity;
    });

    setActivities(initialActivities);

    // Generate new activities periodically
    const interval = setInterval(() => {
      if (Math.random() > 0.3) { // 70% chance every 15 seconds
        const newActivity = generateActivity();
        setActivities(prev => {
          // Mark previous activities as not new
          const updatedPrev = prev.map(activity => ({ ...activity, isNew: false }));
          return [newActivity, ...updatedPrev.slice(0, 9)]; // Keep max 10 activities
        });

        // Remove "new" status after 10 seconds
        setTimeout(() => {
          setActivities(prev => 
            prev.map(activity => 
              activity.id === newActivity.id 
                ? { ...activity, isNew: false }
                : activity
            )
          );
        }, 10000);
      }
    }, 15000); // Check every 15 seconds

    return () => clearInterval(interval);
  }, [user]);

  const formatTimestamp = (timestamp) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now - timestamp) / (1000 * 60));

    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  const refreshActivities = () => {
    setIsLoading(true);
    setTimeout(() => {
      const newActivities = Array.from({ length: 5 }, () => {
        const activity = generateActivity();
        activity.isNew = false;
        activity.timestamp = new Date(Date.now() - Math.random() * 3600000); // Random within last hour
        return activity;
      });
      setActivities(newActivities);
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="realtime-activity-feed">
      <div className="activity-header">
        <div className="header-content">
          <h3>Recent Activity</h3>
          <p>Live system events and alerts</p>
        </div>
        <button 
          className={`refresh-btn ${isLoading ? 'loading' : ''}`}
          onClick={refreshActivities}
          disabled={isLoading}
          title="Refresh activities"
        >
          <RefreshCw size={16} />
        </button>
      </div>

      <div className="activity-list">
        {activities.map((activity) => {
          const IconComponent = activity.icon;
          return (
            <div 
              key={activity.id} 
              className={`activity-item ${activity.className} ${activity.isNew ? 'new-activity' : ''} priority-${activity.priority}`}
            >
              <div className="activity-icon">
                <IconComponent size={16} />
              </div>
              <div className="activity-content">
                <div className="activity-main">
                  <p className="activity-message">{activity.message}</p>
                  <div className="activity-meta">
                    {activity.amount && (
                      <span className="activity-amount">
                        <DollarSign size={12} />
                        {activity.amount}
                      </span>
                    )}
                    {activity.location && (
                      <span className="activity-location">
                        <MapPin size={12} />
                        {activity.location}
                      </span>
                    )}
                    {activity.count && (
                      <span className="activity-count">
                        {activity.count} transactions
                      </span>
                    )}
                    {activity.accuracy && (
                      <span className="activity-accuracy">
                        {activity.accuracy} accuracy
                      </span>
                    )}
                  </div>
                </div>
                <div className="activity-time">
                  <Clock size={12} />
                  {formatTimestamp(activity.timestamp)}
                </div>
              </div>
              {activity.isNew && <div className="new-indicator">NEW</div>}
            </div>
          );
        })}
      </div>

      <div className="activity-footer">
        <div className="activity-stats">
          <span className="stat-item">
            <span className="stat-value">{activities.filter(a => a.type === 'fraud_detected').length}</span>
            <span className="stat-label">Fraud Alerts</span>
          </span>
          <span className="stat-item">
            <span className="stat-value">{activities.filter(a => a.priority === 'high').length}</span>
            <span className="stat-label">High Priority</span>
          </span>
          <span className="stat-item">
            <span className="stat-value">{activities.filter(a => a.isNew).length}</span>
            <span className="stat-label">New Events</span>
          </span>
        </div>
      </div>
    </div>
  );
};

export default RealtimeActivityFeed;
