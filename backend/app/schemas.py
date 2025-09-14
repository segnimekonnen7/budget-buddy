from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    apply_url: Optional[str] = None
    posted_at: datetime
    source: str
    external_id: Optional[str] = None

class SearchResult(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[JobOut]
