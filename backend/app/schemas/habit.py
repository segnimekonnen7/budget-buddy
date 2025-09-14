"""Habit schemas."""

from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel
import uuid


class HabitCreate(BaseModel):
    """Schema for creating a habit."""
    title: str
    notes: Optional[str] = None
    schedule_json: Dict[str, Any]
    goal_type: str
    target_value: Optional[float] = None
    grace_per_week: int = 1
    timezone: str = "UTC"


class HabitUpdate(BaseModel):
    """Schema for updating a habit."""
    title: Optional[str] = None
    notes: Optional[str] = None
    schedule_json: Optional[Dict[str, Any]] = None
    goal_type: Optional[str] = None
    target_value: Optional[float] = None
    grace_per_week: Optional[int] = None
    timezone: Optional[str] = None


class HabitSummary(BaseModel):
    """Schema for habit summary."""
    id: uuid.UUID
    title: str
    notes: Optional[str] = None
    goal_type: str
    target_value: Optional[float] = None
    grace_per_week: int
    timezone: str
    created_at: datetime
    current_streak_length: int
    is_due_today: bool
    best_hour: Optional[int] = None


class Habit(BaseModel):
    """Schema for habit."""
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    notes: Optional[str] = None
    schedule_json: Dict[str, Any]
    goal_type: str
    target_value: Optional[float] = None
    grace_per_week: int
    timezone: str
    created_at: datetime
    
    class Config:
        from_attributes = True