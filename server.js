#!/usr/bin/env node
/**
 * Real-time Collaboration Platform
 * Transformed from interview prep to real-time collaboration system
 */

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// In-memory storage (replace with MongoDB in production)
const users = new Map();
const rooms = new Map();
const messages = new Map();
const sessions = new Map();

// JWT Secret
const JWT_SECRET = process.env.JWT_SECRET || 'your-jwt-secret-key';

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};

// API Routes

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    activeConnections: io.engine.clientsCount,
    activeRooms: rooms.size
  });
});

// User registration
app.post('/api/auth/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Check if user already exists
    if (users.has(email)) {
      return res.status(409).json({ error: 'User already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create user
    const user = {
      id: uuidv4(),
      username,
      email,
      password: hashedPassword,
      createdAt: new Date(),
      isOnline: false
    };

    users.set(email, user);

    // Create JWT token
    const token = jwt.sign({ userId: user.id, email: user.email }, JWT_SECRET, { expiresIn: '24h' });

    res.status(201).json({
      message: 'User registered successfully',
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email
      }
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// User login
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Missing email or password' });
    }

    // Find user
    const user = users.get(email);
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Check password
    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Create JWT token
    const token = jwt.sign({ userId: user.id, email: user.email }, JWT_SECRET, { expiresIn: '24h' });

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get user profile
app.get('/api/users/profile', authenticateToken, (req, res) => {
  const user = users.get(req.user.email);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  res.json({
    id: user.id,
    username: user.username,
    email: user.email,
    isOnline: user.isOnline,
    createdAt: user.createdAt
  });
});

// Create collaboration room
app.post('/api/rooms', authenticateToken, (req, res) => {
  try {
    const { name, description, isPrivate = false } = req.body;
    const userId = req.user.userId;

    if (!name) {
      return res.status(400).json({ error: 'Room name is required' });
    }

    const room = {
      id: uuidv4(),
      name,
      description: description || '',
      isPrivate,
      createdBy: userId,
      createdAt: new Date(),
      participants: [userId],
      messages: []
    };

    rooms.set(room.id, room);
    messages.set(room.id, []);

    res.status(201).json({
      message: 'Room created successfully',
      room: {
        id: room.id,
        name: room.name,
        description: room.description,
        isPrivate: room.isPrivate,
        createdAt: room.createdAt
      }
    });
  } catch (error) {
    console.error('Create room error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get all rooms
app.get('/api/rooms', authenticateToken, (req, res) => {
  try {
    const userId = req.user.userId;
    const userRooms = [];

    for (const [roomId, room] of rooms) {
      if (!room.isPrivate || room.participants.includes(userId)) {
        userRooms.push({
          id: room.id,
          name: room.name,
          description: room.description,
          isPrivate: room.isPrivate,
          participantCount: room.participants.length,
          createdAt: room.createdAt
        });
      }
    }

    res.json({ rooms: userRooms });
  } catch (error) {
    console.error('Get rooms error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get room messages
app.get('/api/rooms/:roomId/messages', authenticateToken, (req, res) => {
  try {
    const { roomId } = req.params;
    const userId = req.user.userId;

    const room = rooms.get(roomId);
    if (!room) {
      return res.status(404).json({ error: 'Room not found' });
    }

    if (room.isPrivate && !room.participants.includes(userId)) {
      return res.status(403).json({ error: 'Access denied' });
    }

    const roomMessages = messages.get(roomId) || [];
    res.json({ messages: roomMessages });
  } catch (error) {
    console.error('Get messages error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get online users
app.get('/api/users/online', authenticateToken, (req, res) => {
  try {
    const onlineUsers = [];
    for (const [email, user] of users) {
      if (user.isOnline) {
        onlineUsers.push({
          id: user.id,
          username: user.username,
          email: user.email
        });
      }
    }
    res.json({ users: onlineUsers });
  } catch (error) {
    console.error('Get online users error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// WebSocket Connection Handling
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.id}`);

  // Join room
  socket.on('join_room', (data) => {
    const { roomId, token } = data;
    
    try {
      // Verify token
      const decoded = jwt.verify(token, JWT_SECRET);
      const user = users.get(decoded.email);
      
      if (!user) {
        socket.emit('error', { message: 'User not found' });
        return;
      }

      const room = rooms.get(roomId);
      if (!room) {
        socket.emit('error', { message: 'Room not found' });
        return;
      }

      // Join room
      socket.join(roomId);
      socket.roomId = roomId;
      socket.userId = user.id;
      socket.username = user.username;

      // Add user to room participants if not already there
      if (!room.participants.includes(user.id)) {
        room.participants.push(user.id);
      }

      // Mark user as online
      user.isOnline = true;
      sessions.set(user.id, socket.id);

      // Notify others in room
      socket.to(roomId).emit('user_joined', {
        userId: user.id,
        username: user.username,
        timestamp: new Date().toISOString()
      });

      // Send room info to user
      socket.emit('room_joined', {
        roomId,
        roomName: room.name,
        participants: room.participants.length,
        messages: messages.get(roomId) || []
      });

      console.log(`${user.username} joined room: ${room.name}`);
    } catch (error) {
      console.error('Join room error:', error);
      socket.emit('error', { message: 'Authentication failed' });
    }
  });

  // Send message
  socket.on('send_message', (data) => {
    const { message, type = 'text' } = data;
    
    if (!socket.roomId || !socket.userId) {
      socket.emit('error', { message: 'Not in a room' });
      return;
    }

    const room = rooms.get(socket.roomId);
    if (!room) {
      socket.emit('error', { message: 'Room not found' });
      return;
    }

    const messageData = {
      id: uuidv4(),
      userId: socket.userId,
      username: socket.username,
      message,
      type,
      timestamp: new Date().toISOString()
    };

    // Store message
    const roomMessages = messages.get(socket.roomId) || [];
    roomMessages.push(messageData);
    messages.set(socket.roomId, roomMessages);

    // Broadcast to room
    io.to(socket.roomId).emit('new_message', messageData);

    console.log(`Message in ${room.name}: ${socket.username}: ${message}`);
  });

  // Typing indicator
  socket.on('typing', (data) => {
    const { isTyping } = data;
    
    if (socket.roomId) {
      socket.to(socket.roomId).emit('user_typing', {
        userId: socket.userId,
        username: socket.username,
        isTyping
      });
    }
  });

  // Code collaboration
  socket.on('code_change', (data) => {
    const { code, language, cursor } = data;
    
    if (socket.roomId) {
      socket.to(socket.roomId).emit('code_updated', {
        userId: socket.userId,
        username: socket.username,
        code,
        language,
        cursor,
        timestamp: new Date().toISOString()
      });
    }
  });

  // Leave room
  socket.on('leave_room', () => {
    if (socket.roomId) {
      socket.to(socket.roomId).emit('user_left', {
        userId: socket.userId,
        username: socket.username,
        timestamp: new Date().toISOString()
      });
      
      socket.leave(socket.roomId);
      console.log(`${socket.username} left room: ${socket.roomId}`);
    }
  });

  // Disconnect
  socket.on('disconnect', () => {
    console.log(`User disconnected: ${socket.id}`);
    
    if (socket.userId) {
      const user = Array.from(users.values()).find(u => u.id === socket.userId);
      if (user) {
        user.isOnline = false;
      }
      
      sessions.delete(socket.userId);
      
      if (socket.roomId) {
        socket.to(socket.roomId).emit('user_disconnected', {
          userId: socket.userId,
          username: socket.username,
          timestamp: new Date().toISOString()
        });
      }
    }
  });
});

// Create default room and admin user on startup
const initializeData = () => {
  // Create admin user
  const adminUser = {
    id: uuidv4(),
    username: 'admin',
    email: 'admin@collaboration.com',
    password: bcrypt.hashSync('admin123', 10),
    createdAt: new Date(),
    isOnline: false
  };
  users.set(adminUser.email, adminUser);

  // Create default room
  const defaultRoom = {
    id: uuidv4(),
    name: 'General Discussion',
    description: 'Welcome to the real-time collaboration platform!',
    isPrivate: false,
    createdBy: adminUser.id,
    createdAt: new Date(),
    participants: [adminUser.id],
    messages: []
  };
  rooms.set(defaultRoom.id, defaultRoom);
  messages.set(defaultRoom.id, []);

  console.log('✅ Default data initialized:');
  console.log(`   Admin user: admin@collaboration.com / admin123`);
  console.log(`   Default room: ${defaultRoom.name}`);
};

// Start server
const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
  initializeData();
  console.log(`🚀 Real-time Collaboration Platform running on port ${PORT}`);
  console.log(`📡 WebSocket server ready for connections`);
  console.log(`🌐 Health check: http://localhost:${PORT}/api/health`);
}); 