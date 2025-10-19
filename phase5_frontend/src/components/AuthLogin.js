import React, { useState } from 'react';
import { Shield, User, Lock, Eye, EyeOff, AlertTriangle } from 'lucide-react';
import './AuthLogin.css';

const AuthLogin = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Demo users for authentication
  const users = {
    admin: {
      password: 'admin123',
      role: 'admin',
      name: 'Bank Administrator',
      permissions: ['view_all', 'manage_system', 'export_data', 'user_management', 'batch_processing', 'analytics']
    },
    user: {
      password: 'user123',
      role: 'user',
      name: 'Bank Customer',
      permissions: ['view_own_transactions', 'real_time_monitoring']
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(''); // Clear error when user types
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    const { username, password } = formData;
    const user = users[username.toLowerCase()];

    if (user && user.password === password) {
      // Successful login
      const userSession = {
        username: username.toLowerCase(),
        name: user.name,
        role: user.role,
        permissions: user.permissions,
        loginTime: new Date().toISOString(),
        sessionId: Math.random().toString(36).substr(2, 9)
      };

      // Store in localStorage for persistence
      localStorage.setItem('fraudDetectionUser', JSON.stringify(userSession));
      
      onLogin(userSession);
    } else {
      setError('Invalid username or password');
    }

    setLoading(false);
  };

  const handleDemoLogin = (role) => {
    const demoUser = users[role];
    setFormData({
      username: role,
      password: demoUser.password
    });
  };

  return (
    <div className="auth-container">
      <div className="auth-background">
        <div className="auth-pattern"></div>
      </div>
      
      <div className="auth-card">
        <div className="auth-header">
          <div className="auth-logo">
            <Shield size={40} />
          </div>
          <h1>Fraud Detection System</h1>
          <p>Secure Access Portal</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label className="form-label">
              <User size={16} />
              Username
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Enter your username"
              className="form-input"
              required
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              <Lock size={16} />
              Password
            </label>
            <div className="password-input-container">
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Enter your password"
                className="form-input"
                required
                autoComplete="current-password"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          {error && (
            <div className="error-message">
              <AlertTriangle size={16} />
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !formData.username || !formData.password}
            className="login-btn"
          >
            {loading ? (
              <>
                <div className="spinner"></div>
                Authenticating...
              </>
            ) : (
              <>
                <Shield size={16} />
                Sign In
              </>
            )}
          </button>
        </form>

        <div className="demo-accounts">
          <h3>Demo Accounts</h3>
          <div className="demo-buttons">
            <button
              type="button"
              onClick={() => handleDemoLogin('admin')}
              className="demo-btn admin"
            >
              <Shield size={14} />
              Admin Access
              <span className="demo-credentials">admin / admin123</span>
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin('user')}
              className="demo-btn user"
            >
              <User size={14} />
              Customer Access
              <span className="demo-credentials">user / user123</span>
            </button>
          </div>
        </div>

        <div className="auth-footer">
          <p>© 2024 Fraud Detection System. All rights reserved.</p>
          <p>Secure • Reliable • Advanced AI Protection</p>
        </div>
      </div>
    </div>
  );
};

export default AuthLogin;
