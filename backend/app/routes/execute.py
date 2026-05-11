"""
app/routes/execute.py
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database.connection import get_db
from app.services import problems as problem_svc
from app.services import submissions as submission_svc
from app.ai_engine.review_service import run_ai_review
from app.models.submission import (
    RunCodeRequest, RunCodeResponse,
    SubmitCodeRequest, SubmissionResult,
    SubmissionStatus,
)
from app.models.ai_review import AIReviewRequest
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/execute", tags=["execute"])

try:
    from app.services.executor import executor_service as execution_service
except ImportError:
    from app.services.piston import piston_service as execution_service


@router.post("/run", response_model=SubmissionResult)
async def run_code(req: RunCodeRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Run code against example test cases (public)."""
    try:
        # Get the problem to access example test cases
        problem = await problem_svc.get_problem_by_id(db, req.problem_id)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Convert examples to test case format (Example has "output", TestCase needs "expected_output")
        test_cases = [
            {"input": ex.input, "expected_output": ex.output}
            for ex in problem.examples
        ]
        
        # Run against examples (public test cases)
        test_results = await execution_service.run_test_cases(
            req.code, req.language, test_cases, problem.title
        )
        
        # Calculate status
        passed_count = sum(1 for t in test_results if t.passed)
        total_count = len(test_results)
        status = SubmissionStatus.accepted if passed_count == total_count else SubmissionStatus.wrong_answer
        
        return SubmissionResult(
            submission_id=str(uuid.uuid4()),
            problem_id=req.problem_id,
            language=req.language,
            code=req.code,
            status=status,
            test_results=test_results,
            passed_count=passed_count,
            total_count=total_count,
        )
    except Exception as e:
        logger.error(f"Error running code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit", response_model=SubmissionResult)
async def submit_code(
    req: SubmitCodeRequest,
    background_tasks: BackgroundTasks,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    # 1. Load hidden test cases
    test_cases = await problem_svc.get_hidden_testcases(db, req.problem_id)
    if not test_cases:
        raise HTTPException(status_code=404, detail="Problem not found or has no test cases configured")

    # 2. Get problem details for AI context
    problem = await problem_svc.get_problem_by_id(db, req.problem_id)
    problem_title = problem.title if problem else "Unknown Problem"
    problem_difficulty = problem.difficulty.value if problem else "Medium"

    # 3. Execute against hidden test cases
    test_results = await execution_service.run_test_cases(
        req.code, req.language, test_cases, problem_title
    )

    # 4. Aggregate results
    passed = sum(1 for r in test_results if r.passed)
    total = len(test_results)
    all_passed = passed == total

    if all_passed:
        status = SubmissionStatus.accepted
    else:
        first_fail = next((r for r in test_results if not r.passed), None)
        if first_fail and first_fail.error:
            err = first_fail.error.lower()
            if "compile" in err:
                status = SubmissionStatus.compilation_error
            elif "time limit" in err:
                status = SubmissionStatus.time_limit
            else:
                status = SubmissionStatus.runtime_error
        else:
            status = SubmissionStatus.wrong_answer

    # 5. Build result
    submission_id = str(uuid.uuid4())
    result = SubmissionResult(
        submission_id=submission_id,
        problem_id=req.problem_id,
        status=status,
        language=req.language,
        code=req.code,
        test_results=test_results,
        passed_count=passed,
        total_count=total,
        runtime_ms=None,
        memory_kb=None,
        ai_review=None,
    )

    # 6. Save to MongoDB
    await submission_svc.save_submission(db, result)

    # 7. Update acceptance stats
    await problem_svc.increment_submission_count(db, req.problem_id, all_passed)

    # 8. Trigger AI review in background (non-blocking)
    ai_req = AIReviewRequest(
        submission_id=submission_id,
        problem_id=req.problem_id,
        problem_title=problem_title,
        problem_difficulty=problem_difficulty,
        code=req.code,
        language=req.language.value,
        passed_count=passed,
        total_count=total,
    )
    background_tasks.add_task(_background_ai_review, db, ai_req)

    return result


async def _background_ai_review(db, req):
    try:
        await run_ai_review(db, req)
    except Exception as e:
        logger.error("Background AI review failed for %s: %s", req.submission_id, e)


@router.get("/history/{problem_id}", response_model=list[SubmissionResult])
async def submission_history(problem_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await submission_svc.get_submissions_for_problem(db, problem_id)


@router.get("/submission/{submission_id}", response_model=SubmissionResult)
async def get_submission(submission_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await submission_svc.get_submission_by_id(db, submission_id)
    if not result:
        raise HTTPException(status_code=404, detail="Submission not found")
    return result