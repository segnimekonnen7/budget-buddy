import React, { useState } from 'react';
import './Settings.css';

const Settings = () => {
  const [settings, setSettings] = useState({
    notifications: {
      priceAlerts: true,
      newsAlerts: false,
      tradeConfirmations: true,
      marketOpen: true
    },
    display: {
      theme: 'light',
      currency: 'USD',
      timezone: 'America/New_York',
      decimalPlaces: 2
    },
    trading: {
      defaultOrderType: 'market',
      confirmTrades: true,
      autoSave: true,
      riskLevel: 'moderate'
    },
    account: {
      email: 'user@example.com',
      phone: '+1 (555) 123-4567',
      twoFactorAuth: true,
      apiKey: '••••••••••••••••'
    }
  });

  const handleSettingChange = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  const handleSaveSettings = () => {
    // In a real app, this would save to backend
    console.log('Saving settings:', settings);
    alert('Settings saved successfully!');
  };

  const handleResetSettings = () => {
    if (window.confirm('Are you sure you want to reset all settings to default?')) {
      // Reset to default settings
      setSettings({
        notifications: {
          priceAlerts: true,
          newsAlerts: false,
          tradeConfirmations: true,
          marketOpen: true
        },
        display: {
          theme: 'light',
          currency: 'USD',
          timezone: 'America/New_York',
          decimalPlaces: 2
        },
        trading: {
          defaultOrderType: 'market',
          confirmTrades: true,
          autoSave: true,
          riskLevel: 'moderate'
        },
        account: {
          email: 'user@example.com',
          phone: '+1 (555) 123-4567',
          twoFactorAuth: true,
          apiKey: '••••••••••••••••'
        }
      });
    }
  };

  return (
    <div className="settings">
      <div className="settings-header">
        <h2>Settings</h2>
        <p>Customize your trading experience</p>
      </div>

      <div className="settings-content">
        {/* Notifications Section */}
        <div className="settings-section">
          <h3>Notifications</h3>
          <div className="settings-grid">
            <div className="setting-item">
              <div className="setting-info">
                <label>Price Alerts</label>
                <p>Get notified when stocks reach your target prices</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={settings.notifications.priceAlerts}
                  onChange={(e) => handleSettingChange('notifications', 'priceAlerts', e.target.checked)}
                />
                <span className="slider"></span>
              </label>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>News Alerts</label>
                <p>Receive breaking news about your watchlist stocks</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={settings.notifications.newsAlerts}
                  onChange={(e) => handleSettingChange('notifications', 'newsAlerts', e.target.checked)}
                />
                <span className="slider"></span>
              </label>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Trade Confirmations</label>
                <p>Confirm all trades before execution</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={settings.notifications.tradeConfirmations}
                  onChange={(e) => handleSettingChange('notifications', 'tradeConfirmations', e.target.checked)}
                />
                <span className="slider"></span>
              </label>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Market Open/Close</label>
                <p>Notifications when markets open and close</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={settings.notifications.marketOpen}
                  onChange={(e) => handleSettingChange('notifications', 'marketOpen', e.target.checked)}
                />
                <span className="slider"></span>
              </label>
            </div>
          </div>
        </div>

        {/* Display Section */}
        <div className="settings-section">
          <h3>Display</h3>
          <div className="settings-grid">
            <div className="setting-item">
              <div className="setting-info">
                <label>Theme</label>
                <p>Choose your preferred color scheme</p>
              </div>
              <select
                value={settings.display.theme}
                onChange={(e) => handleSettingChange('display', 'theme', e.target.value)}
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="auto">Auto</option>
              </select>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Currency</label>
                <p>Display prices in your preferred currency</p>
              </div>
              <select
                value={settings.display.currency}
                onChange={(e) => handleSettingChange('display', 'currency', e.target.value)}
              >
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
                <option value="JPY">JPY (¥)</option>
              </select>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Timezone</label>
                <p>Set your local timezone for accurate timestamps</p>
              </div>
              <select
                value={settings.display.timezone}
                onChange={(e) => handleSettingChange('display', 'timezone', e.target.value)}
              >
                <option value="America/New_York">Eastern Time</option>
                <option value="America/Chicago">Central Time</option>
                <option value="America/Denver">Mountain Time</option>
                <option value="America/Los_Angeles">Pacific Time</option>
                <option value="Europe/London">London</option>
                <option value="Europe/Paris">Paris</option>
                <option value="Asia/Tokyo">Tokyo</option>
              </select>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Decimal Places</label>
                <p>Number of decimal places for price display</p>
              </div>
              <select
                value={settings.display.decimalPlaces}
                onChange={(e) => handleSettingChange('display', 'decimalPlaces', parseInt(e.target.value))}
              >
                <option value={2}>2</option>
                <option value={3}>3</option>
                <option value={4}>4</option>
              </select>
            </div>
          </div>
        </div>

        {/* Trading Section */}
        <div className="settings-section">
          <h3>Trading Preferences</h3>
          <div className="settings-grid">
            <div className="setting-item">
              <div className="setting-info">
                <label>Default Order Type</label>
                <p>Preferred order type for new trades</p>
              </div>
              <select
                value={settings.trading.defaultOrderType}
                onChange={(e) => handleSettingChange('trading', 'defaultOrderType', e.target.value)}
              >
                <option value="market">Market</option>
                <option value="limit">Limit</option>
                <option value="stop">Stop</option>
              </select>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Confirm Trades</label>
                <p>Always confirm before executing trades</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={settings.trading.confirmTrades}
                  onChange={(e) => handleSettingChange('trading', 'confirmTrades', e.target.checked)}
                />
                <span className="slider"></span>
              </label>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Auto Save</label>
                <p>Automatically save trade history</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={settings.trading.autoSave}
                  onChange={(e) => handleSettingChange('trading', 'autoSave', e.target.checked)}
                />
                <span className="slider"></span>
              </label>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Risk Level</label>
                <p>Set your trading risk tolerance</p>
              </div>
              <select
                value={settings.trading.riskLevel}
                onChange={(e) => handleSettingChange('trading', 'riskLevel', e.target.value)}
              >
                <option value="conservative">Conservative</option>
                <option value="moderate">Moderate</option>
                <option value="aggressive">Aggressive</option>
              </select>
            </div>
          </div>
        </div>

        {/* Account Section */}
        <div className="settings-section">
          <h3>Account</h3>
          <div className="settings-grid">
            <div className="setting-item">
              <div className="setting-info">
                <label>Email</label>
                <p>Primary email for notifications</p>
              </div>
              <input
                type="email"
                value={settings.account.email}
                onChange={(e) => handleSettingChange('account', 'email', e.target.value)}
                placeholder="Enter email address"
              />
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Phone</label>
                <p>Phone number for SMS alerts</p>
              </div>
              <input
                type="tel"
                value={settings.account.phone}
                onChange={(e) => handleSettingChange('account', 'phone', e.target.value)}
                placeholder="Enter phone number"
              />
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>Two-Factor Authentication</label>
                <p>Enhanced security for your account</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={settings.account.twoFactorAuth}
                  onChange={(e) => handleSettingChange('account', 'twoFactorAuth', e.target.checked)}
                />
                <span className="slider"></span>
              </label>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <label>API Key</label>
                <p>Your trading API key (masked for security)</p>
              </div>
              <input
                type="password"
                value={settings.account.apiKey}
                onChange={(e) => handleSettingChange('account', 'apiKey', e.target.value)}
                placeholder="Enter API key"
              />
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="settings-actions">
          <button className="btn btn-secondary" onClick={handleResetSettings}>
            Reset to Default
          </button>
          <button className="btn btn-primary" onClick={handleSaveSettings}>
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings; 