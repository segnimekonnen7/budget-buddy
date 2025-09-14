"""Digest run model."""

import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class DigestRun(Base):
    """Digest run model."""
    
    __tablename__ = "digest_runs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ran_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    count_sent = Column(Integer, nullable=False, default=0)
