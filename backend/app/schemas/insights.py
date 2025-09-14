"""Insights schemas."""

import uuid
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel


class AtRiskHabit(BaseModel):
    """At-risk habit schema."""
    habit_id: uuid.UUID
    title: str
    reason: str
    suggested_target: Optional[Decimal] = None


class WeeklyInsights(BaseModel):
    """Weekly insights schema."""
    completion_rate: float
    streak_health_score: int  # 0-100
    at_risk: List[AtRiskHabit]
