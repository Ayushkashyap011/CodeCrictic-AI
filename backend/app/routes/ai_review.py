"""
app/routes/ai_review.py
"""
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database.connection import get_db
from app.ai_engine.review_service import run_ai_review
from app.models.ai_review import AIReviewRequest, AIReviewResponse
from app.services.submissions import get_submission_by_id

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/review", response_model=AIReviewResponse)
async def request_ai_review(
    req: AIReviewRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    # Validate that the submission exists in MongoDB
    existing_submission = await get_submission_by_id(db, req.submission_id)
    if not existing_submission:
        raise HTTPException(status_code=404, detail="Submission not found. Use a valid submission_id from /execute/submit.")
    
    review = await run_ai_review(db, req)
    return AIReviewResponse(submission_id=req.submission_id, **review.model_dump())


@router.get("/review/{submission_id}", response_model=AIReviewResponse)
async def get_review(
    submission_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    submission = await get_submission_by_id(db, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if not submission.ai_review:
        raise HTTPException(status_code=202, detail="AI review not yet available")
    return AIReviewResponse(submission_id=submission_id, **submission.ai_review)
