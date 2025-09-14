import React, { useState, useEffect } from 'react';
import {
  Box, CssBaseline, Drawer, List, ListItem, ListItemIcon, ListItemText, Typography, Container, Paper, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, IconButton, TextField, Dialog, DialogActions, DialogContent, DialogTitle, Checkbox, Chip, LinearProgress, Grid, Card, CardContent, Alert, ButtonGroup, FormControlLabel, Switch, Select, MenuItem, FormControl, InputLabel, Badge
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  CalendarToday as CalendarIcon,
  FitnessCenter as GymIcon,
  ContentCut as HairIcon,
  Face as BeardIcon,
  Psychology as AiIcon,
  Code as ProjectIcon,
  Psychology as ReflectionIcon,
  AccountBalanceWallet as AccountBalanceWalletIcon,
  Settings as SettingsIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  NavigateBefore as NavigateBeforeIcon,
  NavigateNext as NavigateNextIcon,
  Today as TodayIcon,
  Schedule as ScheduleIcon,
  Pending as PendingIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import './App.css';

const drawerWidth = 220;

const CATEGORIES = [
  { label: 'Gym', icon: <GymIcon />, key: 'gym', color: '#ff6b6b' },
  { label: 'Hair', icon: <HairIcon />, key: 'hair', color: '#4ecdc4' },
  { label: 'Beard', icon: <BeardIcon />, key: 'beard', color: '#45b7d1' },
  { label: 'AI', icon: <AiIcon />, key: 'ai', color: '#96ceb4' },
  { label: 'Project', icon: <ProjectIcon />, key: 'project', color: '#feca57' },
];

const DURATION_OPTIONS = [
  { value: 'one-time', label: 'One Time' },
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
  { value: 'custom', label: 'Custom (Days)' }
];

const NAV_ITEMS = [
  { key: 'dashboard', label: 'Dashboard', icon: <DashboardIcon /> },
  { key: 'calendar', label: 'Daily Tracker', icon: <CalendarIcon /> },
  { key: 'pending', label: 'Pending Tasks', icon: <PendingIcon /> },
  { key: 'due-today', label: 'Due Today', icon: <TodayIcon /> },
  ...CATEGORIES.map(cat => ({ key: cat.key, label: cat.label, icon: cat.icon })),
  { key: 'payments', label: 'Payments', icon: <AccountBalanceWalletIcon /> },
  { key: 'reflection', label: 'Reflection', icon: <ReflectionIcon /> },
  { key: 'settings', label: 'Settings', icon: <SettingsIcon /> }
];

// Simplified storage functions
const storage = {
  save: (key, data) => localStorage.setItem(key, JSON.stringify(data)),
  load: (key, defaultValue) => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.error('Storage error:', error);
      return defaultValue;
    }
  }
};

function App() {
  const [tab, setTab] = useState('dashboard');
  const [selectedDate, setSelectedDate] = useState(() => storage.load('selectedDate', new Date().toISOString().split('T')[0]));
  const [pushupCount, setPushupCount] = useState(() => storage.load('pushupCount', 0));
  const [routines, setRoutines] = useState(() => storage.load('routines', {}));
  const [reflections, setReflections] = useState(() => storage.load('reflections', {}));
  const [payments, setPayments] = useState(() => storage.load('payments', []));
  const [settings, setSettings] = useState(() => storage.load('settings', { dataProtectionEnabled: true }));

  // Form states
  const [routineDialog, setRoutineDialog] = useState(false);
  const [routineForm, setRoutineForm] = useState({ 
    task: '', 
    frequency: '', 
    time: '', 
    selectedDays: [],
    duration: 'one-time',
    customDays: 1,
    dueDate: '',
    priority: 'medium'
  });
  const [currentCategory, setCurrentCategory] = useState('gym');
  const [editingRoutine, setEditingRoutine] = useState(null);

  // Auto-save everything
  useEffect(() => storage.save('routines', routines), [routines]);
  useEffect(() => storage.save('selectedDate', selectedDate), [selectedDate]);
  useEffect(() => storage.save('pushupCount', pushupCount), [pushupCount]);
  useEffect(() => storage.save('reflections', reflections), [reflections]);
  useEffect(() => storage.save('payments', payments), [payments]);
  useEffect(() => storage.save('settings', settings), [settings]);

  // Helper functions
  const getDayOfWeek = (dateString) => {
    const [year, month, day] = dateString.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][date.getDay()];
  };

  const isScheduledForDate = (routine, dateString) => {
    if (!routine.scheduledDays?.length) return false;
    return routine.scheduledDays.includes(getDayOfWeek(dateString));
  };

  const isDueToday = (routine) => {
    const today = new Date().toISOString().split('T')[0];
    
    // Check if it's scheduled for today
    if (routine.scheduledDays?.length && isScheduledForDate(routine, today)) {
      return !routine.completedDates.includes(today);
    }
    
    // Check if it has a due date
    if (routine.dueDate && routine.dueDate <= today) {
      return !routine.completedDates.includes(today);
    }
    
    return false;
  };

  const isPending = (routine) => {
    const today = new Date().toISOString().split('T')[0];
    
    // If it's a one-time task with a due date
    if (routine.duration === 'one-time' && routine.dueDate) {
      return routine.dueDate >= today && !routine.completedDates.includes(routine.dueDate);
    }
    
    // If it's recurring and scheduled for today
    if (routine.scheduledDays?.length && isScheduledForDate(routine, today)) {
      return !routine.completedDates.includes(today);
    }
    
    return false;
  };

  const getTaskStatus = (routine) => {
    if (isDueToday(routine)) return 'due-today';
    if (isPending(routine)) return 'pending';
    return 'completed';
  };

  const toggleRoutine = (category, routineIdx) => {
    const routine = routines[category][routineIdx];
    const today = new Date().toISOString().split('T')[0];
    
    // For one-time tasks with due dates
    if (routine.duration === 'one-time' && routine.dueDate) {
      const isCompleted = routine.completedDates.includes(routine.dueDate);
      setRoutines(prev => {
        const updated = { ...prev };
        updated[category][routineIdx] = {
          ...routine,
          completedDates: isCompleted ? 
            routine.completedDates.filter(d => d !== routine.dueDate) :
            [...routine.completedDates, routine.dueDate]
        };
        return updated;
      });
      return;
    }
    
    // For scheduled tasks
    if (!isScheduledForDate(routine, selectedDate)) {
      alert(routine.scheduledDays?.length ? 
        `Scheduled for: ${routine.scheduledDays.join(', ')}` : 
        'Please set scheduled days first');
      return;
    }

    setRoutines(prev => {
      const updated = { ...prev };
      const isCompleted = routine.completedDates.includes(selectedDate);
      updated[category][routineIdx] = {
        ...routine,
        completedDates: isCompleted ? 
          routine.completedDates.filter(d => d !== selectedDate) :
          [...routine.completedDates, selectedDate]
      };
      return updated;
    });

    if (routine.frequency === 'Daily' && !routine.completedDates.includes(selectedDate)) {
      setPushupCount(prev => prev + 40);
    }
  };

  const saveRoutine = () => {
    const newRoutine = {
      ...routineForm,
      id: Date.now(),
      completedDates: editingRoutine ? editingRoutine.completedDates : [],
      scheduledDays: routineForm.selectedDays,
      createdAt: new Date().toISOString(),
      lastUpdated: new Date().toISOString()
    };

    setRoutines(prev => {
      const updated = { ...prev };
      if (!updated[currentCategory]) updated[currentCategory] = [];
      
      if (editingRoutine) {
        updated[currentCategory] = updated[currentCategory].map(r => 
          r.id === editingRoutine.id ? { ...newRoutine, id: editingRoutine.id, createdAt: editingRoutine.createdAt } : r
        );
      } else {
        updated[currentCategory].push(newRoutine);
      }
      return updated;
    });

    setRoutineDialog(false);
    setRoutineForm({ 
      task: '', 
      frequency: '', 
      time: '', 
      selectedDays: [], 
      duration: 'one-time', 
      customDays: 1, 
      dueDate: '', 
      priority: 'medium' 
    });
    setEditingRoutine(null);
  };

  const deleteRoutine = (category, routineIdx) => {
    setRoutines(prev => ({
      ...prev,
      [category]: prev[category].filter((_, i) => i !== routineIdx)
    }));
  };

  const openRoutineDialog = (category, routine = null) => {
    setCurrentCategory(category);
    setEditingRoutine(routine);
    if (routine) {
      setRoutineForm({
        task: routine.task,
        frequency: routine.frequency,
        time: routine.time,
        selectedDays: routine.scheduledDays || [],
        duration: routine.duration,
        customDays: routine.customDays,
        dueDate: routine.dueDate,
        priority: routine.priority
      });
    } else {
      setRoutineForm({ task: '', frequency: '', time: '', selectedDays: [], duration: 'one-time', customDays: 1, dueDate: '', priority: 'medium' });
    }
    setRoutineDialog(true);
  };

  const getMissedRoutines = () => {
    const missed = [];
    const today = new Date();
    
    for (let i = 1; i <= 7; i++) {
      const checkDate = new Date(today);
      checkDate.setDate(today.getDate() - i);
      const checkDateString = checkDate.toISOString().split('T')[0];
      
      CATEGORIES.forEach(category => {
        const categoryRoutines = routines[category.key] || [];
        categoryRoutines.forEach(routine => {
          if (routine.scheduledDays?.length && isScheduledForDate(routine, checkDateString) && 
              !routine.completedDates.includes(checkDateString)) {
            missed.push({
              date: checkDateString,
              dayOfWeek: getDayOfWeek(checkDateString),
              category: category.label,
              routine: routine.task,
              daysAgo: i
            });
          }
        });
      });
    }
    return missed;
  };

  const missedRoutines = getMissedRoutines();

  const clearMissedRoutine = (missedRoutine) => {
    setRoutines(prev => {
      const updated = { ...prev };
      const categoryKey = CATEGORIES.find(cat => cat.label === missedRoutine.category)?.key;
      if (categoryKey && updated[categoryKey]) {
        const routineIdx = updated[categoryKey].findIndex(r => r.task === missedRoutine.routine);
        if (routineIdx !== -1) {
          const routine = updated[categoryKey][routineIdx];
          if (!routine.completedDates.includes(missedRoutine.date)) {
            updated[categoryKey][routineIdx] = {
              ...routine,
              completedDates: [...routine.completedDates, missedRoutine.date]
            };
          }
        }
      }
      return updated;
    });
  };

  const clearAllMissedRoutines = () => {
    setRoutines(prev => {
      const updated = { ...prev };
      const today = new Date();
      
      for (let i = 1; i <= 7; i++) {
        const checkDate = new Date(today);
        checkDate.setDate(today.getDate() - i);
        const checkDateString = checkDate.toISOString().split('T')[0];
        
        CATEGORIES.forEach(category => {
          const categoryRoutines = updated[category.key] || [];
          categoryRoutines.forEach((routine, routineIdx) => {
            if (routine.scheduledDays?.length && isScheduledForDate(routine, checkDateString) && 
                !routine.completedDates.includes(checkDateString)) {
              updated[category.key][routineIdx] = {
                ...routine,
                completedDates: [...routine.completedDates, checkDateString]
              };
            }
          });
        });
      }
      return updated;
    });
  };

  const backupData = () => {
    const backup = { routines, reflections, payments, selectedDate, pushupCount, timestamp: new Date().toISOString() };
    localStorage.setItem('dataBackup', JSON.stringify(backup));
    setSettings(prev => ({ ...prev, lastBackupDate: new Date().toISOString() }));
    alert('✅ Backup created!');
  };

  const restoreData = () => {
    const backup = localStorage.getItem('dataBackup');
    if (backup) {
      try {
        const data = JSON.parse(backup);
        setRoutines(data.routines || routines);
        setReflections(data.reflections || reflections);
        setPayments(data.payments || payments);
        setSelectedDate(data.selectedDate || selectedDate);
        setPushupCount(data.pushupCount || pushupCount);
        alert('✅ Data restored!');
      } catch (error) {
        alert('❌ Restore failed: ' + error.message);
      }
    } else {
      alert('❌ No backup found!');
    }
  };

  const clearAllData = () => {
    if (window.confirm('⚠️ Delete ALL data permanently?')) {
      localStorage.clear();
      window.location.reload();
    }
  };

  // Navigation helpers
  const navigateDate = (direction) => {
    const date = new Date(selectedDate);
    date.setDate(date.getDate() + direction);
    setSelectedDate(date.toISOString().split('T')[0]);
  };

  const goToDate = (dateType) => {
    const today = new Date();
    if (dateType === 'yesterday') today.setDate(today.getDate() - 1);
    if (dateType === 'tomorrow') today.setDate(today.getDate() + 1);
    setSelectedDate(today.toISOString().split('T')[0]);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      
      {/* Sidebar */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            background: 'rgba(0, 0, 0, 0.8)',
            backdropFilter: 'blur(10px)',
            borderRight: '1px solid rgba(255, 255, 255, 0.1)'
          }
        }}
      >
        <Box sx={{ overflow: 'auto', mt: 8 }}>
          <List>
            {NAV_ITEMS.map((item) => {
              // Calculate counts for pending and due today
              let badgeCount = 0;
              if (item.key === 'pending') {
                CATEGORIES.forEach(category => {
                  const categoryRoutines = routines[category.key] || [];
                  categoryRoutines.forEach(routine => {
                    if (isPending(routine)) badgeCount++;
                  });
                });
              } else if (item.key === 'due-today') {
                CATEGORIES.forEach(category => {
                  const categoryRoutines = routines[category.key] || [];
                  categoryRoutines.forEach(routine => {
                    if (isDueToday(routine)) badgeCount++;
                  });
                });
              }

              return (
                <ListItem key={item.key} disablePadding>
                  <ListItemButton
                    onClick={() => setTab(item.key)}
                    selected={tab === item.key}
                    sx={{
                      color: 'white',
                      '&.Mui-selected': {
                        background: 'rgba(255, 255, 255, 0.2)',
                        '&:hover': { background: 'rgba(255, 255, 255, 0.3)' }
                      },
                      '&:hover': { background: 'rgba(255, 255, 255, 0.1)' }
                    }}
                  >
                    <ListItemIcon sx={{ color: 'white', minWidth: 40 }}>
                      {badgeCount > 0 ? (
                        <Badge badgeContent={badgeCount} color="error">
                          {item.icon}
                        </Badge>
                      ) : (
                        item.icon
                      )}
                    </ListItemIcon>
                    <ListItemText primary={item.label} />
                  </ListItemButton>
                </ListItem>
              );
            })}
          </List>
        </Box>
      </Drawer>

      {/* Main Content */}
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Container maxWidth="xl">
          
          {/* Dashboard */}
          {tab === 'dashboard' && (
            <Paper sx={{ p: 3 }} className="glass-card">
              <Typography variant="h4" gutterBottom className="animated-text">📊 Dashboard</Typography>
              
              {/* Missed Routines Alert */}
              {missedRoutines.length > 0 && (
                <Alert severity="warning" sx={{ mb: 3 }}>
                  <AlertTitle>⚠️ Missed Routines ({missedRoutines.length})</AlertTitle>
                  {missedRoutines.slice(0, 3).map((missed, idx) => (
                    <Box key={idx} sx={{ mb: 1 }}>
                      {missed.dayOfWeek} ({missed.daysAgo} days ago): {missed.routine} ({missed.category})
                      <Button size="small" onClick={() => clearMissedRoutine(missed)} sx={{ ml: 1 }}>
                        Clear
                      </Button>
                    </Box>
                  ))}
                  {missedRoutines.length > 3 && (
                    <Button onClick={clearAllMissedRoutines} sx={{ mt: 1 }}>
                      Clear All Missed
                    </Button>
                  )}
                </Alert>
              )}

              {/* Pushup Counter */}
              <Card sx={{ mb: 3 }} className="glass-card">
                <CardContent>
                  <Typography variant="h6" gutterBottom>💪 Pushup Penalty</Typography>
                  <Typography variant="h3" color="error">{pushupCount}</Typography>
                  <Button onClick={() => setPushupCount(0)} variant="outlined" sx={{ mt: 1 }}>
                    Reset Pushups
                  </Button>
                </CardContent>
              </Card>

              {/* Category Progress */}
              <Grid container spacing={3}>
                {CATEGORIES.map(category => {
                  const categoryRoutines = routines[category.key] || [];
                  const progress = categoryRoutines.length > 0 ? 
                    categoryRoutines.reduce((sum, routine) => {
                      const completedThisMonth = routine.completedDates.filter(date => 
                        date.startsWith(new Date().toISOString().slice(0, 7))
                      ).length;
                      return sum + (completedThisMonth / 30) * 100;
                    }, 0) / categoryRoutines.length : 0;

                  return (
                    <Grid item xs={12} sm={6} md={4} key={category.key}>
                      <Card className="glass-card">
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            {category.icon} {category.label}
                          </Typography>
                          <Typography variant="h4" color="primary">
                            {Math.round(progress)}%
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={progress} 
                            sx={{ height: 8, borderRadius: 4, mt: 1 }}
                          />
                        </CardContent>
                      </Card>
                    </Grid>
                  );
                })}
              </Grid>
            </Paper>
          )}

          {/* Daily Tracker */}
          {tab === 'calendar' && (
            <Paper sx={{ p: 3 }} className="glass-card">
              <Typography variant="h4" gutterBottom className="animated-text">📅 Daily Tracker</Typography>
              
              {/* Date Navigation */}
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <ButtonGroup variant="outlined" size="small">
                  <Button onClick={() => navigateDate(-1)}><NavigateBeforeIcon /></Button>
                  <Button onClick={() => navigateDate(1)}><NavigateNextIcon /></Button>
                </ButtonGroup>
                
                <ButtonGroup variant="contained" size="small">
                  <Button onClick={() => goToDate('yesterday')}>Yesterday</Button>
                  <Button onClick={() => goToDate('today')}><TodayIcon sx={{ mr: 1 }} />Today</Button>
                  <Button onClick={() => goToDate('tomorrow')}>Tomorrow</Button>
                </ButtonGroup>
                
                <TextField
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  size="small"
                />
              </Box>

              {/* Routines for Selected Date */}
              <Typography variant="h6" gutterBottom>
                Routines for {new Date(selectedDate).toLocaleDateString()}
              </Typography>
              
              {CATEGORIES.map(category => {
                const categoryRoutines = routines[category.key] || [];
                return categoryRoutines.length > 0 && (
                  <Card key={category.key} sx={{ mb: 2 }} className="glass-card">
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {category.icon} {category.label}
                      </Typography>
                      <Grid container spacing={1}>
                        {categoryRoutines.map((routine, idx) => {
                          const isCompleted = routine.completedDates.includes(selectedDate);
                          const isScheduled = isScheduledForDate(routine, selectedDate);
                          const isDisabled = !isScheduled;
                          
                          return (
                            <Grid item xs={12} key={routine.id}>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                <Checkbox
                                  checked={isCompleted}
                                  onChange={() => toggleRoutine(category.key, idx)}
                                  disabled={isDisabled}
                                  sx={{ 
                                    color: 'rgba(255, 255, 255, 0.7)',
                                    '&.Mui-checked': { color: 'primary.main' }
                                  }}
                                />
                                <Typography 
                                  sx={{ 
                                    textDecoration: isCompleted ? 'line-through' : 'none',
                                    opacity: isDisabled ? 0.5 : 1
                                  }}
                                >
                                  {routine.task} ({routine.time})
                                </Typography>
                                {isDisabled && (
                                  <Chip 
                                    label={routine.scheduledDays?.join(', ') || 'No days set'} 
                                    size="small" 
                                    color="warning"
                                  />
                                )}
                              </Box>
                            </Grid>
                          );
                        })}
                      </Grid>
                    </CardContent>
                  </Card>
                );
              })}
            </Paper>
          )}

          {/* Pending Tasks */}
          {tab === 'pending' && (
            <Paper sx={{ p: 3 }} className="glass-card">
              <Typography variant="h4" gutterBottom className="animated-text">
                <PendingIcon sx={{ mr: 1 }} /> Pending Tasks
              </Typography>
              
              {(() => {
                const pendingTasks = [];
                CATEGORIES.forEach(category => {
                  const categoryRoutines = routines[category.key] || [];
                  categoryRoutines.forEach((routine, idx) => {
                    if (isPending(routine)) {
                      pendingTasks.push({ ...routine, category: category.key, categoryLabel: category.label, routineIdx: idx });
                    }
                  });
                });

                if (pendingTasks.length === 0) {
                  return (
                    <Alert severity="info">
                      <AlertTitle>🎉 All Caught Up!</AlertTitle>
                      No pending tasks at the moment. Great job!
                    </Alert>
                  );
                }

                return (
                  <Grid container spacing={2}>
                    {pendingTasks.map((task, idx) => (
                      <Grid item xs={12} md={6} lg={4} key={`${task.category}-${task.routineIdx}`}>
                        <Card className="glass-card">
                          <CardContent>
                            <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
                              <Typography variant="h6" color="primary">
                                {task.task}
                              </Typography>
                              <Chip 
                                label={task.categoryLabel} 
                                size="small" 
                                sx={{ backgroundColor: CATEGORIES.find(c => c.key === task.category)?.color }}
                              />
                            </Box>
                            <Typography variant="body2" color="text.secondary" mb={1}>
                              {task.time} • {task.duration === 'one-time' ? 'One Time' : task.duration}
                            </Typography>
                            {task.dueDate && (
                              <Typography variant="body2" color="warning.main" mb={1}>
                                Due: {new Date(task.dueDate).toLocaleDateString()}
                              </Typography>
                            )}
                            {task.scheduledDays?.length > 0 && (
                              <Typography variant="body2" color="info.main" mb={1}>
                                Scheduled: {task.scheduledDays.join(', ')}
                              </Typography>
                            )}
                            <Button 
                              variant="contained" 
                              size="small" 
                              onClick={() => toggleRoutine(task.category, task.routineIdx)}
                              startIcon={<CheckCircleIcon />}
                            >
                              Mark Complete
                            </Button>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                );
              })()}
            </Paper>
          )}

          {/* Due Today Tasks */}
          {tab === 'due-today' && (
            <Paper sx={{ p: 3 }} className="glass-card">
              <Typography variant="h4" gutterBottom className="animated-text">
                <TodayIcon sx={{ mr: 1 }} /> Due Today
              </Typography>
              
              {(() => {
                const dueTodayTasks = [];
                CATEGORIES.forEach(category => {
                  const categoryRoutines = routines[category.key] || [];
                  categoryRoutines.forEach((routine, idx) => {
                    if (isDueToday(routine)) {
                      dueTodayTasks.push({ ...routine, category: category.key, categoryLabel: category.label, routineIdx: idx });
                    }
                  });
                });

                if (dueTodayTasks.length === 0) {
                  return (
                    <Alert severity="success">
                      <AlertTitle>✅ All Done!</AlertTitle>
                      No tasks due today. You're all caught up!
                    </Alert>
                  );
                }

                return (
                  <Grid container spacing={2}>
                    {dueTodayTasks.map((task, idx) => (
                      <Grid item xs={12} md={6} lg={4} key={`${task.category}-${task.routineIdx}`}>
                        <Card className="glass-card" sx={{ border: '2px solid #ff6b6b' }}>
                          <CardContent>
                            <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
                              <Typography variant="h6" color="error">
                                {task.task}
                              </Typography>
                              <Chip 
                                label="DUE TODAY" 
                                size="small" 
                                color="error"
                                icon={<WarningIcon />}
                              />
                            </Box>
                            <Typography variant="body2" color="text.secondary" mb={1}>
                              {task.time} • {task.categoryLabel}
                            </Typography>
                            {task.dueDate && (
                              <Typography variant="body2" color="error.main" mb={1}>
                                Due: {new Date(task.dueDate).toLocaleDateString()}
                              </Typography>
                            )}
                            {task.scheduledDays?.length > 0 && (
                              <Typography variant="body2" color="info.main" mb={1}>
                                Scheduled: {task.scheduledDays.join(', ')}
                              </Typography>
                            )}
                            <Button 
                              variant="contained" 
                              color="error" 
                              size="small" 
                              onClick={() => toggleRoutine(task.category, task.routineIdx)}
                              startIcon={<CheckCircleIcon />}
                            >
                              Complete Now
                            </Button>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                );
              })()}
            </Paper>
          )}

          {/* Category Routines */}
          {CATEGORIES.map(category => 
            tab === category.key && (
              <Paper key={category.key} sx={{ p: 3 }} className="glass-card">
                <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                  <Typography variant="h5" className="animated-text">
                    {category.icon} {category.label} Routines
                  </Typography>
                  <Button 
                    variant="contained" 
                    startIcon={<AddIcon />} 
                    onClick={() => openRoutineDialog(category.key)}
                    sx={{ background: 'rgba(255, 255, 255, 0.3)' }}
                  >
                    Add Routine
                  </Button>
                </Box>
                
                <TableContainer component={Paper} className="glass-card">
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Task</TableCell>
                        <TableCell>Duration</TableCell>
                        <TableCell>Time</TableCell>
                        <TableCell>Due Date</TableCell>
                        <TableCell>Priority</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {(routines[category.key] || []).map((routine, idx) => {
                        const status = getTaskStatus(routine);
                        return (
                          <TableRow key={routine.id}>
                            <TableCell>
                              <Typography variant="body2" fontWeight="medium">
                                {routine.task}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Chip 
                                label={routine.duration === 'one-time' ? 'One Time' : routine.duration} 
                                size="small" 
                                color={routine.duration === 'one-time' ? 'default' : 'primary'}
                              />
                            </TableCell>
                            <TableCell>{routine.time}</TableCell>
                            <TableCell>
                              {routine.dueDate ? new Date(routine.dueDate).toLocaleDateString() : '-'}
                            </TableCell>
                            <TableCell>
                              <Chip 
                                label={routine.priority} 
                                size="small" 
                                color={
                                  routine.priority === 'urgent' ? 'error' :
                                  routine.priority === 'high' ? 'warning' :
                                  routine.priority === 'medium' ? 'info' : 'default'
                                }
                              />
                            </TableCell>
                            <TableCell>
                              <Chip 
                                label={status === 'due-today' ? 'Due Today' : status === 'pending' ? 'Pending' : 'Completed'} 
                                size="small" 
                                color={status === 'due-today' ? 'error' : status === 'pending' ? 'warning' : 'success'}
                                icon={status === 'due-today' ? <WarningIcon /> : status === 'pending' ? <PendingIcon /> : <CheckCircleIcon />}
                              />
                            </TableCell>
                            <TableCell>
                              <IconButton onClick={() => openRoutineDialog(category.key, routine)}>
                                <EditIcon />
                              </IconButton>
                              <IconButton onClick={() => deleteRoutine(category.key, idx)}>
                                <DeleteIcon />
                              </IconButton>
                            </TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            )
          )}

          {/* Settings */}
          {tab === 'settings' && (
            <Paper sx={{ p: 3 }} className="glass-card">
              <Typography variant="h4" gutterBottom className="animated-text">⚙️ Settings</Typography>
              
              <Card sx={{ mb: 3 }} className="glass-card">
                <CardContent>
                  <Typography variant="h6" gutterBottom>🛡️ Data Protection</Typography>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.dataProtectionEnabled}
                        onChange={(e) => setSettings(prev => ({
                          ...prev,
                          dataProtectionEnabled: e.target.checked
                        }))}
                      />
                    }
                    label="Enable Data Protection"
                  />
                </CardContent>
              </Card>

              <Card sx={{ mb: 3 }} className="glass-card">
                <CardContent>
                  <Typography variant="h6" gutterBottom>💾 Backup & Restore</Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <Button fullWidth variant="contained" onClick={backupData}>
                        📦 Create Backup
                      </Button>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Button fullWidth variant="outlined" onClick={restoreData}>
                        🔄 Restore from Backup
                      </Button>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              <Card className="glass-card">
                <CardContent>
                  <Typography variant="h6" gutterBottom color="error">⚠️ Danger Zone</Typography>
                  <Button variant="outlined" color="error" onClick={clearAllData}>
                    🗑️ Clear All Data
                  </Button>
                </CardContent>
              </Card>
            </Paper>
          )}

          {/* Routine Dialog */}
          <Dialog open={routineDialog} onClose={() => setRoutineDialog(false)} maxWidth="md" fullWidth>
            <DialogTitle>
              {editingRoutine ? 'Edit Task' : 'Add New Task'}
            </DialogTitle>
            <DialogContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    autoFocus
                    margin="dense"
                    label="Task Name"
                    fullWidth
                    value={routineForm.task}
                    onChange={(e) => setRoutineForm({...routineForm, task: e.target.value})}
                  />
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <TextField
                    margin="dense"
                    label="Estimated Time"
                    fullWidth
                    placeholder="e.g., 30 minutes, 1 hour"
                    value={routineForm.time}
                    onChange={(e) => setRoutineForm({...routineForm, time: e.target.value})}
                  />
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth margin="dense">
                    <InputLabel>Duration Type</InputLabel>
                    <Select
                      value={routineForm.duration}
                      onChange={(e) => setRoutineForm({...routineForm, duration: e.target.value})}
                      label="Duration Type"
                    >
                      {DURATION_OPTIONS.map(option => (
                        <MenuItem key={option.value} value={option.value}>
                          {option.label}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                
                {routineForm.duration === 'custom' && (
                  <Grid item xs={12} md={6}>
                    <TextField
                      margin="dense"
                      label="Custom Days"
                      type="number"
                      fullWidth
                      value={routineForm.customDays}
                      onChange={(e) => setRoutineForm({...routineForm, customDays: parseInt(e.target.value) || 1})}
                      inputProps={{ min: 1, max: 365 }}
                    />
                  </Grid>
                )}
                
                {routineForm.duration === 'one-time' && (
                  <Grid item xs={12} md={6}>
                    <TextField
                      margin="dense"
                      label="Due Date"
                      type="date"
                      fullWidth
                      value={routineForm.dueDate}
                      onChange={(e) => setRoutineForm({...routineForm, dueDate: e.target.value})}
                      InputLabelProps={{ shrink: true }}
                    />
                  </Grid>
                )}
                
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth margin="dense">
                    <InputLabel>Priority</InputLabel>
                    <Select
                      value={routineForm.priority}
                      onChange={(e) => setRoutineForm({...routineForm, priority: e.target.value})}
                      label="Priority"
                    >
                      <MenuItem value="low">Low</MenuItem>
                      <MenuItem value="medium">Medium</MenuItem>
                      <MenuItem value="high">High</MenuItem>
                      <MenuItem value="urgent">Urgent</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                
                <Grid item xs={12}>
                  <Typography variant="subtitle1" sx={{ mb: 1, mt: 2 }}>
                    Scheduled Days (for recurring tasks):
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                    {['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].map((day) => (
                      <Box key={day} sx={{ display: 'flex', alignItems: 'center' }}>
                        <Checkbox
                          checked={routineForm.selectedDays.includes(day)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setRoutineForm({
                                ...routineForm,
                                selectedDays: [...routineForm.selectedDays, day]
                              });
                            } else {
                              setRoutineForm({
                                ...routineForm,
                                selectedDays: routineForm.selectedDays.filter(d => d !== day)
                              });
                            }
                          }}
                        />
                        <Typography>{day}</Typography>
                      </Box>
                    ))}
                  </Box>
                </Grid>
              </Grid>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setRoutineDialog(false)}>Cancel</Button>
              <Button onClick={saveRoutine} variant="contained">Save Task</Button>
            </DialogActions>
          </Dialog>
        </Container>
      </Box>
    </Box>
  );
}

export default App; 