"""Reminders router."""

from fastapi import APIRouter

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.get("/")
async def list_reminders():
    """List user reminders."""
    return {"message": "Reminders endpoint - coming soon"}