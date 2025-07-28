import React, { useState, useEffect } from 'react';
import './StockChart.css';

const StockChart = ({ symbol, timeRange = '1D' }) => {
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTimeRange, setSelectedTimeRange] = useState(timeRange);

  // Mock chart data generation
  useEffect(() => {
    setLoading(true);
    
    // Generate mock price data
    const generateMockData = () => {
      const data = [];
      const basePrice = 150 + Math.random() * 100;
      const now = new Date();
      
      for (let i = 0; i < 100; i++) {
        const time = new Date(now.getTime() - (100 - i) * 60000);
        const price = basePrice + (Math.random() - 0.5) * 10;
        data.push({
          time: time.toISOString(),
          price: parseFloat(price.toFixed(2)),
          volume: Math.floor(Math.random() * 1000000) + 100000
        });
      }
      
      return data;
    };

    setTimeout(() => {
      setChartData(generateMockData());
      setLoading(false);
    }, 500);
  }, [symbol, selectedTimeRange]);

  const timeRanges = [
    { label: '1D', value: '1D' },
    { label: '1W', value: '1W' },
    { label: '1M', value: '1M' },
    { label: '3M', value: '3M' },
    { label: '1Y', value: '1Y' },
    { label: '5Y', value: '5Y' }
  ];

  const currentPrice = chartData.length > 0 ? chartData[chartData.length - 1].price : 0;
  const previousPrice = chartData.length > 1 ? chartData[chartData.length - 2].price : currentPrice;
  const priceChange = currentPrice - previousPrice;
  const priceChangePercent = previousPrice > 0 ? (priceChange / previousPrice) * 100 : 0;

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(price);
  };

  const formatTime = (timeString) => {
    const date = new Date(timeString);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
  };

  return (
    <div className="stock-chart">
      <div className="chart-header">
        <div className="stock-info">
          <h3>{symbol}</h3>
          <div className="price-info">
            <span className="current-price">{formatPrice(currentPrice)}</span>
            <span className={`price-change ${priceChange >= 0 ? 'positive' : 'negative'}`}>
              {priceChange >= 0 ? '+' : ''}{formatPrice(priceChange)} ({priceChangePercent >= 0 ? '+' : ''}{priceChangePercent.toFixed(2)}%)
            </span>
          </div>
        </div>
        
        <div className="time-range-selector">
          {timeRanges.map(range => (
            <button
              key={range.value}
              className={`time-range-btn ${selectedTimeRange === range.value ? 'active' : ''}`}
              onClick={() => setSelectedTimeRange(range.value)}
            >
              {range.label}
            </button>
          ))}
        </div>
      </div>

      <div className="chart-container">
        {loading ? (
          <div className="chart-loading">
            <div className="loading-spinner"></div>
            <p>Loading chart data...</p>
          </div>
        ) : (
          <div className="chart-content">
            <div className="price-chart">
              <svg width="100%" height="200" viewBox="0 0 400 200">
                <defs>
                  <linearGradient id="priceGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#4CAF50" stopOpacity="0.3"/>
                    <stop offset="100%" stopColor="#4CAF50" stopOpacity="0.1"/>
                  </linearGradient>
                </defs>
                
                {/* Price line */}
                <polyline
                  fill="none"
                  stroke="#4CAF50"
                  strokeWidth="2"
                  points={chartData.map((point, index) => 
                    `${(index / (chartData.length - 1)) * 400},${200 - (point.price / 300) * 200}`
                  ).join(' ')}
                />
                
                {/* Area fill */}
                <polygon
                  fill="url(#priceGradient)"
                  points={`0,200 ${chartData.map((point, index) => 
                    `${(index / (chartData.length - 1)) * 400},${200 - (point.price / 300) * 200}`
                  ).join(' ')} 400,200`}
                />
              </svg>
            </div>
            
            <div className="volume-chart">
              <svg width="100%" height="60" viewBox="0 0 400 60">
                {chartData.map((point, index) => {
                  const x = (index / (chartData.length - 1)) * 400;
                  const height = (point.volume / 1000000) * 60;
                  return (
                    <rect
                      key={index}
                      x={x - 2}
                      y={60 - height}
                      width="4"
                      height={height}
                      fill="#2196F3"
                      opacity="0.6"
                    />
                  );
                })}
              </svg>
            </div>
          </div>
        )}
      </div>

      <div className="chart-stats">
        <div className="stat-item">
          <span className="stat-label">Open</span>
          <span className="stat-value">{formatPrice(chartData[0]?.price || 0)}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">High</span>
          <span className="stat-value">{formatPrice(Math.max(...chartData.map(d => d.price)))}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Low</span>
          <span className="stat-value">{formatPrice(Math.min(...chartData.map(d => d.price)))}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Volume</span>
          <span className="stat-value">{new Intl.NumberFormat().format(chartData.reduce((sum, d) => sum + d.volume, 0))}</span>
        </div>
      </div>
    </div>
  );
};

export default StockChart; 