import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import AuthLogin from './components/AuthLogin';
import Dashboard from './pages/Dashboard';
import FraudDetection from './pages/FraudDetection';
import BatchProcessing from './pages/BatchProcessing';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import RealTimeMonitoring from './pages/RealTimeMonitoring';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

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
    // Apply persisted theme on initial load
    try {
      const savedSettings = localStorage.getItem('fraudDetectionSettings');
      if (savedSettings) {
        const parsed = JSON.parse(savedSettings);
        if (parsed && parsed.theme) {
          applyTheme(parsed.theme);
          return;
        }
      }
    } catch (error) {
      // Ignore and fall back to default
    }
    applyTheme('dark');
  }, []);

  useEffect(() => {
    // Check for existing session
    const savedUser = localStorage.getItem('fraudDetectionUser');
    if (savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
      } catch (error) {
        console.error('Error parsing saved user data:', error);
        localStorage.removeItem('fraudDetectionUser');
      }
    }
    setIsLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('fraudDetectionUser');
    setUser(null);
  };

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>Loading Fraud Detection System...</p>
      </div>
    );
  }

  if (!user) {
    return <AuthLogin onLogin={handleLogin} />;
  }

  return (
    <Router>
      <div className="app">
        <Navbar user={user} onLogout={handleLogout} />
        <div className="app-content">
          <Sidebar user={user} />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard user={user} />} />
              <Route path="/dashboard" element={<Dashboard user={user} />} />
              <Route path="/batch-processing" element={<BatchProcessing user={user} />} />
              <Route path="/real-time-monitoring" element={<RealTimeMonitoring user={user} />} />
              <Route path="/analytics" element={<Analytics user={user} />} />
              <Route path="/settings" element={<Settings user={user} />} />
            </Routes>
          </main>
        </div>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: 'var(--bg-card)',
              color: 'var(--text-primary)',
              border: '1px solid var(--accent-primary)',
              borderRadius: 'var(--radius-md)',
            },
            success: {
              iconTheme: {
                primary: 'var(--success)',
                secondary: 'white',
              },
            },
            error: {
              iconTheme: {
                primary: 'var(--error)',
                secondary: 'white',
              },
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;
