"""Authentication router."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


def get_current_user(
    token: str = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    # For now, return a mock user for development
    # In production, you'd validate the JWT token here
    user = db.query(User).first()
    if not user:
        # Create a mock user for development
        user = User(
            email="demo@example.com",
            name="Demo User"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user