"""Habit completion model."""

import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Boolean, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class HabitCompletion(Base):
    """Habit completion model for tracking when habits are completed."""
    
    __tablename__ = "habit_completions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    habit_id = Column(UUID(as_uuid=True), ForeignKey("habits.id"), nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    value = Column(Numeric, nullable=True)  # For count/duration goals
    notes = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", backref="habit_completions")
    habit = relationship("Habit", backref="completions")
