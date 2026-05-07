"""
app/services/problems.py
Business logic for fetching, filtering, and creating problems.
"""
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.problem import (
    ProblemInDB, ProblemListItem, ProblemDetail,
    Difficulty, Category
)
import logging

logger = logging.getLogger(__name__)
COLLECTION = "problems"


def _oid(doc: dict) -> str:
    return str(doc["_id"])


def _to_list_item(doc: dict) -> ProblemListItem:
    return ProblemListItem(
        id=_oid(doc),
        title=doc["title"],
        slug=doc["slug"],
        difficulty=doc["difficulty"],
        category=doc["category"],
        tags=doc.get("tags", []),
        acceptance_rate=doc.get("acceptance_rate", 0.0),
    )


def _to_detail(doc: dict) -> ProblemDetail:
    return ProblemDetail(
        id=_oid(doc),
        title=doc["title"],
        slug=doc["slug"],
        difficulty=doc["difficulty"],
        category=doc["category"],
        description=doc["description"],
        constraints=doc.get("constraints", []),
        examples=doc.get("examples", []),
        starter_code=doc.get("starter_code", {}),
        tags=doc.get("tags", []),
        acceptance_rate=doc.get("acceptance_rate", 0.0),
    )


async def get_all_problems(
    db: AsyncIOMotorDatabase,
    difficulty: Difficulty | None = None,
    category: Category | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[ProblemListItem]:
    """Return paginated list of problems, optionally filtered."""
    query: dict = {}
    if difficulty:
        query["difficulty"] = difficulty.value
    if category:
        query["category"] = category.value
    if search:
        query["title"] = {"$regex": search, "$options": "i"}

    cursor = (
        db[COLLECTION]
        .find(query, {"hidden_testcases": 0})   # never expose hidden cases
        .skip(skip)
        .limit(limit)
        .sort("title", 1)
    )
    docs = await cursor.to_list(length=limit)
    return [_to_list_item(d) for d in docs]


async def get_problem_by_id(
    db: AsyncIOMotorDatabase,
    problem_id: str,
) -> ProblemDetail | None:
    """Fetch a single problem by MongoDB ObjectId (hides hidden_testcases)."""
    try:
        oid = ObjectId(problem_id)
    except Exception:
        return None

    doc = await db[COLLECTION].find_one(
        {"_id": oid}, {"hidden_testcases": 0}
    )
    return _to_detail(doc) if doc else None


async def get_problem_by_slug(
    db: AsyncIOMotorDatabase,
    slug: str,
) -> ProblemDetail | None:
    doc = await db[COLLECTION].find_one(
        {"slug": slug}, {"hidden_testcases": 0}
    )
    return _to_detail(doc) if doc else None


async def get_hidden_testcases(
    db: AsyncIOMotorDatabase,
    problem_id: str,
) -> list[dict]:
    """Internal use only — returns hidden test cases for execution."""
    try:
        oid = ObjectId(problem_id)
    except Exception:
        return []
    doc = await db[COLLECTION].find_one(
        {"_id": oid}, {"hidden_testcases": 1}
    )
    return doc.get("hidden_testcases", []) if doc else []


async def increment_submission_count(
    db: AsyncIOMotorDatabase,
    problem_id: str,
    accepted: bool,
) -> None:
    """Update acceptance rate after each submission."""
    try:
        oid = ObjectId(problem_id)
    except Exception:
        return
    inc = {"total_submissions": 1}
    if accepted:
        inc["accepted_submissions"] = 1   # type: ignore[assignment]

    await db[COLLECTION].update_one({"_id": oid}, {"$inc": inc})
