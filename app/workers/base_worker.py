"""The :class:`BaseWorker` contract.

A Worker owns the full lifecycle of one external model: it takes a
:class:`~app.core.task.Task`, talks to exactly one backend (via an executor), and
returns a normalized :class:`~app.core.response.Response`. Workers never talk to
each other — coordinating multiple workers is the protocol layer's job.

This module defines *only* the contract. Concrete workers (ChatGPT in Milestone 3,
Gemini in M4, Perplexity in M5) subclass :class:`BaseWorker` and implement
:meth:`_send`.

Design — Template Method:

    :meth:`send` (concrete) → timing + error wrapping + Response building
    :meth:`_send` (abstract) → the actual model interaction

This guarantees every concrete worker produces a Response with consistent
provenance (``worker_name``) and timing (``latency_ms``) without re-implementing
that bookkeeping each time.

See ``planning/decisions/ADR-0002`` (response schema), ``ADR-0003`` (async), and
``ADR-0004`` (error taxonomy) for the decisions encoded here.
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod

from app.core.response import Response, ResponseStatus
from app.core.task import Task


class WorkerError(Exception):
    """Base of the worker error hierarchy. See ``ADR-0004``."""


class RetryableWorkerError(WorkerError):
    """A transient worker failure (rate limit, brief network drop, DOM lag).

    The Retry Engine (Milestone 7) will retry these.
    """


class TerminalWorkerError(WorkerError):
    """A non-retryable worker failure (auth rejected, unsupported task).

    These should not be retried.
    """


class BaseWorker(ABC):
    """Abstract contract for every worker in CouncilOS.

    Lifecycle::

        async with worker:
            response = await worker.send(task)

    Subclasses:

    - MUST set :attr:`name` (or pass it to ``super().__init__``).
    - MUST implement :meth:`_send` — perform the model call, return raw text.
    - MAY override :meth:`start` / :meth:`stop` to manage resources
      (an executor session, a browser context, etc.).

    They MUST NOT implement retry, cross-worker coordination, or judging — those
    belong to later layers.
    """

    name: str

    def __init__(self, name: str) -> None:
        # ``worker_name`` provenance on every Response depends on this being set.
        if not isinstance(name, str) or not name.strip():
            raise ValueError("BaseWorker.name must be a non-empty string")
        self.name = name

    # -- lifecycle -----------------------------------------------------------

    async def start(self) -> None:
        """Acquire resources before the first send. Default is a no-op."""

    async def stop(self) -> None:
        """Release resources after the last send. Default is a no-op."""

    async def __aenter__(self) -> BaseWorker:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.stop()

    # -- the contract --------------------------------------------------------

    @abstractmethod
    async def _send(self, task: Task) -> str:
        """Perform the actual model interaction and return raw response text.

        Raises:
            RetryableWorkerError: on transient failure.
            TerminalWorkerError: on non-retryable failure.
        """

    async def send(self, task: Task) -> Response:
        """Send a task to the model and return a normalized :class:`Response`.

        This is a Template Method: it times :meth:`_send`, wraps any
        :class:`WorkerError` into a ``FAILED`` response carrying provenance, and
        builds a success response otherwise.

        Unexpected (non-WorkerError) exceptions are **not** caught: per the
        coding standards we fail loud rather than silently swallowing bugs.
        """
        start = time.perf_counter()
        try:
            text = await self._send(task)
        except WorkerError as exc:
            latency_ms = (time.perf_counter() - start) * 1000.0
            return Response(
                text="",
                worker_name=self.name,
                status=ResponseStatus.FAILED,
                latency_ms=latency_ms,
                error=str(exc) or exc.__class__.__name__,
            )
        latency_ms = (time.perf_counter() - start) * 1000.0
        return Response(
            text=text,
            worker_name=self.name,
            status=ResponseStatus.SUCCESS,
            latency_ms=latency_ms,
        )
