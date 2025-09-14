"""Habits router."""

import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.habit import Habit
from app.models.event import Event
from app.schemas.habit import HabitCreate, HabitUpdate, HabitSummary
from app.schemas.event import EventCreate
from app.routers.auth import get_current_user
from app.services.streak_service import StreakService

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("/", response_model=Habit)
async def create_habit(
    habit_data: HabitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new habit."""
    habit = Habit(
        user_id=current_user.id,
        title=habit_data.title,
        notes=habit_data.notes,
        schedule_json=habit_data.schedule_json,
        goal_type=habit_data.goal_type,
        target_value=habit_data.target_value,
        grace_per_week=habit_data.grace_per_week,
        timezone=habit_data.timezone
    )
    
    db.add(habit)
    db.commit()
    db.refresh(habit)
    
    return habit


@router.get("/", response_model=List[HabitSummary])
async def list_habits(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's habits with summaries."""
    habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()
    
    streak_service = StreakService(db)
    habit_summaries = []
    
    for habit in habits:
        # Get streak summary
        streak_summary = streak_service.get_streak_summary(habit)
        
        # Get best hour from reminder
        best_hour = None
        if habit.reminder:
            best_hour = habit.reminder.best_hour
        
        habit_summary = HabitSummary(
            id=habit.id,
            title=habit.title,
            notes=habit.notes,
            goal_type=habit.goal_type,
            target_value=habit.target_value,
            grace_per_week=habit.grace_per_week,
            timezone=habit.timezone,
            created_at=habit.created_at,
            current_streak_length=streak_summary["current_streak_length"],
            is_due_today=streak_summary["is_due_today"],
            best_hour=best_hour
        )
        habit_summaries.append(habit_summary)
    
    return habit_summaries


@router.get("/{habit_id}", response_model=Habit)
async def get_habit(
    habit_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get habit details."""
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    return habit


@router.patch("/{habit_id}", response_model=Habit)
async def update_habit(
    habit_id: uuid.UUID,
    habit_data: HabitUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a habit."""
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Update fields
    for field, value in habit_data.dict(exclude_unset=True).items():
        setattr(habit, field, value)
    
    db.commit()
    db.refresh(habit)
    
    return habit


@router.delete("/{habit_id}")
async def delete_habit(
    habit_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a habit."""
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    db.delete(habit)
    db.commit()
    
    return {"message": "Habit deleted"}


@router.post("/{habit_id}/checkin")
async def checkin_habit(
    habit_id: uuid.UUID,
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record a habit checkin."""
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Create checkin event
    event = Event(
        user_id=current_user.id,
        habit_id=habit_id,
        type="checkin",
        ts=event_data.ts or datetime.utcnow(),
        payload=event_data.payload
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    # Update streak
    streak_service = StreakService(db)
    streak_service.update_streak(habit)
    
    return {"message": "Checkin recorded", "event_id": event.id}


@router.post("/{habit_id}/miss")
async def miss_habit(
    habit_id: uuid.UUID,
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record a habit miss."""
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Create miss event
    event = Event(
        user_id=current_user.id,
        habit_id=habit_id,
        type="miss",
        ts=event_data.ts or datetime.utcnow(),
        payload=event_data.payload
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    # Update streak
    streak_service = StreakService(db)
    streak_service.update_streak(habit)
    
    return {"message": "Miss recorded", "event_id": event.id}


@router.get("/{habit_id}/events")
async def get_habit_events(
    habit_id: uuid.UUID,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get events for a habit."""
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Build query
    query = db.query(Event).filter(Event.habit_id == habit_id)
    
    if from_date:
        query = query.filter(Event.ts >= from_date)
    if to_date:
        query = query.filter(Event.ts <= to_date)
    
    events = query.order_by(Event.ts.desc()).all()
    
    return events
