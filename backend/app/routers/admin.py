"""Admin router."""

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/")
async def admin_dashboard():
    """Admin dashboard."""
    return {"message": "Admin endpoint - coming soon"}