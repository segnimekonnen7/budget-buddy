import React, { useState, useEffect } from 'react';
import {
  Box, Card, CardContent, Typography, TextField, Button, Grid, Chip, 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,
  Avatar, Divider, Alert, CircularProgress
} from '@mui/material';
import {
  Search as SearchIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Add as AddIcon,
  Remove as RemoveIcon
} from '@mui/icons-material';

const StockSearch = ({ onAddToWatchlist }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [loading, setLoading] = useState(false);

  // Mock stock data - in real app, this would come from API
  const mockStocks = [
    { symbol: 'AAPL', name: 'Apple Inc.', price: 150.25, change: 2.15, changePercent: 1.45, volume: '45.2M', marketCap: '2.4T' },
    { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 2750.80, change: -15.20, changePercent: -0.55, volume: '12.8M', marketCap: '1.8T' },
    { symbol: 'MSFT', name: 'Microsoft Corporation', price: 310.45, change: 5.75, changePercent: 1.89, volume: '28.9M', marketCap: '2.3T' },
    { symbol: 'TSLA', name: 'Tesla Inc.', price: 245.60, change: -8.40, changePercent: -3.31, volume: '89.1M', marketCap: '780B' },
    { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 135.20, change: 1.80, changePercent: 1.35, volume: '52.3M', marketCap: '1.4T' },
    { symbol: 'META', name: 'Meta Platforms Inc.', price: 320.15, change: 12.45, changePercent: 4.05, volume: '31.7M', marketCap: '820B' },
    { symbol: 'NVDA', name: 'NVIDIA Corporation', price: 485.90, change: 25.10, changePercent: 5.45, volume: '67.2M', marketCap: '1.2T' },
    { symbol: 'NFLX', name: 'Netflix Inc.', price: 485.25, change: -12.75, changePercent: -2.56, volume: '18.9M', marketCap: '215B' }
  ];

  const handleSearch = () => {
    if (!searchTerm.trim()) return;
    
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      const filtered = mockStocks.filter(stock => 
        stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
        stock.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setSearchResults(filtered);
      setLoading(false);
    }, 500);
  };

  const handleStockSelect = (stock) => {
    setSelectedStock(stock);
  };

  const handleAddToWatchlist = (stock) => {
    onAddToWatchlist(stock);
    // Show success message or notification
  };

  useEffect(() => {
    if (searchTerm.length >= 2) {
      handleSearch();
    } else {
      setSearchResults([]);
    }
  }, [searchTerm]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Stock Search & Analysis
      </Typography>
      
      {/* Search Bar */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <TextField
              fullWidth
              label="Search stocks by symbol or company name"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="e.g., AAPL, Apple, Tesla"
              InputProps={{
                endAdornment: loading ? <CircularProgress size={20} /> : <SearchIcon />
              }}
            />
            <Button 
              variant="contained" 
              onClick={handleSearch}
              disabled={!searchTerm.trim()}
            >
              Search
            </Button>
          </Box>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Search Results */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Search Results
              </Typography>
              {searchResults.length === 0 && searchTerm.length >= 2 && !loading && (
                <Alert severity="info">No stocks found matching "{searchTerm}"</Alert>
              )}
              {searchResults.map((stock) => (
                <Box 
                  key={stock.symbol}
                  sx={{ 
                    p: 2, 
                    border: '1px solid #e0e0e0', 
                    borderRadius: 1, 
                    mb: 2,
                    cursor: 'pointer',
                    '&:hover': { backgroundColor: '#f5f5f5' }
                  }}
                  onClick={() => handleStockSelect(stock)}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Avatar sx={{ bgcolor: 'primary.main', width: 40, height: 40 }}>
                        {stock.symbol.charAt(0)}
                      </Avatar>
                      <Box>
                        <Typography variant="h6" fontWeight="bold">
                          {stock.symbol}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {stock.name}
                        </Typography>
                      </Box>
                    </Box>
                    <Button
                      size="small"
                      variant="outlined"
                      startIcon={<AddIcon />}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAddToWatchlist(stock);
                      }}
                    >
                      Watch
                    </Button>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="h6">
                      ${stock.price}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {stock.changePercent > 0 ? (
                        <TrendingUpIcon color="success" fontSize="small" />
                      ) : (
                        <TrendingDownIcon color="error" fontSize="small" />
                      )}
                      <Chip 
                        label={`${stock.changePercent > 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%`}
                        size="small"
                        color={stock.changePercent > 0 ? 'success' : 'error'}
                        variant="outlined"
                      />
                    </Box>
                  </Box>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Stock Details */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Stock Details
              </Typography>
              {selectedStock ? (
                <Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                    <Avatar sx={{ bgcolor: 'primary.main', width: 60, height: 60 }}>
                      {selectedStock.symbol.charAt(0)}
                    </Avatar>
                    <Box>
                      <Typography variant="h4" fontWeight="bold">
                        {selectedStock.symbol}
                      </Typography>
                      <Typography variant="h6" color="text.secondary">
                        {selectedStock.name}
                      </Typography>
                    </Box>
                  </Box>

                  <Grid container spacing={2} sx={{ mb: 3 }}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Current Price
                      </Typography>
                      <Typography variant="h5" fontWeight="bold">
                        ${selectedStock.price}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Change
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {selectedStock.changePercent > 0 ? (
                          <TrendingUpIcon color="success" />
                        ) : (
                          <TrendingDownIcon color="error" />
                        )}
                        <Typography 
                          variant="h5" 
                          fontWeight="bold"
                          color={selectedStock.changePercent > 0 ? 'success.main' : 'error.main'}
                        >
                          ${selectedStock.change} ({selectedStock.changePercent.toFixed(2)}%)
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>

                  <Divider sx={{ my: 2 }} />

                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Volume
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {selectedStock.volume}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Market Cap
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {selectedStock.marketCap}
                      </Typography>
                    </Grid>
                  </Grid>

                  <Box sx={{ mt: 3 }}>
                    <Button 
                      variant="contained" 
                      fullWidth
                      startIcon={<AddIcon />}
                      onClick={() => handleAddToWatchlist(selectedStock)}
                    >
                      Add to Watchlist
                    </Button>
                  </Box>
                </Box>
              ) : (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body1" color="text.secondary">
                    Select a stock to view details
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StockSearch; 