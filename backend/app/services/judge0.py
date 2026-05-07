"""
app/services/judge0.py
Handles all communication with the Judge0 API.
Supports: run (custom input) and batch execute (hidden test cases).
"""
import httpx
import asyncio
import base64
import logging
from typing import Optional
from app.config import get_settings
from app.models.submission import (
    Language, LANGUAGE_IDS,
    RunCodeResponse, TestCaseResult
)

logger = logging.getLogger(__name__)

# Judge0 status IDs
STATUS_ACCEPTED = 3
STATUS_WRONG_ANSWER = 4
STATUS_TLE = 5
STATUS_CE = 6
STATUS_RE_IDS = {7, 8, 9, 10, 11, 12}

# Polling config
MAX_POLLS = 10
POLL_INTERVAL = 1.0   # seconds


def _b64_encode(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def _b64_decode(text: str | None) -> str:
    if not text:
        return ""
    try:
        return base64.b64decode(text).decode(errors="replace")
    except Exception:
        return text


class Judge0Service:
    def __init__(self):
        settings = get_settings()
        self.base_url = settings.judge0_url.rstrip("/")
        self.headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Key": settings.judge0_api_key,
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
        }

    # ── Internal helpers ──────────────────────────────────────────────────────

    async def _create_submission(
        self,
        client: httpx.AsyncClient,
        source_code: str,
        language: Language,
        stdin: str = "",
        expected_output: str = "",
    ) -> str:
        """Submit code to Judge0 and return the token."""
        payload = {
            "source_code": _b64_encode(source_code),
            "language_id": LANGUAGE_IDS[language],
            "stdin": _b64_encode(stdin),
            "expected_output": _b64_encode(expected_output) if expected_output else None,
            "base64_encoded": True,
            "wait": False,
        }
        resp = await client.post(
            f"{self.base_url}/submissions",
            json=payload,
            headers=self.headers,
            timeout=15.0,
        )
        resp.raise_for_status()
        return resp.json()["token"]

    async def _poll_submission(
        self,
        client: httpx.AsyncClient,
        token: str,
    ) -> dict:
        """Poll a single submission until it finishes."""
        for _ in range(MAX_POLLS):
            await asyncio.sleep(POLL_INTERVAL)
            resp = await client.get(
                f"{self.base_url}/submissions/{token}",
                headers=self.headers,
                params={"base64_encoded": "true", "fields": "*"},
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            if data["status"]["id"] > 2:   # 1=In Queue, 2=Processing
                return data
        # Timed out waiting
        return {"status": {"id": 5, "description": "Time Limit Exceeded"}}

    # ── Public API ────────────────────────────────────────────────────────────

    async def run_code(
        self,
        source_code: str,
        language: Language,
        stdin: str = "",
    ) -> RunCodeResponse:
        """
        Execute code with custom stdin.
        Used by the 'Run' button in the workspace.
        """
        async with httpx.AsyncClient() as client:
            try:
                token = await self._create_submission(
                    client, source_code, language, stdin
                )
                result = await self._poll_submission(client, token)
            except httpx.HTTPStatusError as e:
                logger.error("Judge0 HTTP error: %s", e)
                return RunCodeResponse(
                    status="Error",
                    stderr=f"Execution service error: {e.response.status_code}",
                )
            except Exception as e:
                logger.error("Judge0 unexpected error: %s", e)
                return RunCodeResponse(status="Error", stderr=str(e))

        status_desc = result["status"]["description"]
        return RunCodeResponse(
            stdout=_b64_decode(result.get("stdout")),
            stderr=_b64_decode(result.get("stderr")),
            compile_output=_b64_decode(result.get("compile_output")),
            status=status_desc,
            runtime_ms=float(result["time"]) * 1000 if result.get("time") else None,
            memory_kb=float(result["memory"]) if result.get("memory") else None,
        )

    async def run_test_cases(
        self,
        source_code: str,
        language: Language,
        test_cases: list[dict],   # [{"input": ..., "expected_output": ...}]
    ) -> list[TestCaseResult]:
        """
        Execute code against multiple hidden test cases concurrently.
        Returns a result per test case.
        """
        async with httpx.AsyncClient() as client:
            # Submit all test cases simultaneously
            token_tasks = [
                self._create_submission(
                    client,
                    source_code,
                    language,
                    tc["input"],
                    tc["expected_output"],
                )
                for tc in test_cases
            ]
            try:
                tokens = await asyncio.gather(*token_tasks)
            except Exception as e:
                logger.error("Batch submission error: %s", e)
                return [
                    TestCaseResult(
                        test_number=i + 1,
                        passed=False,
                        input=tc["input"],
                        expected=tc["expected_output"],
                        actual="",
                        error=str(e),
                    )
                    for i, tc in enumerate(test_cases)
                ]

            # Poll all submissions concurrently
            poll_tasks = [self._poll_submission(client, t) for t in tokens]
            results = await asyncio.gather(*poll_tasks, return_exceptions=True)

        test_results: list[TestCaseResult] = []
        for i, (tc, res) in enumerate(zip(test_cases, results)):
            if isinstance(res, Exception):
                test_results.append(
                    TestCaseResult(
                        test_number=i + 1,
                        passed=False,
                        input=tc["input"],
                        expected=tc["expected_output"],
                        actual="",
                        error=str(res),
                    )
                )
                continue

            status_id = res["status"]["id"]
            stdout = _b64_decode(res.get("stdout")).strip()
            expected = tc["expected_output"].strip()
            passed = status_id == STATUS_ACCEPTED or stdout == expected

            error_msg: Optional[str] = None
            if status_id in STATUS_RE_IDS:
                error_msg = _b64_decode(res.get("stderr")) or "Runtime error"
            elif status_id == STATUS_CE:
                error_msg = _b64_decode(res.get("compile_output")) or "Compilation error"
            elif status_id == STATUS_TLE:
                error_msg = "Time Limit Exceeded"

            test_results.append(
                TestCaseResult(
                    test_number=i + 1,
                    passed=passed,
                    input=tc["input"],
                    expected=expected,
                    actual=stdout,
                    runtime_ms=float(res["time"]) * 1000 if res.get("time") else None,
                    memory_kb=float(res["memory"]) if res.get("memory") else None,
                    error=error_msg,
                )
            )

        return test_results


# Singleton — imported by routes
judge0_service = Judge0Service()
