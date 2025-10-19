import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Shield, User, Settings, LogOut, Wifi, WifiOff, ChevronDown } from 'lucide-react';
import { fraudAPI } from '../utils/api';
import NotificationCenter from './NotificationCenter';
import './Navbar.css';

const Navbar = ({ user, onLogout }) => {
  const [isOnline, setIsOnline] = useState(true);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  useEffect(() => {
    // Check API connection status
    const checkConnection = async () => {
      try {
        await fraudAPI.healthCheck();
        setIsOnline(true);
      } catch (error) {
        setIsOnline(false);
      }
    };

    checkConnection();
    const interval = setInterval(checkConnection, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/" className="brand-link">
          <Shield className="brand-icon" />
          <span className="brand-text">FraudGuard</span>
        </Link>
        <div className="connection-status">
          {isOnline ? (
            <div className="status-indicator online">
              <Wifi size={16} />
              <span>Online</span>
            </div>
          ) : (
            <div className="status-indicator offline">
              <WifiOff size={16} />
              <span>Offline</span>
            </div>
          )}
        </div>
      </div>

      <div className="navbar-actions">
        <NotificationCenter user={user} />

        <div className="user-menu">
          <button 
            className="nav-button user-button"
            onClick={() => setUserMenuOpen(!userMenuOpen)}
          >
            <User size={20} />
            <div className="user-info">
              <span className="user-name">{user?.name || 'User'}</span>
              <span className="user-role">{user?.role || 'guest'}</span>
            </div>
            <ChevronDown size={16} className={`chevron ${userMenuOpen ? 'open' : ''}`} />
          </button>
          
          {userMenuOpen && (
            <div className="user-dropdown">
              <div className="dropdown-header">
                <div className="user-avatar">
                  <User size={20} />
                </div>
                <div className="user-details">
                  <span className="dropdown-user-name">{user?.name}</span>
                  <span className="dropdown-user-role">{user?.role}</span>
                </div>
              </div>
              <div className="dropdown-divider"></div>
              <Link to="/settings" className="dropdown-item" onClick={() => setUserMenuOpen(false)}>
                <Settings size={16} />
                <span>Settings</span>
              </Link>
              <button className="dropdown-item logout-item" onClick={onLogout}>
                <LogOut size={16} />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
