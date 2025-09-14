"""Contextual bandit service for reminder timing."""

import logging
import random
from datetime import datetime, time
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.reminder import Reminder
from app.models.event import Event
from app.core.config import settings

logger = logging.getLogger(__name__)


class BanditService:
    """Contextual bandit service for optimizing reminder timing."""
    
    def __init__(self, db: Session):
        self.db = db
        self.epsilon = settings.bandit_epsilon
    
    def get_candidate_hours(self, reminder: Reminder) -> List[int]:
        """Get candidate hours for reminder within the window."""
        window = reminder.window
        start_hour = window.get("start_hour", 6)
        end_hour = window.get("end_hour", 21)
        
        # Generate list of hours within the window
        hours = list(range(start_hour, end_hour + 1))
        
        # Filter out quiet hours if specified
        if reminder.quiet_hours:
            quiet_start = reminder.quiet_hours.get("start_hour", 22)
            quiet_end = reminder.quiet_hours.get("end_hour", 6)
            
            if quiet_start <= quiet_end:
                # Quiet hours are within the same day
                hours = [h for h in hours if h < quiet_start or h > quiet_end]
            else:
                # Quiet hours span midnight
                hours = [h for h in hours if h < quiet_start and h > quiet_end]
        
        return hours
    
    def choose_hour(self, habit: Habit, reminder: Reminder) -> int:
        """Choose optimal hour for reminder using ε-greedy bandit."""
        candidate_hours = self.get_candidate_hours(reminder)
        
        if not candidate_hours:
            # Fallback to default
            return reminder.window.get("start_hour", 9)
        
        # Get arm stats for this habit
        arm_stats = self._get_arm_stats(habit.id)
        
        # ε-greedy selection
        if random.random() < self.epsilon:
            # Explore: choose random hour
            chosen_hour = random.choice(candidate_hours)
            logger.info(f"Exploring: chose hour {chosen_hour} for habit {habit.id}")
        else:
            # Exploit: choose best hour based on success rate
            best_hour = self._get_best_hour(arm_stats, candidate_hours)
            chosen_hour = best_hour if best_hour is not None else random.choice(candidate_hours)
            logger.info(f"Exploiting: chose hour {chosen_hour} for habit {habit.id}")
        
        # Update arm stats
        self._update_arm_stats(habit.id, chosen_hour, 0)  # 0 = pull, not reward yet
        
        return chosen_hour
    
    def update_reward(self, habit: Habit, hour: int, reward: int):
        """Update reward for a specific hour."""
        self._update_arm_stats(habit.id, hour, reward)
        
        # Update best_hour if this hour is now the best
        arm_stats = self._get_arm_stats(habit.id)
        best_hour = self._get_best_hour(arm_stats, list(range(24)))
        
        if best_hour is not None:
            reminder = self.db.query(Reminder).filter(Reminder.habit_id == habit.id).first()
            if reminder:
                reminder.best_hour = best_hour
                self.db.commit()
                logger.info(f"Updated best_hour to {best_hour} for habit {habit.id}")
    
    def _get_arm_stats(self, habit_id: str) -> Dict[int, Dict[str, int]]:
        """Get arm statistics for a habit."""
        # In a real implementation, this would be stored in the database
        # For now, we'll use a simple in-memory approach
        # TODO: Implement proper arm stats storage
        return {}
    
    def _update_arm_stats(self, habit_id: str, hour: int, reward: int):
        """Update arm statistics for a habit and hour."""
        # In a real implementation, this would update the database
        # For now, we'll use a simple in-memory approach
        # TODO: Implement proper arm stats storage
        pass
    
    def _get_best_hour(self, arm_stats: Dict[int, Dict[str, int]], candidate_hours: List[int]) -> Optional[int]:
        """Get the best hour based on success rate."""
        best_hour = None
        best_success_rate = -1
        
        for hour in candidate_hours:
            stats = arm_stats.get(hour, {"pulls": 0, "successes": 0})
            pulls = stats.get("pulls", 0)
            successes = stats.get("successes", 0)
            
            if pulls > 0:
                success_rate = successes / pulls
                if success_rate > best_success_rate:
                    best_success_rate = success_rate
                    best_hour = hour
        
        return best_hour
    
    def calculate_completion_rate(self, habit: Habit, days: int = 7) -> float:
        """Calculate completion rate for the last N days."""
        from datetime import timedelta
        
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)
        
        # Count total due days
        total_due = 0
        check_date = start_date
        while check_date <= end_date:
            if self._is_habit_due_on_date(habit, check_date):
                total_due += 1
            check_date += timedelta(days=1)
        
        if total_due == 0:
            return 0.0
        
        # Count completed days
        completed = self.db.query(Event).filter(
            Event.habit_id == habit.id,
            Event.type == "checkin",
            Event.ts >= start_date,
            Event.ts <= end_date
        ).count()
        
        return completed / total_due
    
    def _is_habit_due_on_date(self, habit: Habit, check_date) -> bool:
        """Check if habit is due on a specific date."""
        schedule = habit.schedule_json
        
        if schedule.get("type") == "daily":
            return True
        elif schedule.get("type") == "weekly":
            days = schedule.get("days", [])
            weekday = check_date.weekday() + 1  # Monday = 1, Sunday = 7
            return weekday in days
        elif schedule.get("type") == "times_per_week":
            # For simplicity, assume every other day
            return check_date.day % 2 == 0
        
        return False
