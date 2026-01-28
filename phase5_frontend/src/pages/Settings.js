import React, { useState, useEffect } from 'react';
import { 
  Settings as SettingsIcon, 
  Save, 
  RotateCcw, 
  Database,
  Shield,
  Bell,
  Palette,
  Server
} from 'lucide-react';
import toast from 'react-hot-toast';
import './Settings.css';

const Settings = () => {
  const [settings, setSettings] = useState({
    // API Settings
    apiEndpoint: 'http://localhost:8000',
    apiTimeout: 30000,
    authToken: 'demo_token_123',
    
    // Model Settings
    defaultModel: 'xgboost',
    fraudThreshold: 0.5,
    enableExplanations: true,
    
    // Notification Settings
    emailNotifications: true,
    fraudAlerts: true,
    systemAlerts: false,
    
    // UI Settings
    theme: 'dark',
    autoRefresh: true,
    refreshInterval: 30,
    
    // Security Settings
    sessionTimeout: 3600,
    enableLogging: true,
    logLevel: 'INFO'
  });

  const applyTheme = (theme) => {
    if (typeof document === 'undefined') return;
    const root = document.documentElement;
    const namedThemes = ['light', 'emerald', 'sunset', 'purple'];
    if (namedThemes.includes(theme)) {
      root.setAttribute('data-theme', theme);
    } else if (theme === 'auto') {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        root.removeAttribute('data-theme');
      } else {
        root.setAttribute('data-theme', 'light');
      }
    } else {
      // Default to dark theme (no explicit data-theme attribute)
      root.removeAttribute('data-theme');
    }
  };

  useEffect(() => {
    // Load any previously saved settings
    try {
      const saved = localStorage.getItem('fraudDetectionSettings');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed && typeof parsed === 'object') {
          setSettings(prev => ({ ...prev, ...parsed }));
          if (parsed.theme) {
            applyTheme(parsed.theme);
          }
        }
      }
    } catch (error) {
      // Ignore and use defaults
    }
  }, []);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;

    setSettings(prev => ({
      ...prev,
      [name]: newValue
    }));

    if (name === 'theme') {
      applyTheme(newValue);
    }
  };

  const handleSave = () => {
    // Simulate saving settings
    localStorage.setItem('fraudDetectionSettings', JSON.stringify(settings));
    toast.success('Settings saved successfully');
  };

  const handleReset = () => {
    // Reset to defaults
    const defaultSettings = {
      apiEndpoint: 'http://localhost:8000',
      apiTimeout: 30000,
      authToken: 'demo_token_123',
      defaultModel: 'xgboost',
      fraudThreshold: 0.5,
      enableExplanations: true,
      emailNotifications: true,
      fraudAlerts: true,
      systemAlerts: false,
      theme: 'dark',
      autoRefresh: true,
      refreshInterval: 30,
      sessionTimeout: 3600,
      enableLogging: true,
      logLevel: 'INFO'
    };

    setSettings(defaultSettings);
    localStorage.setItem('fraudDetectionSettings', JSON.stringify(defaultSettings));
    applyTheme(defaultSettings.theme);
    toast.success('Settings reset to defaults');
  };

  return (
    <div className="settings">
      <div className="page-header">
        <div className="header-content">
          <SettingsIcon className="header-icon" />
          <div>
            <h1>Settings</h1>
            <p>Configure system preferences and parameters</p>
          </div>
        </div>
      </div>

      <div className="settings-grid">
        {/* API Configuration */}
        <div className="settings-section">
          <div className="section-header">
            <Server size={20} />
            <h2>API Configuration</h2>
          </div>
          
          <div className="settings-form">
            <div className="form-group">
              <label className="form-label">API Endpoint</label>
              <input
                type="url"
                name="apiEndpoint"
                value={settings.apiEndpoint}
                onChange={handleInputChange}
                className="form-input"
                placeholder="http://localhost:8000"
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Request Timeout (ms)</label>
              <input
                type="number"
                name="apiTimeout"
                value={settings.apiTimeout}
                onChange={handleInputChange}
                className="form-input"
                min="1000"
                max="120000"
                step="1000"
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Authentication Token</label>
              <input
                type="password"
                name="authToken"
                value={settings.authToken}
                onChange={handleInputChange}
                className="form-input"
                placeholder="Enter API token"
              />
            </div>
          </div>
        </div>

        {/* Model Configuration */}
        <div className="settings-section">
          <div className="section-header">
            <Database size={20} />
            <h2>Model Configuration</h2>
          </div>
          
          <div className="settings-form">
            <div className="form-group">
              <label className="form-label">Default Model</label>
              <select
                name="defaultModel"
                value={settings.defaultModel}
                onChange={handleInputChange}
                className="form-input form-select"
              >
                <option value="xgboost">XGBoost</option>
                <option value="isolation_forest">Isolation Forest</option>
                <option value="ensemble">Ensemble</option>
              </select>
            </div>
            
            <div className="form-group">
              <label className="form-label">Fraud Threshold</label>
              <div className="threshold-control">
                <input
                  type="range"
                  name="fraudThreshold"
                  value={settings.fraudThreshold}
                  onChange={handleInputChange}
                  className="threshold-slider"
                  min="0"
                  max="1"
                  step="0.01"
                />
                <span className="threshold-value">{(settings.fraudThreshold * 100).toFixed(0)}%</span>
              </div>
            </div>
            
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="enableExplanations"
                  checked={settings.enableExplanations}
                  onChange={handleInputChange}
                  className="checkbox-input"
                />
                <span className="checkbox-custom"></span>
                Enable SHAP explanations
              </label>
            </div>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="settings-section">
          <div className="section-header">
            <Bell size={20} />
            <h2>Notifications</h2>
          </div>
          
          <div className="settings-form">
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="emailNotifications"
                  checked={settings.emailNotifications}
                  onChange={handleInputChange}
                  className="checkbox-input"
                />
                <span className="checkbox-custom"></span>
                Email notifications
              </label>
            </div>
            
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="fraudAlerts"
                  checked={settings.fraudAlerts}
                  onChange={handleInputChange}
                  className="checkbox-input"
                />
                <span className="checkbox-custom"></span>
                Fraud detection alerts
              </label>
            </div>
            
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="systemAlerts"
                  checked={settings.systemAlerts}
                  onChange={handleInputChange}
                  className="checkbox-input"
                />
                <span className="checkbox-custom"></span>
                System maintenance alerts
              </label>
            </div>
          </div>
        </div>

        {/* UI Preferences */}
        <div className="settings-section">
          <div className="section-header">
            <Palette size={20} />
            <h2>Interface</h2>
          </div>
          
          <div className="settings-form">
            <div className="form-group">
              <label className="form-label">Theme</label>
              <select
                name="theme"
                value={settings.theme}
                onChange={handleInputChange}
                className="form-input form-select"
              >
                <option value="dark">Dark (Aqua Blue)</option>
                <option value="light">Light</option>
                <option value="emerald">Emerald (Teal Green)</option>
                <option value="sunset">Sunset (Warm)</option>
                <option value="purple">Purple (Violet)</option>
                <option value="auto">Auto (Match System)</option>
              </select>
            </div>
            
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="autoRefresh"
                  checked={settings.autoRefresh}
                  onChange={handleInputChange}
                  className="checkbox-input"
                />
                <span className="checkbox-custom"></span>
                Auto-refresh dashboard
              </label>
            </div>
            
            {settings.autoRefresh && (
              <div className="form-group">
                <label className="form-label">Refresh Interval (seconds)</label>
                <input
                  type="number"
                  name="refreshInterval"
                  value={settings.refreshInterval}
                  onChange={handleInputChange}
                  className="form-input"
                  min="10"
                  max="300"
                  step="10"
                />
              </div>
            )}
          </div>
        </div>

        {/* Security Settings */}
        <div className="settings-section">
          <div className="section-header">
            <Shield size={20} />
            <h2>Security</h2>
          </div>
          
          <div className="settings-form">
            <div className="form-group">
              <label className="form-label">Session Timeout (seconds)</label>
              <input
                type="number"
                name="sessionTimeout"
                value={settings.sessionTimeout}
                onChange={handleInputChange}
                className="form-input"
                min="300"
                max="86400"
                step="300"
              />
            </div>
            
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="enableLogging"
                  checked={settings.enableLogging}
                  onChange={handleInputChange}
                  className="checkbox-input"
                />
                <span className="checkbox-custom"></span>
                Enable audit logging
              </label>
            </div>
            
            <div className="form-group">
              <label className="form-label">Log Level</label>
              <select
                name="logLevel"
                value={settings.logLevel}
                onChange={handleInputChange}
                className="form-input form-select"
              >
                <option value="DEBUG">Debug</option>
                <option value="INFO">Info</option>
                <option value="WARNING">Warning</option>
                <option value="ERROR">Error</option>
              </select>
            </div>
          </div>
        </div>

        {/* System Information */}
        <div className="settings-section info-section">
          <div className="section-header">
            <Database size={20} />
            <h2>System Information</h2>
          </div>
          
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Version</span>
              <span className="info-value">1.0.0</span>
            </div>
            <div className="info-item">
              <span className="info-label">Build</span>
              <span className="info-value">2024.01.15</span>
            </div>
            <div className="info-item">
              <span className="info-label">API Status</span>
              <span className="info-value status-online">Online</span>
            </div>
            <div className="info-item">
              <span className="info-label">Models Loaded</span>
              <span className="info-value">2</span>
            </div>
            <div className="info-item">
              <span className="info-label">Uptime</span>
              <span className="info-value">2h 34m</span>
            </div>
            <div className="info-item">
              <span className="info-label">Last Updated</span>
              <span className="info-value">Just now</span>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="settings-actions">
        <button onClick={handleSave} className="btn btn-primary btn-lg">
          <Save size={20} />
          Save Settings
        </button>
        <button onClick={handleReset} className="btn btn-ghost">
          <RotateCcw size={20} />
          Reset to Defaults
        </button>
      </div>
    </div>
  );
};

export default Settings;
