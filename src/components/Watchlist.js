import React from 'react';
import {
  Box, Card, CardContent, Typography, Button, Grid, Chip, 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Avatar, IconButton
} from '@mui/material';
import {
  Remove as RemoveIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon
} from '@mui/icons-material';

const Watchlist = ({ watchlist, setWatchlist }) => {
  const handleRemove = (symbol) => {
    setWatchlist(prev => prev.filter(stock => stock.symbol !== symbol));
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Watchlist
      </Typography>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Watched Stocks ({watchlist.length})
          </Typography>
          {watchlist.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="body1" color="text.secondary">
                No stocks in your watchlist. Add some from the Stock Search!
              </Typography>
            </Box>
          ) : (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Stock</TableCell>
                    <TableCell>Price</TableCell>
                    <TableCell>Change</TableCell>
                    <TableCell>Volume</TableCell>
                    <TableCell>Market Cap</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {watchlist.map((stock) => (
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
                      <TableCell>
                        <Typography variant="h6">
                          ${stock.price}
                        </Typography>
                      </TableCell>
                      <TableCell>
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
                      </TableCell>
                      <TableCell>{stock.volume}</TableCell>
                      <TableCell>{stock.marketCap}</TableCell>
                      <TableCell>
                        <IconButton
                          color="error"
                          onClick={() => handleRemove(stock.symbol)}
                        >
                          <RemoveIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default Watchlist; 