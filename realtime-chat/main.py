"""
Real-Time Chat Application Backend
FastAPI + WebSockets + SQLAlchemy + PostgreSQL

Features:
- Real-time messaging with WebSockets
- User authentication and rooms
- Message persistence
- Online user tracking
- Message history
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import jwt
import bcrypt
from datetime import datetime, timedelta
import uuid
import asyncio
import os

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./chat.db"  # Using SQLite for demo
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "demo-secret-key-for-github-showcase")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI app
app = FastAPI(title="Real-Time Chat API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    messages = relationship("Message", back_populates="sender")
    room_memberships = relationship("RoomMember", back_populates="user")

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    messages = relationship("Message", back_populates="room")
    members = relationship("RoomMember", back_populates="room")

class RoomMember(Base):
    __tablename__ = "room_members"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    joined_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="room_memberships")
    room = relationship("Room", back_populates="members")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    message_type = Column(String(20), default="text")  # text, image, file, system
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_edited = Column(Boolean, default=False)
    
    sender = relationship("User", back_populates="messages")
    room = relationship("Room", back_populates="messages")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_online: bool
    last_seen: datetime
    
    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_private: bool = False

class RoomResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_private: bool
    created_at: datetime
    member_count: int
    
    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    content: str
    room_id: int
    message_type: str = "text"

class MessageResponse(BaseModel):
    id: int
    content: str
    sender_id: int
    sender_username: str
    room_id: int
    message_type: str
    timestamp: datetime
    is_edited: bool
    
    class Config:
        from_attributes = True

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        # Store connections by room_id
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # Store user info for each connection
        self.connection_users: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, room_id: int, user_info: dict):
        await websocket.accept()
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        
        self.active_connections[room_id].append(websocket)
        self.connection_users[websocket] = user_info
        
        # Notify room about new user
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user": user_info["username"],
            "message": f"{user_info['username']} joined the room",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def disconnect(self, websocket: WebSocket, room_id: int):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
        
        user_info = self.connection_users.pop(websocket, None)
        
        # Notify room about user leaving
        if user_info:
            asyncio.create_task(self.broadcast_to_room(room_id, {
                "type": "user_left",
                "user": user_info["username"],
                "message": f"{user_info['username']} left the room",
                "timestamp": datetime.utcnow().isoformat()
            }))
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))
    
    async def broadcast_to_room(self, room_id: int, message: dict):
        if room_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    disconnected.append(connection)
            
            # Clean up disconnected connections
            for conn in disconnected:
                self.active_connections[room_id].remove(conn)

manager = ConnectionManager()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication functions
security = HTTPBearer()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(db: Session = Depends(get_db), username: str = Depends(verify_token)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# API Endpoints
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create new user
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update online status
    db_user.is_online = True
    db_user.last_seen = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "user": UserResponse.from_orm(db_user)}

@app.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.is_online = False
    current_user.last_seen = datetime.utcnow()
    db.commit()
    return {"message": "Logged out successfully"}

@app.get("/rooms", response_model=List[RoomResponse])
def get_rooms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    room_responses = []
    for room in rooms:
        member_count = db.query(RoomMember).filter(RoomMember.room_id == room.id).count()
        room_response = RoomResponse(
            id=room.id,
            name=room.name,
            description=room.description,
            is_private=room.is_private,
            created_at=room.created_at,
            member_count=member_count
        )
        room_responses.append(room_response)
    return room_responses

@app.post("/rooms", response_model=RoomResponse)
def create_room(room: RoomCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_room = Room(
        name=room.name,
        description=room.description,
        is_private=room.is_private,
        created_by=current_user.id
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    
    # Add creator as admin member
    membership = RoomMember(
        user_id=current_user.id,
        room_id=db_room.id,
        is_admin=True
    )
    db.add(membership)
    db.commit()
    
    return RoomResponse(
        id=db_room.id,
        name=db_room.name,
        description=db_room.description,
        is_private=db_room.is_private,
        created_at=db_room.created_at,
        member_count=1
    )

@app.post("/rooms/{room_id}/join")
def join_room(room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if room exists
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Check if already a member
    existing_membership = db.query(RoomMember).filter(
        RoomMember.user_id == current_user.id,
        RoomMember.room_id == room_id
    ).first()
    if existing_membership:
        raise HTTPException(status_code=400, detail="Already a member of this room")
    
    # Add membership
    membership = RoomMember(user_id=current_user.id, room_id=room_id)
    db.add(membership)
    db.commit()
    
    return {"message": "Joined room successfully"}

@app.get("/rooms/{room_id}/messages", response_model=List[MessageResponse])
def get_room_messages(
    room_id: int, 
    limit: int = 50,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Check if user is member of room
    membership = db.query(RoomMember).filter(
        RoomMember.user_id == current_user.id,
        RoomMember.room_id == room_id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this room")
    
    messages = db.query(Message).filter(Message.room_id == room_id)\
                 .order_by(Message.timestamp.desc())\
                 .limit(limit)\
                 .all()
    
    message_responses = []
    for message in reversed(messages):  # Reverse to show oldest first
        message_response = MessageResponse(
            id=message.id,
            content=message.content,
            sender_id=message.sender_id,
            sender_username=message.sender.username,
            room_id=message.room_id,
            message_type=message.message_type,
            timestamp=message.timestamp,
            is_edited=message.is_edited
        )
        message_responses.append(message_response)
    
    return message_responses

@app.get("/users/online", response_model=List[UserResponse])
def get_online_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).filter(User.is_online == True).all()
    return users

# WebSocket endpoint
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, token: str):
    try:
        # Verify token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            await websocket.close(code=4001)
            return
        
        # Get user from database
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        if not user:
            await websocket.close(code=4001)
            return
        
        # Check if user is member of room
        membership = db.query(RoomMember).filter(
            RoomMember.user_id == user.id,
            RoomMember.room_id == room_id
        ).first()
        if not membership:
            await websocket.close(code=4003)
            return
        
        # Connect to WebSocket
        user_info = {"id": user.id, "username": user.username}
        await manager.connect(websocket, room_id, user_info)
        
        try:
            while True:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                if message_data["type"] == "message":
                    # Save message to database
                    db_message = Message(
                        content=message_data["content"],
                        sender_id=user.id,
                        room_id=room_id,
                        message_type=message_data.get("message_type", "text")
                    )
                    db.add(db_message)
                    db.commit()
                    db.refresh(db_message)
                    
                    # Broadcast message to room
                    broadcast_data = {
                        "type": "message",
                        "id": db_message.id,
                        "content": db_message.content,
                        "sender_id": user.id,
                        "sender_username": user.username,
                        "room_id": room_id,
                        "message_type": db_message.message_type,
                        "timestamp": db_message.timestamp.isoformat(),
                        "is_edited": False
                    }
                    await manager.broadcast_to_room(room_id, broadcast_data)
                
                elif message_data["type"] == "typing":
                    # Broadcast typing indicator
                    typing_data = {
                        "type": "typing",
                        "user": user.username,
                        "is_typing": message_data["is_typing"]
                    }
                    await manager.broadcast_to_room(room_id, typing_data)
        
        except WebSocketDisconnect:
            manager.disconnect(websocket, room_id)
        
        finally:
            db.close()
    
    except Exception as e:
        await websocket.close(code=4000)

@app.get("/")
def root():
    return {
        "message": "Real-Time Chat API",
        "version": "1.0.0",
        "features": [
            "Real-time messaging",
            "User authentication",
            "Room management",
            "Message persistence",
            "Online user tracking",
            "Typing indicators"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Real-Time Chat API...")
    print("📡 WebSocket support enabled")
    print("🔐 JWT authentication enabled")
    print("💾 Database: SQLite (chat.db)")
    print("🌐 CORS: Enabled for all origins")
    uvicorn.run(app, host="0.0.0.0", port=8001)
