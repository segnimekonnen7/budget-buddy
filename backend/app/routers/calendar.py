"""Calendar router."""

from fastapi import APIRouter

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/")
async def get_calendar():
    """Get calendar data."""
    return {"message": "Calendar endpoint - coming soon"}