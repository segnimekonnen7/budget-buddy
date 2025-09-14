"""Reminder model."""

import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.session import Base


class Reminder(Base):
    """Reminder model."""
    
    __tablename__ = "reminders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    habit_id = Column(UUID(as_uuid=True), ForeignKey("habits.id"), nullable=False, unique=True)
    channel = Column(String, nullable=False)
    window = Column(JSONB, nullable=False)
    quiet_hours = Column(JSONB)
    best_hour = Column(Integer)
    timezone = Column(String, nullable=False)
    
    __table_args__ = (
        CheckConstraint("channel IN ('email')", name="check_channel"),
    )
