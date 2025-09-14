"""Reminder schemas."""

import uuid
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class ReminderBase(BaseModel):
    """Base reminder schema."""
    channel: str = Field(..., pattern="^email$")
    window: Dict[str, Any]
    quiet_hours: Optional[Dict[str, Any]] = None
    timezone: str


class ReminderCreate(ReminderBase):
    """Reminder creation schema."""
    pass


class Reminder(ReminderBase):
    """Reminder schema."""
    id: uuid.UUID
    habit_id: uuid.UUID
    best_hour: Optional[int] = None
    
    class Config:
        from_attributes = True
