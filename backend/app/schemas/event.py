"""Event schemas."""

from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel
import uuid


class EventCreate(BaseModel):
    """Schema for creating an event."""
    ts: Optional[datetime] = None
    payload: Optional[Dict[str, Any]] = None


class Event(BaseModel):
    """Schema for event."""
    id: uuid.UUID
    user_id: uuid.UUID
    habit_id: uuid.UUID
    type: str
    ts: datetime
    payload: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True