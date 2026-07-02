"""The :class:`BaseExecutor` contract.

Executors are the lowest layer of CouncilOS. They perform **one atomic action**
against a transport (HTTP API, browser DOM, anything future) and return a raw
string result. They have no knowledge of:

- other executors,
- workers, protocols, or the council,
- retry, judging, or council-level error handling.

Their only job: *execute one request, return one string, manage their own
resources.* Concrete executors (e.g. ``HttpApiExecutor`` in M2, browser executors
later) implement :meth:`_execute`.

See ``planning/decisions/ADR-0004`` for the error taxonomy and ``ADR-0003`` for
the async contract.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# The request type varies by executor family (HTTP params, browser selectors...),
# so the base is generic over it. ``Any`` would erase the type safety we rely on.
R = TypeVar("R")


class ExecutorError(Exception):
    """Base of the executor error hierarchy."""


class RetryableExecutorError(ExecutorError):
    """A transient failure worth retrying (network blip, rate limit, DOM lag)."""


class TerminalExecutorError(ExecutorError):
    """A failure not worth retrying (auth rejected, malformed request, 4xx)."""


class BaseExecutor(ABC, Generic[R]):
    """Abstract contract for all executors.

    Lifecycle::

        async with executor:
            result = await executor.execute(request)

    Subclasses implement :meth:`_execute` and may override :meth:`start`/:meth:`stop`
    to acquire/release transport resources (an HTTP client, a browser page...). The
    default ``start``/``stop`` are no-ops, so stateless executors need not override
    them.
    """

    async def start(self) -> None:
        """Acquire transport resources. Default is a no-op."""

    async def stop(self) -> None:
        """Release transport resources. Default is a no-op."""

    @abstractmethod
    async def _execute(self, request: R) -> str:
        """Perform the atomic action and return the raw string result.

        Raises:
            RetryableExecutorError: on transient failure.
            TerminalExecutorError: on non-retryable failure.
        """

    async def execute(self, request: R) -> str:
        """Execute one request against the transport.

        This is the public entry point. It is a thin, non-retrying wrapper around
        :meth:`_execute`. Retrying is the responsibility of a future Retry Engine
        (Milestone 7), not the executor.
        """
        return await self._execute(request)

    async def __aenter__(self) -> BaseExecutor[R]:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.stop()
