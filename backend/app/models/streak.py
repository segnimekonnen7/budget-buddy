"""Streak model."""

import uuid
from datetime import datetime, date
from sqlalchemy import Column, Date, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class Streak(Base):
    """Streak model."""
    
    __tablename__ = "streaks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    habit_id = Column(UUID(as_uuid=True), ForeignKey("habits.id"), nullable=False, unique=True)
    start_date = Column(Date, nullable=False)
    length_days = Column(Integer, nullable=False)
    grace_used = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
