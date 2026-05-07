"""
app/routes/problems.py
REST endpoints for fetching problems.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database.connection import get_db
from app.services import problems as problem_svc
from app.models.problem import Difficulty, Category, ProblemListItem, ProblemDetail

router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("/", response_model=list[ProblemListItem])
async def list_problems(
    difficulty: Difficulty | None = Query(None),
    category: Category | None = Query(None),
    search: str | None = Query(None, min_length=1, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """
    Return all problems (paginated).
    Supports filtering by difficulty, category, and free-text search.
    """
    return await problem_svc.get_all_problems(
        db, difficulty, category, search, skip, limit
    )


@router.get("/{problem_id}", response_model=ProblemDetail)
async def get_problem(
    problem_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Return a single problem by its MongoDB ObjectId."""
    problem = await problem_svc.get_problem_by_id(db, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.get("/slug/{slug}", response_model=ProblemDetail)
async def get_problem_by_slug(
    slug: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Return a single problem by its URL slug."""
    problem = await problem_svc.get_problem_by_slug(db, slug)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem
