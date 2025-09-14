"""Streak service for calculating habit streaks."""

from typing import Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion


class StreakService:
    """Service for calculating and managing habit streaks."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_streak_summary(self, habit: Habit) -> Dict[str, Any]:
        """Get streak summary for a habit."""
        
        # Get recent completions
        since_date = datetime.utcnow() - timedelta(days=30)
        completions = self.db.query(HabitCompletion).filter(
            HabitCompletion.habit_id == habit.id,
            HabitCompletion.completed_at >= since_date
        ).all()
        
        # Calculate current streak
        current_streak = self.calculate_current_streak(completions)
        
        # Check if due today
        is_due_today = self.is_due_today(habit, completions)
        
        return {
            "current_streak_length": current_streak,
            "is_due_today": is_due_today
        }
    
    def calculate_current_streak(self, completions) -> int:
        """Calculate current streak length."""
        if not completions:
            return 0
        
        # Sort by completion date (most recent first)
        sorted_completions = sorted(completions, key=lambda x: x.completed_at, reverse=True)
        
        streak = 0
        current_date = datetime.utcnow().date()
        
        for completion in sorted_completions:
            completion_date = completion.completed_at.date()
            days_diff = (current_date - completion_date).days
            
            if days_diff == streak:
                streak += 1
                current_date = completion_date
            elif days_diff == streak + 1:
                # Allow for one day gap
                streak += 1
                current_date = completion_date
            else:
                break
        
        return streak
    
    def is_due_today(self, habit: Habit, completions) -> bool:
        """Check if habit is due today."""
        today = datetime.utcnow().date()
        
        # Check if already completed today
        for completion in completions:
            if completion.completed_at.date() == today:
                return False
        
        return True
    
    def update_streak(self, habit: Habit):
        """Update streak for a habit."""
        # This would typically update a streak record
        # For now, we'll just log the update
        pass