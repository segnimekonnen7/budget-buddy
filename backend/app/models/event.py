"""Event model for event sourcing."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


class Event(Base):
    """Event model for event sourcing pattern."""
    
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    habit_id = Column(UUID(as_uuid=True), ForeignKey("habits.id"), nullable=False, index=True)
    type = Column(String, nullable=False)  # 'checkin', 'miss', 'reminder_sent', etc.
    ts = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    payload = Column(JSONB, nullable=True)
    
    # Relationships
    user = relationship("User", backref="events")
    habit = relationship("Habit", backref="events")