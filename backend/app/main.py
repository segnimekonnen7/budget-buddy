"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings
from app.routers import auth, habits, reminders, admin, insights, calendar, health
from app.services.scheduler_service import SchedulerService
from app.db.session import SessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global scheduler
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Habit Loop API")
    
    # Start scheduler
    scheduler.start()
    
    # Add reminder job
    scheduler.add_job(
        run_reminder_job,
        trigger=IntervalTrigger(minutes=settings.scheduler_interval_minutes),
        id="reminder_job",
        replace_existing=True
    )
    
    # Add weekly digest job (runs every Sunday at 18:00)
    scheduler.add_job(
        run_weekly_digest_job,
        trigger="cron",
        day_of_week=6,  # Sunday
        hour=18,
        minute=0,
        id="weekly_digest_job",
        replace_existing=True
    )
    
    logger.info("Scheduler started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Habit Loop API")
    scheduler.shutdown()


def run_reminder_job():
    """Run reminder job."""
    db = SessionLocal()
    try:
        scheduler_service = SchedulerService(db)
        stats = scheduler_service.run_reminders()
        logger.info(f"Reminder job completed: {stats}")
    except Exception as e:
        logger.error(f"Reminder job failed: {e}")
    finally:
        db.close()


def run_weekly_digest_job():
    """Run weekly digest job."""
    db = SessionLocal()
    try:
        scheduler_service = SchedulerService(db)
        stats = scheduler_service.run_weekly_digest()
        logger.info(f"Weekly digest job completed: {stats}")
    except Exception as e:
        logger.error(f"Weekly digest job failed: {e}")
    finally:
        db.close()


# Create FastAPI app
app = FastAPI(
    title="Habit Loop API",
    description="Science-backed habit builder with adaptive reminders",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(reminders.router)
app.include_router(admin.router)
app.include_router(insights.router)
app.include_router(calendar.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)