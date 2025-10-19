import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Shield, 
  Layers, 
  BarChart3, 
  Settings,
  ChevronLeft,
  ChevronRight,
  Activity,
  Database,
  Lock
} from 'lucide-react';
import { getNavigationItems, hasPermission, PERMISSIONS } from '../utils/dataAccess';
import './Sidebar.css';

const Sidebar = ({ user }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const location = useLocation();

  // Get role-based menu items
  const getMenuItems = () => {
    const allItems = [
      {
        path: '/dashboard',
        icon: LayoutDashboard,
        label: 'Dashboard',
        description: 'Overview & metrics',
        permission: null
      },
      {
        path: '/batch-processing',
        icon: Layers,
        label: 'Fraud Analysis',
        description: 'Transaction fraud detection',
        permission: PERMISSIONS.BATCH_PROCESSING
      },
      {
        path: '/real-time-monitoring',
        icon: Activity,
        label: 'Real-Time Monitoring',
        description: 'Live transaction stream',
        permission: PERMISSIONS.REAL_TIME_MONITORING
      },
      {
        path: '/analytics',
        icon: BarChart3,
        label: 'Analytics',
        description: 'Reports & insights',
        permission: PERMISSIONS.ANALYTICS_ADVANCED
      },
      {
        path: '/settings',
        icon: Settings,
        label: 'Settings',
        description: 'System configuration',
        permission: PERMISSIONS.MANAGE_SYSTEM
      }
    ];

    return allItems.map(item => ({
      ...item,
      hasAccess: !item.permission || hasPermission(user, item.permission),
      isRestricted: item.permission && !hasPermission(user, item.permission)
    }));
  };

  const menuItems = getMenuItems();

  const isActive = (path) => {
    return location.pathname === path || (path === '/dashboard' && location.pathname === '/');
  };

  return (
    <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <button 
          className="collapse-button"
          onClick={() => setIsCollapsed(!isCollapsed)}
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>

      <nav className="sidebar-nav">
        <ul className="nav-list">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isItemActive = isActive(item.path);
            
            return (
              <li key={item.path} className="nav-item">
                {item.hasAccess ? (
                  <Link
                    to={item.path}
                    className={`nav-link ${isItemActive ? 'active' : ''}`}
                    title={isCollapsed ? item.label : ''}
                  >
                    <Icon className="nav-icon" size={20} />
                    {!isCollapsed && (
                      <div className="nav-content">
                        <span className="nav-label">{item.label}</span>
                        <span className="nav-description">{item.description}</span>
                      </div>
                    )}
                    {isItemActive && <div className="active-indicator" />}
                  </Link>
                ) : (
                  <div
                    className="nav-link restricted"
                    title={isCollapsed ? `${item.label} (Access Restricted)` : 'Access Restricted'}
                  >
                    <Icon className="nav-icon" size={20} />
                    {!isCollapsed && (
                      <div className="nav-content">
                        <span className="nav-label">{item.label}</span>
                        <span className="nav-description">Access Restricted</span>
                      </div>
                    )}
                    <Lock className="restriction-icon" size={14} />
                  </div>
                )}
              </li>
            );
          })}
        </ul>
        
        {!isCollapsed && user && (
          <div className="sidebar-footer">
            <div className="user-role-info">
              <div className="role-badge">
                <span className={`role-indicator ${user.role}`}></span>
                <span className="role-text">{user.role.toUpperCase()}</span>
              </div>
              <div className="access-level">
                {user.role === 'admin' && <span>Full Access</span>}
                {user.role === 'analyst' && <span>Advanced Access</span>}
                {user.role === 'user' && <span>Limited Access</span>}
              </div>
            </div>
          </div>
        )}
      </nav>

      {!isCollapsed && (
        <div className="sidebar-footer">
          <div className="system-status">
            <div className="status-item">
              <Activity size={16} />
              <div className="status-info">
                <span className="status-label">API Status</span>
                <span className="status-value online">Online</span>
              </div>
            </div>
            <div className="status-item">
              <Database size={16} />
              <div className="status-info">
                <span className="status-label">Models</span>
                <span className="status-value">2 Active</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
};

export default Sidebar;
