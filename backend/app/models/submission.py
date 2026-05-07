"""
app/models/submission.py
Pydantic schemas for code execution and submission results.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class Language(str, Enum):
    python = "python"
    java = "java"
    cpp = "cpp"
    javascript = "javascript"


# Piston runtime versions (for frontend display)
LANGUAGE_VERSIONS: dict[str, str] = {
    "python": "3.10.0",
    "java": "15.0.2",
    "cpp": "10.2.0",
    "javascript": "18.15.0",
}


class SubmissionStatus(str, Enum):
    pending = "Pending"
    running = "Running"
    accepted = "Accepted"
    wrong_answer = "Wrong Answer"
    time_limit = "Time Limit Exceeded"
    runtime_error = "Runtime Error"
    compilation_error = "Compilation Error"


# ── Request models ────────────────────────────────────────────────────────────

class RunCodeRequest(BaseModel):
    """Run code against provided example test cases."""
    problem_id: str
    code: str
    language: Language
    stdin: str = ""


class SubmitCodeRequest(BaseModel):
    """Submit against all hidden test cases + trigger AI review."""
    problem_id: str
    code: str
    language: Language


# ── Test case result ──────────────────────────────────────────────────────────

class TestCaseResult(BaseModel):
    test_number: int
    passed: bool
    input: str
    expected: str
    actual: str
    runtime_ms: Optional[float] = None
    memory_kb: Optional[float] = None
    error: Optional[str] = None


# ── Response models ───────────────────────────────────────────────────────────

class RunCodeResponse(BaseModel):
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    compile_output: Optional[str] = None
    status: str
    runtime_ms: Optional[float] = None
    memory_kb: Optional[float] = None


class SubmissionResult(BaseModel):
    submission_id: str
    problem_id: str
    status: SubmissionStatus
    language: Language
    code: str
    test_results: list[TestCaseResult] = []
    passed_count: int = 0
    total_count: int = 0
    runtime_ms: Optional[float] = None
    memory_kb: Optional[float] = None
    ai_review: Optional[dict] = None   # populated in Part 2
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


# ── MongoDB document ──────────────────────────────────────────────────────────

class SubmissionInDB(SubmissionResult):
    """Stored in submissions collection."""
    pass
