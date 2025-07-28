import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import StockSearch from './components/StockSearch';
import Portfolio from './components/Portfolio';
import Watchlist from './components/Watchlist';
import StockChart from './components/StockChart';
import Settings from './components/Settings';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'search', label: 'Search', icon: '🔍' },
  { id: 'portfolio', label: 'Portfolio', icon: '💼' },
  { id: 'watchlist', label: 'Watchlist', icon: '👀' },
  { id: 'chart', label: 'Charts', icon: '📈' },
  { id: 'settings', label: 'Settings', icon: '⚙️' }
];

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedStock, setSelectedStock] = useState('AAPL');
  const [portfolio, setPortfolio] = useState([
    {
      symbol: 'AAPL',
      shares: 10,
      avgPrice: 150.25,
      currentPrice: 175.50,
      change: 25.25,
      changePercent: 16.81
    },
    {
      symbol: 'GOOGL',
      shares: 5,
      avgPrice: 2800.00,
      currentPrice: 2950.75,
      change: 150.75,
      changePercent: 5.38
    },
    {
      symbol: 'TSLA',
      shares: 20,
      avgPrice: 800.00,
      currentPrice: 750.25,
      change: -49.75,
      changePercent: -6.22
    }
  ]);

  const [watchlist, setWatchlist] = useState([
    { symbol: 'MSFT', name: 'Microsoft Corporation', price: 320.45, change: 5.20, changePercent: 1.65 },
    { symbol: 'AMZN', name: 'Amazon.com Inc', price: 145.80, change: -2.30, changePercent: -1.55 },
    { symbol: 'NVDA', name: 'NVIDIA Corporation', price: 450.75, change: 12.50, changePercent: 2.85 },
    { symbol: 'META', name: 'Meta Platforms Inc', price: 280.90, change: 8.75, changePercent: 3.22 }
  ]);

  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Mock market data
  const [marketData, setMarketData] = useState({
    totalValue: 0,
    totalGain: 0,
    totalGainPercent: 0,
    dayGain: 0,
    dayGainPercent: 0
  });

  useEffect(() => {
    // Calculate portfolio totals
    const totalValue = portfolio.reduce((sum, stock) => sum + (stock.shares * stock.currentPrice), 0);
    const totalCost = portfolio.reduce((sum, stock) => sum + (stock.shares * stock.avgPrice), 0);
    const totalGain = totalValue - totalCost;
    const totalGainPercent = totalCost > 0 ? (totalGain / totalCost) * 100 : 0;
    const dayGain = portfolio.reduce((sum, stock) => sum + (stock.shares * stock.change), 0);
    const dayGainPercent = totalValue > 0 ? (dayGain / totalValue) * 100 : 0;

    setMarketData({
      totalValue,
      totalGain,
      totalGainPercent,
      dayGain,
      dayGainPercent
    });
  }, [portfolio]);

  const handleSearch = async (query) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    setIsLoading(true);
    
    // Mock search results
    setTimeout(() => {
      const mockResults = [
        { symbol: 'AAPL', name: 'Apple Inc.', price: 175.50, change: 2.30, changePercent: 1.33 },
        { symbol: 'MSFT', name: 'Microsoft Corporation', price: 320.45, change: 5.20, changePercent: 1.65 },
        { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 2950.75, change: 150.75, changePercent: 5.38 },
        { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 145.80, change: -2.30, changePercent: -1.55 },
        { symbol: 'TSLA', name: 'Tesla Inc.', price: 750.25, change: -49.75, changePercent: -6.22 }
      ].filter(stock => 
        stock.symbol.toLowerCase().includes(query.toLowerCase()) ||
        stock.name.toLowerCase().includes(query.toLowerCase())
      );
      
      setSearchResults(mockResults);
      setIsLoading(false);
    }, 500);
  };

  const addToWatchlist = (stock) => {
    if (!watchlist.find(item => item.symbol === stock.symbol)) {
      setWatchlist(prev => [...prev, stock]);
    }
  };

  const removeFromWatchlist = (symbol) => {
    setWatchlist(prev => prev.filter(item => item.symbol !== symbol));
  };

  const buyStock = (stock, shares, price) => {
    const existingStock = portfolio.find(item => item.symbol === stock.symbol);
    
    if (existingStock) {
      // Update existing position
      const totalShares = existingStock.shares + shares;
      const totalCost = (existingStock.shares * existingStock.avgPrice) + (shares * price);
      const newAvgPrice = totalCost / totalShares;
      
      setPortfolio(prev => prev.map(item => 
        item.symbol === stock.symbol 
          ? { ...item, shares: totalShares, avgPrice: newAvgPrice }
          : item
      ));
    } else {
      // Add new position
      setPortfolio(prev => [...prev, {
        symbol: stock.symbol,
        shares: shares,
        avgPrice: price,
        currentPrice: price,
        change: 0,
        changePercent: 0
      }]);
    }
  };

  const sellStock = (symbol, shares) => {
    setPortfolio(prev => {
      const stock = prev.find(item => item.symbol === symbol);
      if (!stock) return prev;
      
      if (stock.shares <= shares) {
        // Sell all shares
        return prev.filter(item => item.symbol !== symbol);
      } else {
        // Sell partial shares
        return prev.map(item => 
          item.symbol === symbol 
            ? { ...item, shares: item.shares - shares }
            : item
        );
      }
    });
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard marketData={marketData} portfolio={portfolio} watchlist={watchlist} />;
      case 'search':
        return (
          <StockSearch 
            onSearch={handleSearch}
            searchResults={searchResults}
            isLoading={isLoading}
            onAddToWatchlist={addToWatchlist}
            onBuyStock={buyStock}
          />
        );
      case 'portfolio':
        return (
          <Portfolio 
            portfolio={portfolio}
            onSellStock={sellStock}
            onBuyMore={buyStock}
          />
        );
      case 'watchlist':
        return (
          <Watchlist 
            watchlist={watchlist}
            onRemoveFromWatchlist={removeFromWatchlist}
            onBuyStock={buyStock}
          />
        );
      case 'chart':
        return <StockChart symbol={selectedStock} />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard marketData={marketData} portfolio={portfolio} watchlist={watchlist} />;
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">📈 Stock Trader Pro</h1>
          <div className="market-status">
            <span className="status-indicator open"></span>
            <span className="status-text">Market Open</span>
            <span className="current-time">
              {new Date().toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: false,
                timeZone: 'America/New_York'
              })}
            </span>
          </div>
        </div>
      </header>

      <nav className="app-nav">
        <div className="nav-content">
          {NAV_ITEMS.map(item => (
            <button
              key={item.id}
              className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </button>
          ))}
        </div>
      </nav>

      <main className="app-main">
        <div className="main-content">
          {renderContent()}
        </div>
      </main>

      <footer className="app-footer">
        <div className="footer-content">
          <p>&copy; 2024 Stock Trader Pro. This is a demo application for educational purposes.</p>
          <p>Stock data is simulated and not real-time.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
