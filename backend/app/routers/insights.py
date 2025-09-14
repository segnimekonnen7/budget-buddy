"""Insights router with ML-like features."""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.habit import Habit
from app.routers.auth import get_current_user
from app.services.prediction_service import PredictionService
from app.services.smart_reminder_service import SmartReminderService

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/habits/{habit_id}/success-prediction")
async def predict_habit_success(
    habit_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict likelihood of maintaining habit streak."""
    
    # Verify habit belongs to user
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Get prediction
    prediction_service = PredictionService(db)
    result = prediction_service.predict_habit_success(str(habit_id))
    
    return result


@router.get("/habits/{habit_id}/optimal-reminder")
async def get_optimal_reminder_time(
    habit_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get optimal reminder time based on completion patterns."""
    
    # Verify habit belongs to user
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Get optimal reminder time
    reminder_service = SmartReminderService(db)
    result = reminder_service.analyze_optimal_reminder_time(
        str(current_user.id), 
        str(habit_id)
    )
    
    if not result:
        return {"message": "Not enough data for analysis. Complete the habit a few more times."}
    
    return result


@router.get("/habits/{habit_id}/completion-stats")
async def get_completion_stats(
    habit_id: uuid.UUID,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get completion statistics for a habit."""
    
    # Verify habit belongs to user
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Get completion stats
    reminder_service = SmartReminderService(db)
    result = reminder_service.get_completion_stats(
        str(current_user.id), 
        str(habit_id), 
        days
    )
    
    return result