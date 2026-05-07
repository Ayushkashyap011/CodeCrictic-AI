"""
app/models/ai_review.py
Pydantic schemas for the AI code review engine output.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class CodingLevel(str, Enum):
    beginner = "Beginner"
    junior = "Junior Developer"
    mid = "Mid-Level Developer"
    senior = "Senior Developer"
    expert = "Expert / Principal Engineer"


class ComplexityAnalysis(BaseModel):
    time_complexity: str = "O(n)"
    space_complexity: str = "O(1)"
    time_explanation: str = ""
    space_explanation: str = ""


class ScoreBreakdown(BaseModel):
    correctness: int = Field(0, ge=0, le=10)
    optimization: int = Field(0, ge=0, le=10)
    readability: int = Field(0, ge=0, le=10)
    interview_readiness: int = Field(0, ge=0, le=10)
    senior_engineer: int = Field(0, ge=0, le=10)


class AIReviewResult(BaseModel):
    scores: ScoreBreakdown = ScoreBreakdown()
    estimated_level: CodingLevel = CodingLevel.beginner
    summary: str = ""
    strengths: list[str] = []
    issues: list[str] = []
    improvements: list[str] = []
    complexity: ComplexityAnalysis = ComplexityAnalysis()
    optimized_approach: Optional[str] = None
    interview_tips: list[str] = []
    review_status: str = "success"


class AIReviewRequest(BaseModel):
    submission_id: str
    problem_id: str
    problem_title: str
    problem_difficulty: str
    code: str
    language: str
    passed_count: int
    total_count: int


class AIReviewResponse(AIReviewResult):
    submission_id: str
