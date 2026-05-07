"""
app/ai_engine/review_service.py
Orchestrates AI review: calls DeepSeek, patches submission in MongoDB.
"""
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.ai_engine.groq_client import groq_client
from app.models.ai_review import AIReviewResult, AIReviewRequest

logger = logging.getLogger(__name__)


async def run_ai_review(
    db: AsyncIOMotorDatabase,
    req: AIReviewRequest,
) -> AIReviewResult:
    logger.info("Starting AI review for submission %s", req.submission_id)

    review = await groq_client.review_code(
        problem_title=req.problem_title,
        problem_difficulty=req.problem_difficulty,
        language=req.language,
        code=req.code,
        passed_count=req.passed_count,
        total_count=req.total_count,
    )

    await _patch_submission(db, req.submission_id, review)

    logger.info(
        "AI review complete for %s — level: %s, correctness: %d/10",
        req.submission_id,
        review.estimated_level,
        review.scores.correctness,
    )

    return review


async def _patch_submission(
    db: AsyncIOMotorDatabase,
    submission_id: str,
    review: AIReviewResult,
) -> None:
    review_dict = review.model_dump()

    result = await db["submissions"].update_one(
        {"submission_id": submission_id},
        {"$set": {"ai_review": review_dict}},
    )

    if result.matched_count == 0:
        try:
            oid = ObjectId(submission_id)
            await db["submissions"].update_one(
                {"_id": oid},
                {"$set": {"ai_review": review_dict}},
            )
        except Exception:
            logger.warning("Could not patch submission %s — not found", submission_id)
