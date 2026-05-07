"""
app/services/submissions.py
Store submission results in MongoDB and retrieve history.
"""
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.submission import SubmissionResult, SubmissionInDB
import logging

logger = logging.getLogger(__name__)
COLLECTION = "submissions"


async def save_submission(
    db: AsyncIOMotorDatabase,
    result: SubmissionResult,
) -> str:
    """Persist a submission result. Returns the inserted document ID."""
    doc = result.model_dump()
    inserted = await db[COLLECTION].insert_one(doc)
    return str(inserted.inserted_id)


async def get_submission_by_id(
    db: AsyncIOMotorDatabase,
    submission_id: str,
) -> SubmissionResult | None:
    # First try to find by submission_id field (UUID or string)
    doc = await db[COLLECTION].find_one({"submission_id": submission_id})
    if doc:
        doc["submission_id"] = str(doc.pop("_id", submission_id))
        return SubmissionResult(**doc)
    
    # Fallback: try to find by MongoDB _id (ObjectId)
    try:
        oid = ObjectId(submission_id)
        doc = await db[COLLECTION].find_one({"_id": oid})
        if doc:
            doc["submission_id"] = str(doc.pop("_id"))
            return SubmissionResult(**doc)
    except Exception:
        pass
    
    return None


async def get_submissions_for_problem(
    db: AsyncIOMotorDatabase,
    problem_id: str,
    limit: int = 20,
) -> list[SubmissionResult]:
    """Retrieve recent submissions for a problem (submission history)."""
    cursor = (
        db[COLLECTION]
        .find({"problem_id": problem_id})
        .sort("submitted_at", -1)
        .limit(limit)
    )
    docs = await cursor.to_list(length=limit)
    results = []
    for doc in docs:
        doc["submission_id"] = str(doc.pop("_id"))
        results.append(SubmissionResult(**doc))
    return results
