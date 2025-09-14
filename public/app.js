// Real-time Collaboration Platform Frontend
let socket;
let currentUser = null;
let currentRoom = null;
let typingTimeout;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token) {
        currentUser = JSON.parse(localStorage.getItem('user'));
        showApp();
        initializeSocket();
        loadRooms();
        loadOnlineUsers();
    }
});

// Authentication Functions
async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        alert('Please enter both email and password');
        return;
    }

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data.user;
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            showApp();
            initializeSocket();
            loadRooms();
            loadOnlineUsers();
        } else {
            alert(data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
}

async function register() {
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    if (!username || !email || !password) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Registration successful! Please login.');
            showLogin();
        } else {
            alert(data.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    }
}

function showLogin() {
    document.getElementById('authSection').innerHTML = `
        <div class="auth-form">
            <h2 class="text-center text-white mb-4">
                <i class="fas fa-users"></i> Real-time Collaboration Platform
            </h2>
            
            <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" id="loginEmail" placeholder="Enter your email">
            </div>
            
            <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" id="loginPassword" placeholder="Enter your password">
            </div>
            
            <button class="btn btn-primary w-100 mb-3" onclick="login()">
                <i class="fas fa-sign-in-alt"></i> Login
            </button>
            
            <div class="text-center">
                <small class="text-white-50">Don't have an account? 
                    <a href="#" onclick="showRegister()" class="text-white">Register</a>
                </small>
            </div>
            
            <div class="text-center mt-3">
                <small class="text-white-50">
                    Demo: admin@collaboration.com / admin123
                </small>
            </div>
        </div>
    `;
}

function showRegister() {
    document.getElementById('authSection').innerHTML = `
        <div class="auth-form">
            <h2 class="text-center text-white mb-4">
                <i class="fas fa-user-plus"></i> Create Account
            </h2>
            
            <div class="mb-3">
                <label class="form-label">Username</label>
                <input type="text" class="form-control" id="registerUsername" placeholder="Enter your username">
            </div>
            
            <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" id="registerEmail" placeholder="Enter your email">
            </div>
            
            <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" id="registerPassword" placeholder="Enter your password">
            </div>
            
            <button class="btn btn-primary w-100 mb-3" onclick="register()">
                <i class="fas fa-user-plus"></i> Register
            </button>
            
            <div class="text-center">
                <small class="text-white-50">Already have an account? 
                    <a href="#" onclick="showLogin()" class="text-white">Login</a>
                </small>
            </div>
        </div>
    `;
}

function showApp() {
    document.getElementById('authSection').classList.add('d-none');
    document.getElementById('appSection').classList.remove('d-none');
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    currentUser = null;
    currentRoom = null;
    
    if (socket) {
        socket.disconnect();
    }
    
    document.getElementById('appSection').classList.add('d-none');
    document.getElementById('authSection').classList.remove('d-none');
    showLogin();
}

// WebSocket Functions
function initializeSocket() {
    const token = localStorage.getItem('token');
    socket = io();

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('room_joined', (data) => {
        console.log('Joined room:', data);
        currentRoom = data.roomId;
        document.getElementById('currentRoomName').textContent = data.roomName;
        
        // Display existing messages
        displayMessages(data.messages);
    });

    socket.on('new_message', (message) => {
        addMessage(message);
    });

    socket.on('user_joined', (data) => {
        addSystemMessage(`${data.username} joined the room`);
        loadOnlineUsers();
    });

    socket.on('user_left', (data) => {
        addSystemMessage(`${data.username} left the room`);
        loadOnlineUsers();
    });

    socket.on('user_typing', (data) => {
        if (data.isTyping) {
            document.getElementById('typingIndicator').textContent = `${data.username} is typing...`;
            document.getElementById('typingIndicator').style.display = 'block';
        } else {
            document.getElementById('typingIndicator').style.display = 'none';
        }
    });

    socket.on('code_updated', (data) => {
        if (data.userId !== currentUser.id) {
            document.getElementById('codeEditor').value = data.code;
        }
    });

    socket.on('error', (data) => {
        alert('Error: ' + data.message);
    });
}

// Room Functions
async function loadRooms() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/rooms', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();
        displayRooms(data.rooms);
    } catch (error) {
        console.error('Error loading rooms:', error);
    }
}

function displayRooms(rooms) {
    const roomList = document.getElementById('roomList');
    roomList.innerHTML = '';

    rooms.forEach(room => {
        const roomElement = document.createElement('div');
        roomElement.className = 'room-item';
        roomElement.onclick = () => joinRoom(room.id);
        roomElement.innerHTML = `
            <h6 class="text-white mb-1">${room.name}</h6>
            <small class="text-white-50">${room.description}</small>
            <div class="mt-2">
                <span class="badge bg-primary">${room.participantCount} participants</span>
                ${room.isPrivate ? '<span class="badge bg-warning ms-1">Private</span>' : ''}
            </div>
        `;
        roomList.appendChild(roomElement);
    });
}

function joinRoom(roomId) {
    if (currentRoom) {
        socket.emit('leave_room');
    }

    const token = localStorage.getItem('token');
    socket.emit('join_room', { roomId, token });

    // Update active room styling
    document.querySelectorAll('.room-item').forEach(item => {
        item.classList.remove('active');
    });
    event.target.closest('.room-item').classList.add('active');
}

async function createRoom() {
    const name = prompt('Enter room name:');
    if (!name) return;

    const description = prompt('Enter room description (optional):');
    const isPrivate = confirm('Make this room private?');

    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/rooms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name, description, isPrivate })
        });

        const data = await response.json();

        if (response.ok) {
            loadRooms();
            joinRoom(data.room.id);
        } else {
            alert(data.error || 'Failed to create room');
        }
    } catch (error) {
        console.error('Error creating room:', error);
        alert('Failed to create room');
    }
}

function showCreateRoom() {
    createRoom();
}

// Message Functions
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    if (message && currentRoom) {
        socket.emit('send_message', { message, type: 'text' });
        messageInput.value = '';
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    } else {
        // Typing indicator
        socket.emit('typing', { isTyping: true });
        
        clearTimeout(typingTimeout);
        typingTimeout = setTimeout(() => {
            socket.emit('typing', { isTyping: false });
        }, 1000);
    }
}

function addMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.className = `message ${message.userId === currentUser.id ? 'own' : ''}`;
    
    messageElement.innerHTML = `
        <div class="message-header">
            ${message.username}
            <span class="message-time">${new Date(message.timestamp).toLocaleTimeString()}</span>
        </div>
        <div class="message-content">${message.message}</div>
    `;
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addSystemMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    messageElement.style.borderLeftColor = '#FF9800';
    
    messageElement.innerHTML = `
        <div class="message-content text-center text-white-50">
            <i class="fas fa-info-circle"></i> ${message}
        </div>
    `;
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function displayMessages(messages) {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '';
    
    messages.forEach(message => {
        addMessage(message);
    });
}

// User Functions
async function loadOnlineUsers() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/users/online', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();
        displayOnlineUsers(data.users);
    } catch (error) {
        console.error('Error loading online users:', error);
    }
}

function displayOnlineUsers(users) {
    const userList = document.getElementById('userList');
    userList.innerHTML = '';

    users.forEach(user => {
        const userElement = document.createElement('div');
        userElement.className = 'user-item online';
        userElement.innerHTML = `
            <div class="online-indicator"></div>
            <span class="text-white">${user.username}</span>
        `;
        userList.appendChild(userElement);
    });
}

// Code Editor Functions
function handleCodeChange() {
    if (currentRoom) {
        const code = document.getElementById('codeEditor').value;
        socket.emit('code_change', {
            code,
            language: 'javascript',
            cursor: { line: 0, ch: 0 }
        });
    }
}

// Utility Functions
function formatTime(timestamp) {
    return new Date(timestamp).toLocaleTimeString();
}

// Auto-login with demo credentials
function autoLogin() {
    document.getElementById('loginEmail').value = 'admin@collaboration.com';
    document.getElementById('loginPassword').value = 'admin123';
    login();
} 