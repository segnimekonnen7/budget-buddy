"""Prediction service for habit success forecasting."""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


def get_recent_completions(completions: List[Dict[str, Any]], days: int = 30) -> List[Dict[str, Any]]:
    """Get completions from the last N days."""
    cutoff_date = datetime.now() - timedelta(days=days)
    recent = []
    
    for completion in completions:
        try:
            completion_time = datetime.fromisoformat(completion['completed_at'].replace('Z', '+00:00'))
            if completion_time >= cutoff_date:
                recent.append(completion)
        except (ValueError, KeyError):
            continue
    
    return recent


def calculate_current_streak(completions: List[Dict[str, Any]]) -> int:
    """Calculate the current streak length."""
    if not completions:
        return 0
    
    # Sort completions by date (most recent first)
    sorted_completions = sorted(
        completions, 
        key=lambda x: datetime.fromisoformat(x['completed_at'].replace('Z', '+00:00')),
        reverse=True
    )
    
    streak = 0
    current_date = datetime.now().date()
    
    for completion in sorted_completions:
        try:
            completion_date = datetime.fromisoformat(
                completion['completed_at'].replace('Z', '+00:00')
            ).date()
            
            # Check if this completion is consecutive
            if completion_date == current_date - timedelta(days=streak):
                streak += 1
            else:
                break
        except (ValueError, KeyError):
            continue
    
    return streak


def calculate_consistency(completions: List[Dict[str, Any]], days: int = 30) -> float:
    """Calculate completion consistency over the last N days."""
    if not completions:
        return 0.0
    
    recent_completions = get_recent_completions(completions, days)
    
    # Count unique days with completions
    completion_dates = set()
    for completion in recent_completions:
        try:
            completion_date = datetime.fromisoformat(
                completion['completed_at'].replace('Z', '+00:00')
            ).date()
            completion_dates.add(completion_date)
        except (ValueError, KeyError):
            continue
    
    # Calculate consistency as percentage of days with completions
    consistency = len(completion_dates) / days if days > 0 else 0.0
    return round(consistency, 3)


def generate_recommendation(prediction: str, habit: Dict[str, Any]) -> str:
    """Generate personalized recommendations based on prediction."""
    recommendations = {
        "high": [
            "Keep up the excellent work! Your consistency is impressive.",
            "Consider increasing the challenge slightly to maintain engagement.",
            "Share your success with others to stay motivated."
        ],
        "medium": [
            "You're on the right track! Try setting smaller, more achievable goals.",
            "Consider adjusting your reminder timing to better fit your schedule.",
            "Track your progress more closely to identify patterns."
        ],
        "low": [
            "Start with smaller, more manageable goals to build momentum.",
            "Set up multiple reminders throughout the day.",
            "Find an accountability partner to help you stay on track.",
            "Consider if this habit aligns with your current priorities."
        ]
    }
    
    import random
    return random.choice(recommendations.get(prediction, recommendations["medium"]))


class PredictionService:
    """Service for predicting habit success using statistical analysis."""
    
    def __init__(self):
        self.prediction_history = defaultdict(list)
    
    def predict_success(self, habit_id: str, completions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Predict the likelihood of maintaining the habit streak.
        Uses rule-based logic with statistical analysis.
        """
        if not completions:
            return {
                "prediction": "low",
                "probability": 0.2,
                "confidence": 0.0,
                "current_streak": 0,
                "consistency": 0.0,
                "recommendations": ["Start building your habit with small, achievable goals."]
            }
        
        # Calculate key metrics
        current_streak = calculate_current_streak(completions)
        consistency = calculate_consistency(completions, 30)
        total_completions = len(completions)
        
        # Rule-based prediction logic
        score = 0.0
        
        # Streak bonus (up to 40 points)
        if current_streak >= 7:
            score += 40
        elif current_streak >= 3:
            score += 25
        elif current_streak >= 1:
            score += 10
        
        # Consistency bonus (up to 30 points)
        if consistency >= 0.8:
            score += 30
        elif consistency >= 0.6:
            score += 20
        elif consistency >= 0.4:
            score += 10
        
        # Completion volume bonus (up to 20 points)
        if total_completions >= 50:
            score += 20
        elif total_completions >= 20:
            score += 15
        elif total_completions >= 10:
            score += 10
        elif total_completions >= 5:
            score += 5
        
        # Recent activity bonus (up to 10 points)
        recent_completions = get_recent_completions(completions, 7)
        if len(recent_completions) >= 5:
            score += 10
        elif len(recent_completions) >= 3:
            score += 7
        elif len(recent_completions) >= 1:
            score += 3
        
        # Normalize score to 0-100
        probability = min(score, 100) / 100
        
        # Determine prediction category
        if probability >= 0.7:
            prediction = "high"
        elif probability >= 0.4:
            prediction = "medium"
        else:
            prediction = "low"
        
        # Calculate confidence based on data quality
        confidence = min(len(completions) / 20, 1.0)  # More data = higher confidence
        
        # Generate recommendations
        recommendations = [generate_recommendation(prediction, {"id": habit_id})]
        
        return {
            "prediction": prediction,
            "probability": round(probability, 3),
            "confidence": round(confidence, 3),
            "current_streak": current_streak,
            "consistency": consistency,
            "total_completions": total_completions,
            "recent_completions": len(get_recent_completions(completions, 7)),
            "recommendations": recommendations,
            "analysis": f"Based on {total_completions} completions, {current_streak} day streak, and {consistency*100:.1f}% consistency"
        }
