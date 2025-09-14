from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..db.session import SessionLocal
from ..schemas import JobOut, SearchResult
from ..utils.geo import expand_location_terms

router = APIRouter(prefix="/jobs", tags=["jobs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/search", response_model=SearchResult)
def search_jobs(
    query: str = Query(default=""),
    loc: str | None = None,
    page: int = 1,
    per_page: int = 20,
    source: list[str] | None = Query(default=None),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * per_page
    params: dict = {"limit": per_page, "offset": offset}
    where = ["1=1"]

    if source:
        where.append("source = ANY(:sources)")
        params["sources"] = source

    if loc:
        pats = expand_location_terms(loc)
        if pats:
            clauses = []
            for i, p in enumerate(pats):
                key = f"loc_{i}"
                params[key] = p
                clauses.append(f"location ILIKE :{key}")
            where.append("(" + " OR ".join(clauses) + ")")

    rank_sql = ""
    if query.strip():
        params["q"] = query.strip()
        where.append("tsv @@ plainto_tsquery('english', :q)")
        rank_sql = ", ts_rank(tsv, plainto_tsquery('english', :q)) AS rank"

    where_sql = " AND ".join(where)
    total = db.execute(text(f"SELECT COUNT(*) FROM jobs WHERE {where_sql}"), params).scalar() or 0
    order = "ORDER BY posted_at DESC" if not rank_sql else "ORDER BY rank DESC, posted_at DESC"

    rows = db.execute(text(
        f"SELECT id, title, company, location, description, apply_url, posted_at, source, external_id {rank_sql} "
        f"FROM jobs WHERE {where_sql} {order} LIMIT :limit OFFSET :offset"
    ), params).mappings().all()

    return SearchResult(total=total, page=page, per_page=per_page, items=[JobOut(**dict(r)) for r in rows])

@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    row = db.execute(text(
        "SELECT id, title, company, location, description, apply_url, posted_at, source, external_id FROM jobs WHERE id=:id"
    ), {"id": job_id}).mappings().first()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(404, "Job not found")
    return JobOut(**row)
