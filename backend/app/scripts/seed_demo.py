"""Seed script for demo data."""

import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.models.habit import Habit
from app.models.event import Event
from app.models.reminder import Reminder
from app.models.experiment import Experiment
from app.services.streak_service import StreakService


def seed_demo_data():
    """Seed demo data."""
    db = SessionLocal()
    
    try:
        # Create demo user
        demo_user = db.query(User).filter(User.email == "demo@habitloop.local").first()
        if not demo_user:
            demo_user = User(email="demo@habitloop.local")
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
        
        print(f"Created demo user: {demo_user.email}")
        
        # Create demo habits
        habits_data = [
            {
                "title": "Drink 8oz Water",
                "notes": "Stay hydrated throughout the day",
                "schedule_json": {"type": "daily", "times": ["morning", "afternoon", "evening"]},
                "goal_type": "count",
                "target_value": Decimal("8"),
                "grace_per_week": 2,
                "timezone": "America/Chicago"
            },
            {
                "title": "Run 2km",
                "notes": "Morning cardio routine",
                "schedule_json": {"type": "weekly", "days": [1, 3, 5], "times": ["morning"]},
                "goal_type": "duration",
                "target_value": Decimal("20"),  # 20 minutes
                "grace_per_week": 1,
                "timezone": "America/Chicago"
            },
            {
                "title": "Study 30 minutes",
                "notes": "Evening study session",
                "schedule_json": {"type": "times_per_week", "count": 4, "times": ["evening"]},
                "goal_type": "duration",
                "target_value": Decimal("30"),
                "grace_per_week": 1,
                "timezone": "America/Chicago"
            }
        ]
        
        habits = []
        for habit_data in habits_data:
            habit = Habit(
                user_id=demo_user.id,
                **habit_data
            )
            db.add(habit)
            db.commit()
            db.refresh(habit)
            habits.append(habit)
            print(f"Created habit: {habit.title}")
        
        # Create reminders for each habit
        reminder_configs = [
            {
                "window": {"days": [1, 2, 3, 4, 5, 6, 7], "start_hour": 6, "end_hour": 10},
                "quiet_hours": {"start_hour": 22, "end_hour": 6},
                "timezone": "America/Chicago"
            },
            {
                "window": {"days": [1, 3, 5], "start_hour": 6, "end_hour": 9},
                "quiet_hours": {"start_hour": 22, "end_hour": 6},
                "timezone": "America/Chicago"
            },
            {
                "window": {"days": [1, 2, 3, 4, 5, 6, 7], "start_hour": 18, "end_hour": 21},
                "quiet_hours": {"start_hour": 22, "end_hour": 6},
                "timezone": "America/Chicago"
            }
        ]
        
        for i, habit in enumerate(habits):
            reminder = Reminder(
                habit_id=habit.id,
                channel="email",
                **reminder_configs[i]
            )
            db.add(reminder)
            db.commit()
            print(f"Created reminder for: {habit.title}")
        
        # Generate 21 days of realistic events
        streak_service = StreakService(db)
        
        for habit in habits:
            # Generate events for the last 21 days
            for days_ago in range(21, 0, -1):
                event_date = date.today() - timedelta(days=days_ago)
                
                # Check if habit is due on this date
                if is_habit_due_on_date(habit, event_date):
                    # 70% chance of completion
                    if (days_ago + habit.id.int % 3) % 3 != 0:  # Pseudo-random but consistent
                        # Create checkin event
                        event = Event(
                            user_id=demo_user.id,
                            habit_id=habit.id,
                            type="checkin",
                            ts=datetime.combine(event_date, datetime.min.time().replace(hour=9)),
                            payload={"value": habit.target_value}
                        )
                        db.add(event)
                    else:
                        # Create miss event
                        event = Event(
                            user_id=demo_user.id,
                            habit_id=habit.id,
                            type="miss",
                            ts=datetime.combine(event_date, datetime.min.time().replace(hour=9)),
                            payload={}
                        )
                        db.add(event)
            
            # Update streak for this habit
            streak_service.update_streak(habit)
        
        db.commit()
        print("Generated 21 days of events and updated streaks")
        
        # Create experiment assignments
        experiment_variants = ["control", "bandit"]
        for i, habit in enumerate(habits):
            variant = experiment_variants[i % len(experiment_variants)]
            experiment = Experiment(
                user_id=demo_user.id,
                name="reminder_timing",
                variant=variant
            )
            db.add(experiment)
        
        db.commit()
        print("Created experiment assignments")
        
        print("\n✅ Demo data seeded successfully!")
        print(f"Demo user: {demo_user.email}")
        print(f"Created {len(habits)} habits with reminders and 21 days of events")
        
    except Exception as e:
        print(f"❌ Error seeding demo data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def is_habit_due_on_date(habit, check_date):
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


if __name__ == "__main__":
    seed_demo_data()
