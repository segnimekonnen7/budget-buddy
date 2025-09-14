"""Habit model."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Numeric, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


class Habit(Base):
    """Habit model."""
    
    __tablename__ = "habits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    notes = Column(Text)
    schedule_json = Column(JSONB, nullable=False)
    goal_type = Column(String, nullable=False)
    target_value = Column(Numeric)
    grace_per_week = Column(Integer, nullable=False, default=1)
    timezone = Column(String, nullable=False, default="UTC")
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="habits")
    completions = relationship("HabitCompletion", backref="habit")
    
    __table_args__ = (
        CheckConstraint("goal_type IN ('check', 'count', 'duration')", name="check_goal_type"),
    )