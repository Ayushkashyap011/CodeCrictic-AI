"""
app/services/piston.py
Local code execution for the supported languages used by the app.

The public Piston API is now whitelist-only, so this module executes code
directly on the backend host instead of depending on an external service.
"""

from __future__ import annotations

import asyncio
import sys
import logging
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from app.models.submission import (
    Language,
    RunCodeResponse,
    TestCaseResult,
)
from app.services.code_wrapper import wrap_python_solution

logger = logging.getLogger(__name__)

# How many test cases to run concurrently.
CONCURRENCY_LIMIT = 4
# Per-process timeout in seconds.
TIMEOUT = 15.0


# Note: Windows event loop policy is set in app/main.py at module load time
# to ensure it takes effect before Uvicorn starts its event loop.

CommandFactory = Callable[[Path], list[str]]


@dataclass(frozen=True)
class RuntimeSpec:
    source_name: str
    run_command_factory: CommandFactory
    compile_command_factory: Optional[CommandFactory] = None


def _python_run_command(workdir: Path) -> list[str]:
    return [sys.executable, str(workdir / "main.py")]


def _javascript_run_command(workdir: Path) -> list[str]:
    node = shutil.which("node")
    if not node:
        raise RuntimeError("Node.js is not installed on the backend host")
    return [node, str(workdir / "main.js")]


def _java_compile_command(workdir: Path) -> list[str]:
    javac = shutil.which("javac")
    if not javac:
        raise RuntimeError("Java compiler (javac) is not installed on the backend host")
    return [javac, str(workdir / "Main.java")]


def _java_run_command(workdir: Path) -> list[str]:
    java = shutil.which("java")
    if not java:
        raise RuntimeError("Java runtime (java) is not installed on the backend host")
    return [java, "-cp", str(workdir), "Main"]


def _cpp_compile_command(workdir: Path) -> list[str]:
    gpp = shutil.which("g++")
    if not gpp:
        raise RuntimeError("g++ is not installed on the backend host")
    output_path = workdir / ("main.exe" if sys.platform.startswith("win") else "main.out")
    return [
        gpp,
        str(workdir / "main.cpp"),
        "-std=c++17",
        "-O2",
        "-o",
        str(output_path),
    ]


def _cpp_run_command(workdir: Path) -> list[str]:
    output_path = workdir / ("main.exe" if sys.platform.startswith("win") else "main.out")
    return [str(output_path)]


RUNTIME_SPECS: dict[Language, RuntimeSpec] = {
    Language.python: RuntimeSpec(
        source_name="main.py",
        run_command_factory=_python_run_command,
    ),
    Language.javascript: RuntimeSpec(
        source_name="main.js",
        run_command_factory=_javascript_run_command,
    ),
    Language.java: RuntimeSpec(
        source_name="Main.java",
        compile_command_factory=_java_compile_command,
        run_command_factory=_java_run_command,
    ),
    Language.cpp: RuntimeSpec(
        source_name="main.cpp",
        compile_command_factory=_cpp_compile_command,
        run_command_factory=_cpp_run_command,
    ),
}


@dataclass
class ExecutionResult:
    status: str
    stdout: str = ""
    stderr: str = ""
    compile_output: str = ""


async def _run_process(
    command: list[str],
    *,
    stdin: str = "",
    cwd: Path | None = None,
    timeout: float = TIMEOUT,
) -> tuple[int | None, str, str, bool]:
    # Prefer async subprocess when available (Unix / Proactor on Windows).
    # On some Windows event loops (Selector) `subprocess_exec` is not
    # implemented and raises NotImplementedError — fall back to a
    # synchronous `subprocess.run` executed in a thread.
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=str(cwd) if cwd else None,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(stdin.encode("utf-8")),
                timeout=timeout,
            )
            return (
                process.returncode,
                stdout_bytes.decode("utf-8", errors="replace"),
                stderr_bytes.decode("utf-8", errors="replace"),
                False,
            )
        except asyncio.TimeoutError:
            process.kill()
            stdout_bytes, stderr_bytes = await process.communicate()
            return (
                None,
                stdout_bytes.decode("utf-8", errors="replace"),
                stderr_bytes.decode("utf-8", errors="replace"),
                True,
            )
    except NotImplementedError:
        # Fallback: run synchronously in a thread.
        import subprocess

        def _sync_run():
            try:
                completed = subprocess.run(
                    command,
                    input=stdin.encode("utf-8"),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=str(cwd) if cwd else None,
                    timeout=timeout,
                )
                return (
                    completed.returncode,
                    completed.stdout.decode("utf-8", errors="replace"),
                    completed.stderr.decode("utf-8", errors="replace"),
                    False,
                )
            except subprocess.TimeoutExpired as exc:
                out = b""
                err = b""
                if exc.stdout:
                    out = exc.stdout
                if exc.stderr:
                    err = exc.stderr
                return (
                    None,
                    out.decode("utf-8", errors="replace"),
                    err.decode("utf-8", errors="replace"),
                    True,
                )

        return await asyncio.to_thread(_sync_run)


def _spec_for(language: Language) -> RuntimeSpec:
    try:
        return RUNTIME_SPECS[language]
    except KeyError as exc:
        raise RuntimeError(f"Unsupported language: {language.value}") from exc


def _normalize_output(text: str) -> str:
    return text.strip()


class PistonService:
    """
    Executes code for both:
      - run_code()       -> single execution with custom stdin (Run button)
      - run_test_cases() -> batch execution against hidden test cases (Submit)
    """

    async def _execute_local(
        self,
        source_code: str,
        language: Language,
        stdin: str = "",
    ) -> ExecutionResult:
        spec = _spec_for(language)

        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = Path(temp_dir)
            source_path = workdir / spec.source_name
            source_path.write_text(source_code, encoding="utf-8")

            if spec.compile_command_factory:
                try:
                    compile_command = spec.compile_command_factory(workdir)
                except RuntimeError as exc:
                    return ExecutionResult(status="Error", stderr=str(exc))

                compile_rc, compile_stdout, compile_stderr, compile_timed_out = await _run_process(
                    compile_command,
                    cwd=workdir,
                )
                if compile_timed_out:
                    return ExecutionResult(
                        status="Time Limit Exceeded",
                        compile_output="Compilation timed out.",
                    )
                if compile_rc != 0:
                    compile_output = _normalize_output(compile_stderr) or _normalize_output(compile_stdout) or "Compilation error"
                    return ExecutionResult(
                        status="Compilation Error",
                        compile_output=compile_output,
                    )

            try:
                run_command = spec.run_command_factory(workdir)
            except RuntimeError as exc:
                return ExecutionResult(status="Error", stderr=str(exc))

            run_rc, run_stdout, run_stderr, run_timed_out = await _run_process(
                run_command,
                stdin=stdin,
                cwd=workdir,
            )
            if run_timed_out:
                return ExecutionResult(
                    status="Time Limit Exceeded",
                    stderr="Execution timed out.",
                )

            if run_rc == 0:
                return ExecutionResult(
                    status="Accepted",
                    stdout=run_stdout,
                    stderr=run_stderr,
                )

            stderr = _normalize_output(run_stderr) or _normalize_output(run_stdout) or "Runtime error"
            return ExecutionResult(
                status="Runtime Error",
                stdout=run_stdout,
                stderr=stderr,
            )

    async def run_code(
        self,
        source_code: str,
        language: Language,
        stdin: str = "",
    ) -> RunCodeResponse:
        result = await self._execute_local(source_code, language, stdin)

        return RunCodeResponse(
            stdout=_normalize_output(result.stdout) or None,
            stderr=_normalize_output(result.stderr) or None,
            compile_output=_normalize_output(result.compile_output) or None,
            status=result.status,
            runtime_ms=None,
            memory_kb=None,
        )

    async def _execute_one(
        self,
        semaphore: asyncio.Semaphore,
        source_code: str,
        language: Language,
        test_case: dict,
        test_number: int,
    ) -> TestCaseResult:
        stdin = test_case["input"]
        expected = test_case["expected_output"].strip()

        async with semaphore:
            try:
                # For Python, wrap the solution code to handle input parsing
                final_code = source_code
                if language == Language.python:
                    logger.info(f"[Test {test_number}] Wrapping Python solution for input: {stdin[:50]}")
                    final_code = wrap_python_solution(source_code, stdin)
                
                result = await self._execute_local(final_code, language, "")
                logger.info(f"[Test {test_number}] Execution result: status={result.status}, stdout={result.stdout[:100] if result.stdout else 'EMPTY'}")
                
                actual = _normalize_output(result.stdout)
                passed = (result.status == "Accepted") and (actual == expected)
                
                logger.info(f"[Test {test_number}] Result: actual={actual}, expected={expected}, passed={passed}")

                error: Optional[str] = None
                if result.status == "Compilation Error":
                    error = result.compile_output or "Compilation error"
                elif result.status == "Runtime Error":
                    error = result.stderr or result.stdout or "Runtime error"
                elif result.status == "Time Limit Exceeded":
                    error = "Time Limit Exceeded"

                return TestCaseResult(
                    test_number=test_number,
                    passed=passed,
                    input=stdin,
                    expected=expected,
                    actual=actual,
                    runtime_ms=None,
                    memory_kb=None,
                    error=error,
                )
            except Exception as exc:
                logger.error(f"[Test {test_number}] Exception: {exc}", exc_info=True)
                return TestCaseResult(
                    test_number=test_number,
                    passed=False,
                    input=stdin,
                    expected=expected,
                    actual="",
                    error=str(exc),
                )

    async def run_test_cases(
        self,
        source_code: str,
        language: Language,
        test_cases: list[dict],
    ) -> list[TestCaseResult]:
        semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

        tasks = [
            self._execute_one(
                semaphore,
                source_code,
                language,
                test_case,
                index + 1,
            )
            for index, test_case in enumerate(test_cases)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        final: list[TestCaseResult] = []
        for index, result in enumerate(results):
            if isinstance(result, Exception):
                test_case = test_cases[index]
                final.append(
                    TestCaseResult(
                        test_number=index + 1,
                        passed=False,
                        input=test_case["input"],
                        expected=test_case["expected_output"],
                        actual="",
                        error=str(result),
                    )
                )
            else:
                final.append(result)

        return final


# Singleton — imported by routes
piston_service = PistonService()
