"""User schemas."""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    """Base user schema."""
    email: str


class UserCreate(UserBase):
    """User creation schema."""
    pass


class User(UserBase):
    """User schema."""
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
