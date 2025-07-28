import React, { useState } from 'react';
import {
  Box, Card, CardContent, Typography, Button, Grid, Chip, 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Dialog, DialogTitle, DialogContent, DialogActions, TextField, MenuItem,
  Avatar, Divider
} from '@mui/material';
import {
  Add as AddIcon,
  Remove as RemoveIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon
} from '@mui/icons-material';

const Portfolio = ({ portfolio, setPortfolio, user, setUser }) => {
  const [buyDialog, setBuyDialog] = useState(false);
  const [sellDialog, setSellDialog] = useState(false);
  const [selectedStock, setSelectedStock] = useState(null);
  const [transactionForm, setTransactionForm] = useState({
    shares: '',
    price: ''
  });

  const handleBuy = () => {
    const totalCost = parseFloat(transactionForm.shares) * parseFloat(transactionForm.price);
    if (totalCost > user.balance) {
      alert('Insufficient funds!');
      return;
    }

    const existingStock = portfolio.find(stock => stock.symbol === selectedStock.symbol);
    if (existingStock) {
      // Update existing position
      const newShares = existingStock.shares + parseFloat(transactionForm.shares);
      const newAvgPrice = ((existingStock.shares * existingStock.avgPrice) + totalCost) / newShares;
      
      setPortfolio(prev => prev.map(stock => 
        stock.symbol === selectedStock.symbol 
          ? { ...stock, shares: newShares, avgPrice: newAvgPrice }
          : stock
      ));
    } else {
      // Add new position
      setPortfolio(prev => [...prev, {
        ...selectedStock,
        shares: parseFloat(transactionForm.shares),
        avgPrice: parseFloat(transactionForm.price),
        currentPrice: parseFloat(transactionForm.price)
      }]);
    }

    setUser(prev => ({ ...prev, balance: prev.balance - totalCost }));
    setBuyDialog(false);
    setTransactionForm({ shares: '', price: '' });
  };

  const handleSell = () => {
    const existingStock = portfolio.find(stock => stock.symbol === selectedStock.symbol);
    if (!existingStock || existingStock.shares < parseFloat(transactionForm.shares)) {
      alert('Insufficient shares!');
      return;
    }

    const totalValue = parseFloat(transactionForm.shares) * parseFloat(transactionForm.price);
    const newShares = existingStock.shares - parseFloat(transactionForm.shares);

    if (newShares === 0) {
      // Remove position entirely
      setPortfolio(prev => prev.filter(stock => stock.symbol !== selectedStock.symbol));
    } else {
      // Update position
      setPortfolio(prev => prev.map(stock => 
        stock.symbol === selectedStock.symbol 
          ? { ...stock, shares: newShares }
          : stock
      ));
    }

    setUser(prev => ({ ...prev, balance: prev.balance + totalValue }));
    setSellDialog(false);
    setTransactionForm({ shares: '', price: '' });
  };

  const openBuyDialog = (stock) => {
    setSelectedStock(stock);
    setTransactionForm({ shares: '', price: stock.currentPrice || stock.price });
    setBuyDialog(true);
  };

  const openSellDialog = (stock) => {
    setSelectedStock(stock);
    setTransactionForm({ shares: '', price: stock.currentPrice || stock.price });
    setSellDialog(true);
  };

  const totalPortfolioValue = portfolio.reduce((total, stock) => {
    return total + (stock.shares * (stock.currentPrice || stock.price));
  }, 0);

  const totalGainLoss = portfolio.reduce((total, stock) => {
    const currentValue = stock.shares * (stock.currentPrice || stock.price);
    const costBasis = stock.shares * stock.avgPrice;
    return total + (currentValue - costBasis);
  }, 0);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Portfolio
      </Typography>

      {/* Portfolio Summary */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Total Value
              </Typography>
              <Typography variant="h4" color="primary">
                ${totalPortfolioValue.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Total Gain/Loss
              </Typography>
              <Typography 
                variant="h4" 
                color={totalGainLoss >= 0 ? 'success.main' : 'error.main'}
              >
                ${totalGainLoss.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Available Cash
              </Typography>
              <Typography variant="h4" color="secondary">
                ${user.balance.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Positions
              </Typography>
              <Typography variant="h4" color="primary">
                {portfolio.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Holdings Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Holdings
          </Typography>
          {portfolio.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="body1" color="text.secondary">
                No positions yet. Start by buying some stocks!
              </Typography>
            </Box>
          ) : (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Stock</TableCell>
                    <TableCell>Shares</TableCell>
                    <TableCell>Avg Price</TableCell>
                    <TableCell>Current Price</TableCell>
                    <TableCell>Market Value</TableCell>
                    <TableCell>Gain/Loss</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {portfolio.map((stock) => {
                    const currentValue = stock.shares * (stock.currentPrice || stock.price);
                    const costBasis = stock.shares * stock.avgPrice;
                    const gainLoss = currentValue - costBasis;
                    const gainLossPercent = (gainLoss / costBasis) * 100;

                    return (
                      <TableRow key={stock.symbol}>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                            <Avatar sx={{ bgcolor: 'primary.main' }}>
                              {stock.symbol.charAt(0)}
                            </Avatar>
                            <Box>
                              <Typography variant="subtitle1" fontWeight="bold">
                                {stock.symbol}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                {stock.name}
                              </Typography>
                            </Box>
                          </Box>
                        </TableCell>
                        <TableCell>{stock.shares}</TableCell>
                        <TableCell>${stock.avgPrice.toFixed(2)}</TableCell>
                        <TableCell>${(stock.currentPrice || stock.price).toFixed(2)}</TableCell>
                        <TableCell>${currentValue.toLocaleString()}</TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            {gainLoss >= 0 ? (
                              <TrendingUpIcon color="success" fontSize="small" />
                            ) : (
                              <TrendingDownIcon color="error" fontSize="small" />
                            )}
                            <Chip 
                              label={`${gainLossPercent > 0 ? '+' : ''}${gainLossPercent.toFixed(2)}%`}
                              size="small"
                              color={gainLoss >= 0 ? 'success' : 'error'}
                              variant="outlined"
                            />
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Button
                              size="small"
                              variant="outlined"
                              startIcon={<AddIcon />}
                              onClick={() => openBuyDialog(stock)}
                            >
                              Buy
                            </Button>
                            <Button
                              size="small"
                              variant="outlined"
                              color="error"
                              startIcon={<RemoveIcon />}
                              onClick={() => openSellDialog(stock)}
                            >
                              Sell
                            </Button>
                          </Box>
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </CardContent>
      </Card>

      {/* Buy Dialog */}
      <Dialog open={buyDialog} onClose={() => setBuyDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Buy {selectedStock?.symbol}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Number of Shares"
                type="number"
                value={transactionForm.shares}
                onChange={(e) => setTransactionForm(prev => ({ ...prev, shares: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Price per Share"
                type="number"
                value={transactionForm.price}
                onChange={(e) => setTransactionForm(prev => ({ ...prev, price: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="h6">
                Total Cost: ${(parseFloat(transactionForm.shares) * parseFloat(transactionForm.price)).toFixed(2)}
              </Typography>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBuyDialog(false)}>Cancel</Button>
          <Button onClick={handleBuy} variant="contained">Buy</Button>
        </DialogActions>
      </Dialog>

      {/* Sell Dialog */}
      <Dialog open={sellDialog} onClose={() => setSellDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Sell {selectedStock?.symbol}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Number of Shares"
                type="number"
                value={transactionForm.shares}
                onChange={(e) => setTransactionForm(prev => ({ ...prev, shares: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Price per Share"
                type="number"
                value={transactionForm.price}
                onChange={(e) => setTransactionForm(prev => ({ ...prev, price: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="h6">
                Total Value: ${(parseFloat(transactionForm.shares) * parseFloat(transactionForm.price)).toFixed(2)}
              </Typography>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSellDialog(false)}>Cancel</Button>
          <Button onClick={handleSell} variant="contained" color="error">Sell</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Portfolio; 