"""
app/ai_engine/prompts.py
Prompt engineering for DeepSeek Coder AI review.
"""

SYSTEM_PROMPT = """You are CodeCritic AI — a senior software engineer and technical interviewer with 15+ years of experience at top tech companies (Google, Meta, Amazon).

Your job is to review submitted code solutions to coding problems and provide structured, honest, actionable feedback.

You MUST respond with ONLY valid JSON. No markdown, no explanation outside the JSON, no code blocks.
The JSON must exactly match the schema provided in the user message.

Be specific, constructive, and honest. Don't be overly generous with scores."""


def build_review_prompt(
    problem_title: str,
    problem_difficulty: str,
    language: str,
    code: str,
    passed_count: int,
    total_count: int,
) -> str:
    correctness_context = (
        f"The solution passed {passed_count}/{total_count} hidden test cases."
        if total_count > 0
        else "Test results unavailable."
    )

    return f"""Review this code submission and return a JSON evaluation.

PROBLEM: {problem_title} (Difficulty: {problem_difficulty})
LANGUAGE: {language}
TEST RESULTS: {correctness_context}

SUBMITTED CODE:  Return ONLY this JSON structure with no other text:
{{
  "scores": {{
    "correctness": <0-10 based on test results and logic correctness>,
    "optimization": <0-10 based on time/space complexity vs optimal>,
    "readability": <0-10 based on naming, structure, comments, clarity>,
    "interview_readiness": <0-10 would this pass a real FAANG interview>,
    "senior_engineer": <0-10 does this reflect senior engineering quality>
  }},
  "estimated_level": <one of: "Beginner", "Junior Developer", "Mid-Level Developer", "Senior Developer", "Expert / Principal Engineer">,
  "summary": "<2-3 sentence honest overall assessment>",
  "strengths": [
    "<specific strength 1>",
    "<specific strength 2>"
  ],
  "issues": [
    "<specific issue 1 with line reference if possible>",
    "<specific issue 2>"
  ],
  "improvements": [
    "<concrete actionable improvement 1>",
    "<concrete actionable improvement 2>",
    "<concrete actionable improvement 3>"
  ],
  "complexity": {{
    "time_complexity": "<Big-O notation e.g. O(n)>",
    "space_complexity": "<Big-O notation e.g. O(n)>",
    "time_explanation": "<one sentence explaining why>",
    "space_explanation": "<one sentence explaining why>"
  }},
  "optimized_approach": "<describe a better approach if one exists, or null if already optimal>",
  "interview_tips": [
    "<specific tip for performing better in interviews on this type of problem>",
    "<another tip>"
  ]
}}

Scoring guide:
- correctness: {passed_count}/{total_count} tests passed. 10 = all pass with clean logic.
- optimization: 10 = optimal complexity, 5 = correct but suboptimal, 1 = brute force
- readability: 10 = excellent naming + structure, 5 = average, 1 = cryptic
- interview_readiness: handles edge cases? clean code? would a senior engineer approve?
- senior_engineer: 10 = production-quality. 1 = works but nothing more."""