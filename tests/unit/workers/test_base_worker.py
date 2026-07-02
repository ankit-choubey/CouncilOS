"""Unit tests for :class:`app.workers.base_worker.BaseWorker` and its error taxonomy.

The Template Method (:meth:`send`) is the load-bearing piece: it must build a
consistent :class:`Response` (timing, provenance, status) for both success and
worker-error paths, and re-raise unexpected exceptions.
"""
from __future__ import annotations

import pytest

from app.core.response import Response, ResponseStatus
from app.core.task import Task
from app.workers.base_worker import (
    BaseWorker,
    RetryableWorkerError,
    TerminalWorkerError,
    WorkerError,
)


class _OkWorker(BaseWorker):
    """Returns a canned string."""

    started = False
    stopped = False

    async def start(self) -> None:
        self.started = True

    async def stop(self) -> None:
        self.stopped = False  # sentinel; set False to prove stop ran
        # (set False rather than True so the assertion is meaningful: it
        # distinguishes "ran and toggled" from "never changed from default".)

    async def _send(self, task: Task) -> str:
        return f"answer to: {task.prompt}"


class _TransientWorker(BaseWorker):
    async def _send(self, task: Task) -> str:
        raise RetryableWorkerError("rate limited")


class _TerminalWorker(BaseWorker):
    async def _send(self, task: Task) -> str:
        raise TerminalWorkerError("auth rejected")


class _ExplodingWorker(BaseWorker):
    async def _send(self, task: Task) -> str:
        # A bug, not a WorkerError. Must NOT be swallowed.
        raise RuntimeError("unexpected explosion")


class TestErrorHierarchy:
    def test_retryable_is_worker_error(self) -> None:
        assert issubclass(RetryableWorkerError, WorkerError)

    def test_terminal_is_worker_error(self) -> None:
        assert issubclass(TerminalWorkerError, WorkerError)


class TestBaseWorkerIsAbstract:
    def test_cannot_instantiate_base_directly(self) -> None:
        with pytest.raises(TypeError):
            BaseWorker("x")  # type: ignore[abstract]


class TestConstruction:
    def test_requires_non_empty_name(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            _OkWorker(name="")  # type: ignore[arg-type]


class TestSendSuccess:
    async def test_returns_success_response_with_text(self) -> None:
        worker = _OkWorker(name="echo")

        resp = await worker.send(Task(prompt="hello"))

        assert resp.status is ResponseStatus.SUCCESS
        assert resp.text == "answer to: hello"
        assert resp.error is None

    async def test_stamps_provenance_worker_name(self) -> None:
        resp = await _OkWorker(name="chatgpt").send(Task(prompt="hi"))

        assert resp.worker_name == "chatgpt"

    async def test_records_positive_latency(self) -> None:
        resp = await _OkWorker(name="w").send(Task(prompt="hi"))

        # Non-negative; allow 0.0 for instant fakes.
        assert resp.latency_ms >= 0.0


class TestSendFailureWrapping:
    async def test_wraps_retryable_error_into_failed_response(self) -> None:
        resp = await _TransientWorker(name="gemini").send(Task(prompt="hi"))

        assert resp.status is ResponseStatus.FAILED
        assert resp.text == ""
        assert resp.worker_name == "gemini"
        assert resp.error is not None
        assert "rate limited" in resp.error

    async def test_wraps_terminal_error_into_failed_response(self) -> None:
        resp = await _TerminalWorker(name="perplex").send(Task(prompt="hi"))

        assert resp.status is ResponseStatus.FAILED
        assert "auth rejected" in (resp.error or "")

    async def test_records_latency_even_on_failure(self) -> None:
        resp = await _TransientWorker(name="w").send(Task(prompt="hi"))

        assert resp.latency_ms >= 0.0


class TestSendDoesNotSwallowBugs:
    async def test_propagates_unexpected_exception(self) -> None:
        # CODING_STANDARDS: fail loud. A RuntimeError is not a WorkerError and
        # must surface, not become a FAILED Response.
        with pytest.raises(RuntimeError, match="unexpected explosion"):
            await _ExplodingWorker(name="buggy").send(Task(prompt="hi"))


class TestLifecycle:
    async def test_context_manager_calls_start_and_stop(self) -> None:
        worker = _OkWorker(name="w")
        assert worker.started is False

        async with worker:
            assert worker.started is True

        assert worker.stopped is False  # stop() ran and set it False

    async def test_stop_runs_even_on_send_error_inside_context(self) -> None:
        worker = _TransientWorker(name="w")

        # send() itself returns a FAILED response (doesn't raise), but stop()
        # must still run on context exit.
        async with worker:
            resp = await worker.send(Task(prompt="x"))
            assert resp.status is ResponseStatus.FAILED


class TestReturnsResponse:
    async def test_send_returns_response_type(self) -> None:
        resp = await _OkWorker(name="w").send(Task(prompt="hi"))

        assert isinstance(resp, Response)
