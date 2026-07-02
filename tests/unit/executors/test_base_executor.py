"""Unit tests for :class:`app.executors.base_executor.BaseExecutor` and its error taxonomy."""
from __future__ import annotations

import pytest

from app.executors.base_executor import (
    BaseExecutor,
    ExecutorError,
    RetryableExecutorError,
    TerminalExecutorError,
)


class _FakeExecutor(BaseExecutor[str]):
    """Minimal concrete executor for contract testing."""

    started = False
    stopped = False

    async def start(self) -> None:
        self.started = True

    async def stop(self) -> None:
        self.stopped = True

    async def _execute(self, request: str) -> str:
        return f"echo:{request}"


class _FailingExecutor(BaseExecutor[str]):
    stopped = False

    async def stop(self) -> None:
        self.stopped = True

    async def _execute(self, request: str) -> str:
        raise RetryableExecutorError("transient")


class TestErrorHierarchy:
    def test_retryable_is_executor_error(self) -> None:
        assert issubclass(RetryableExecutorError, ExecutorError)

    def test_terminal_is_executor_error(self) -> None:
        assert issubclass(TerminalExecutorError, ExecutorError)

    def test_retryable_and_terminal_are_distinct(self) -> None:
        # The Retry Engine (M7) branches on this distinction.
        assert RetryableExecutorError is not TerminalExecutorError


class TestBaseExecutorIsAbstract:
    def test_cannot_instantiate_base_directly(self) -> None:
        with pytest.raises(TypeError):
            BaseExecutor()  # type: ignore[abstract]


class TestExecute:
    async def test_returns_raw_string(self) -> None:
        ex = _FakeExecutor()

        result = await ex.execute("hello")

        assert result == "echo:hello"

    async def test_does_not_swallow_executor_errors(self) -> None:
        # execute() is a thin, non-retrying wrapper: errors propagate for the
        # worker / retry engine to classify.
        ex = _FailingExecutor()

        with pytest.raises(RetryableExecutorError):
            await ex.execute("hi")


class TestLifecycle:
    async def test_context_manager_calls_start_and_stop(self) -> None:
        ex = _FakeExecutor()

        async with ex:
            assert ex.started is True
            assert ex.stopped is False

        assert ex.stopped is True

    async def test_stop_runs_even_on_exception(self) -> None:
        ex = _FailingExecutor()

        with pytest.raises(RetryableExecutorError):
            async with ex:
                await ex.execute("x")

        assert ex.stopped is True


class TestGenericRequestType:
    def test_accepts_int_request_type(self) -> None:
        # A generic over R proves the base is reusable across request shapes.

        class _IntExecutor(BaseExecutor[int]):
            async def _execute(self, request: int) -> str:
                return str(request * 2)

        assert _IntExecutor  # noqa: F841 — defined & instantiable is the point

    def test_default_start_and_stop_are_no_ops(self) -> None:
        class _Stateless(BaseExecutor[str]):
            async def _execute(self, request: str) -> str:
                return request

        ex = _Stateless()
        # Default no-ops should not raise.
        import asyncio

        asyncio.run(ex.start())
        asyncio.run(ex.stop())
