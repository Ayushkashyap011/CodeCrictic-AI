"""
app/ai_engine/deepseek_client.py
DeepSeek API client for AI code review.

Get your free API key at: https://platform.deepseek.com
"""

import httpx
import json
import logging
import re
from typing import Optional
from app.config import get_settings
from app.models.ai_review import AIReviewResult, ScoreBreakdown, ComplexityAnalysis, CodingLevel
from app.ai_engine.prompts import SYSTEM_PROMPT, build_review_prompt

logger = logging.getLogger(__name__)

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-coder"
MAX_TOKENS = 2000
TEMPERATURE = 0.3
TIMEOUT = 60.0


def _extract_json(text: str) -> Optional[dict]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    patterns = [
        r"```json\s*([\s\S]*?)\s*```",
        r"```\s*([\s\S]*?)\s*```",
        r"\{[\s\S]*\}",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            candidate = match.group(1) if "```" in pattern else match.group(0)
            try:
                return json.loads(candidate.strip())
            except json.JSONDecodeError:
                continue
    return None


def _clamp(val, lo: int = 0, hi: int = 10) -> int:
    try:
        return max(lo, min(hi, int(val)))
    except (TypeError, ValueError):
        return 5


def _ensure_list(val) -> list:
    if isinstance(val, list):
        return [str(i) for i in val]
    if isinstance(val, str):
        return [val]
    return []


def _infer_correctness(passed: int, total: int) -> int:
    if total == 0:
        return 5
    return round((passed / total) * 10)


def _parse_review(raw: dict, passed: int, total: int) -> AIReviewResult:
    scores_raw = raw.get("scores", {})
    scores = ScoreBreakdown(
        correctness=_clamp(scores_raw.get("correctness", _infer_correctness(passed, total))),
        optimization=_clamp(scores_raw.get("optimization", 5)),
        readability=_clamp(scores_raw.get("readability", 5)),
        interview_readiness=_clamp(scores_raw.get("interview_readiness", 5)),
        senior_engineer=_clamp(scores_raw.get("senior_engineer", 5)),
    )

    complexity_raw = raw.get("complexity", {})
    complexity = ComplexityAnalysis(
        time_complexity=complexity_raw.get("time_complexity", "O(n)"),
        space_complexity=complexity_raw.get("space_complexity", "O(n)"),
        time_explanation=complexity_raw.get("time_explanation", ""),
        space_explanation=complexity_raw.get("space_explanation", ""),
    )

    level_str = raw.get("estimated_level", "Beginner")
    try:
        level = CodingLevel(level_str)
    except ValueError:
        level = CodingLevel.junior

    return AIReviewResult(
        scores=scores,
        estimated_level=level,
        summary=raw.get("summary", "Review completed."),
        strengths=_ensure_list(raw.get("strengths", [])),
        issues=_ensure_list(raw.get("issues", [])),
        improvements=_ensure_list(raw.get("improvements", [])),
        complexity=complexity,
        optimized_approach=raw.get("optimized_approach"),
        interview_tips=_ensure_list(raw.get("interview_tips", [])),
        review_status="success",
    )


def _fallback_review(passed: int, total: int, error: str = "") -> AIReviewResult:
    correctness = _infer_correctness(passed, total)
    logger.warning("Using fallback review. Reason: %s", error)
    return AIReviewResult(
        scores=ScoreBreakdown(
            correctness=correctness,
            optimization=5,
            readability=5,
            interview_readiness=5,
            senior_engineer=5,
        ),
        estimated_level=CodingLevel.junior,
        summary=f"Automated review: {passed}/{total} test cases passed. AI detailed review unavailable.",
        strengths=["Solution submitted successfully"] if passed > 0 else [],
        issues=["AI review service temporarily unavailable"] if error else [],
        improvements=["Configure DEEPSEEK_API_KEY in .env for detailed AI feedback"],
        complexity=ComplexityAnalysis(
            time_complexity="N/A",
            space_complexity="N/A",
            time_explanation="AI review unavailable",
            space_explanation="AI review unavailable",
        ),
        review_status="fallback",
    )


class DeepSeekClient:
    def __init__(self):
        self.settings = get_settings()

    async def review_code(
        self,
        problem_title: str,
        problem_difficulty: str,
        language: str,
        code: str,
        passed_count: int,
        total_count: int,
    ) -> AIReviewResult:
        api_key = self.settings.deepseek_api_key
        if not api_key:
            return _fallback_review(passed_count, total_count, "No API key configured")

        prompt = build_review_prompt(
            problem_title=problem_title,
            problem_difficulty=problem_difficulty,
            language=language,
            code=code,
            passed_count=passed_count,
            total_count=total_count,
        )

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "stream": False,
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            try:
                resp = await client.post(DEEPSEEK_API_URL, json=payload, headers=headers)
                resp.raise_for_status()
            except httpx.TimeoutException:
                return _fallback_review(passed_count, total_count, "API timeout")
            except httpx.HTTPStatusError as e:
                return _fallback_review(passed_count, total_count, f"HTTP {e.response.status_code}")
            except Exception as e:
                return _fallback_review(passed_count, total_count, str(e))

        try:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            return _fallback_review(passed_count, total_count, "Unexpected response structure")

        raw_json = _extract_json(content)
        if not raw_json:
            return _fallback_review(passed_count, total_count, "JSON parse failed")

        try:
            return _parse_review(raw_json, passed_count, total_count)
        except Exception as e:
            return _fallback_review(passed_count, total_count, f"Parse error: {e}")


# Singleton
deepseek_client = DeepSeekClient()
