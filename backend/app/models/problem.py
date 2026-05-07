"""
app/models/problem.py
Pydantic schemas for problems stored in MongoDB.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class Difficulty(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"


class Category(str, Enum):
    arrays = "Arrays"
    strings = "Strings"
    trees = "Trees"
    graphs = "Graphs"
    dynamic_programming = "Dynamic Programming"
    hashmaps = "HashMaps"
    linked_lists = "Linked Lists"
    sorting = "Sorting"
    binary_search = "Binary Search"
    two_pointers = "Two Pointers"


class Example(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None


class TestCase(BaseModel):
    input: str
    expected_output: str


class StarterCode(BaseModel):
    python: str = ""
    java: str = ""
    cpp: str = ""
    javascript: str = ""


# ── Database document model ──────────────────────────────────────────────────

class ProblemInDB(BaseModel):
    """Full problem document as stored in MongoDB."""
    title: str
    slug: str                          # url-friendly id e.g. "two-sum"
    difficulty: Difficulty
    category: Category
    description: str
    constraints: list[str] = []
    examples: list[Example] = []
    hidden_testcases: list[TestCase] = []  # never sent to client
    starter_code: StarterCode = StarterCode()
    tags: list[str] = []
    acceptance_rate: float = 0.0
    total_submissions: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── API response models (hide hidden_testcases) ───────────────────────────────

class ProblemListItem(BaseModel):
    """Slim model for the problem list page."""
    id: str
    title: str
    slug: str
    difficulty: Difficulty
    category: Category
    tags: list[str] = []
    acceptance_rate: float


class ProblemDetail(BaseModel):
    """Full problem sent to the coding workspace (no hidden test cases)."""
    id: str
    title: str
    slug: str
    difficulty: Difficulty
    category: Category
    description: str
    constraints: list[str]
    examples: list[Example]
    starter_code: StarterCode
    tags: list[str]
    acceptance_rate: float
