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
