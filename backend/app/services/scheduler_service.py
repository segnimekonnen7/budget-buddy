"""Scheduler service for habit reminders."""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class SchedulerService:
    """Service for scheduling habit reminders."""
    
    def __init__(self):
        self.scheduler_interval_minutes = 15
    
    def should_send_reminder(self, habit: Dict[str, Any]) -> bool:
        """Check if a reminder should be sent for a habit."""
        # Simple logic: send reminder if habit is due today and not completed
        return habit.get('is_due_today', False) and not habit.get('completed_today', False)


class SmartReminderService:
    """Service for analyzing optimal reminder times using statistical analysis."""
    
    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon
        self.completion_history = defaultdict(list)
    
    def analyze_completion_patterns(self, habit_id: str, completions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze completion patterns to find optimal reminder times.
        Uses statistical analysis without external libraries.
        """
        if not completions:
            return {
                "best_hour": 9,  # Default to 9 AM
                "confidence": 0.0,
                "total_completions": 0,
                "analysis": "No completion data available"
            }
        
        # Extract completion hours
        completion_hours = []
        for completion in completions:
            try:
                completion_time = datetime.fromisoformat(completion['completed_at'].replace('Z', '+00:00'))
                completion_hours.append(completion_time.hour)
            except (ValueError, KeyError):
                continue
        
        if not completion_hours:
            return {
                "best_hour": 9,
                "confidence": 0.0,
                "total_completions": 0,
                "analysis": "No valid completion times found"
            }
        
        # Calculate hour distribution
        hour_counts = defaultdict(int)
        for hour in completion_hours:
            hour_counts[hour] += 1
        
        # Find the most common completion hour
        best_hour = max(hour_counts.items(), key=lambda x: x[1])[0]
        total_completions = len(completion_hours)
        
        # Calculate confidence based on consistency
        max_count = max(hour_counts.values())
        confidence = max_count / total_completions if total_completions > 0 else 0.0
        
        # Calculate average completion time
        avg_hour = sum(completion_hours) / len(completion_hours)
        
        return {
            "best_hour": best_hour,
            "confidence": round(confidence, 3),
            "total_completions": total_completions,
            "average_hour": round(avg_hour, 1),
            "hour_distribution": dict(hour_counts),
            "analysis": f"Based on {total_completions} completions, optimal time is {best_hour}:00 with {confidence*100:.1f}% consistency"
        }
    
    def get_optimal_reminder_time(self, habit_id: str, completions: List[Dict[str, Any]]) -> int:
        """
        Get the optimal reminder hour for a habit.
        Returns the best hour (0-23) based on historical completion data.
        """
        analysis = self.analyze_completion_patterns(habit_id, completions)
        return analysis["best_hour"]
    
    def should_explore_new_time(self) -> bool:
        """
        Epsilon-greedy strategy: occasionally try new times to explore.
        """
        import random
        return random.random() < self.epsilon
