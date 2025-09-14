"""Smart reminder service for analyzing optimal reminder times."""

import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, Dict, Any

from app.models.habit_completion import HabitCompletion


class SmartReminderService:
    """Service for analyzing user behavior and suggesting optimal reminder times."""
    
    def __init__(self, db):
        self.db = db
    
    def analyze_optimal_reminder_time(self, user_id: str, habit_id: str) -> Optional[Dict[str, Any]]:
        """Analyze when user typically completes habits to suggest best reminder time."""
        
        # Get completion data (pure software engineering)
        completions = self.db.query(HabitCompletion).filter(
            HabitCompletion.user_id == user_id,
            HabitCompletion.habit_id == habit_id,
            HabitCompletion.completed_at.isnot(None)
        ).all()
        
        if len(completions) < 3:
            return None  # Not enough data
        
        # Simple pattern analysis (no external APIs)
        completion_hours = [c.completed_at.hour for c in completions]
        success_by_hour = defaultdict(int)
        
        for hour in completion_hours:
            success_by_hour[hour] += 1
        
        # Find peak completion time
        best_hour = max(success_by_hour.items(), key=lambda x: x[1])[0]
        
        return {
            "suggested_reminder_hour": max(6, best_hour - 1),  # Remind 1 hour before peak
            "confidence": len(completions),
            "pattern": dict(success_by_hour)
        }
    
    def get_completion_stats(self, user_id: str, habit_id: str, days: int = 30) -> Dict[str, Any]:
        """Get completion statistics for a habit."""
        
        since_date = datetime.utcnow() - timedelta(days=days)
        completions = self.db.query(HabitCompletion).filter(
            HabitCompletion.user_id == user_id,
            HabitCompletion.habit_id == habit_id,
            HabitCompletion.completed_at >= since_date
        ).all()
        
        if not completions:
            return {
                "total_completions": 0,
                "completion_rate": 0.0,
                "average_daily": 0.0,
                "best_hour": None
            }
        
        # Calculate statistics
        total_completions = len(completions)
        completion_rate = total_completions / days
        
        # Find most common completion hour
        hour_counts = defaultdict(int)
        for completion in completions:
            hour_counts[completion.completed_at.hour] += 1
        
        best_hour = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else None
        
        return {
            "total_completions": total_completions,
            "completion_rate": round(completion_rate, 2),
            "average_daily": round(total_completions / days, 2),
            "best_hour": best_hour,
            "hour_distribution": dict(hour_counts)
        }
