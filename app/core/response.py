"""The :class:`Response` — a worker's normalized result for a :class:`Task`.

Every worker, no matter its transport (HTTP API, browser automation, anything
future), returns a :class:`Response`. This uniform shape is what lets the Response
Collector (Milestone 8) gather heterogeneous worker outputs and the Judge
(Milestone 9) reconcile them.

See ``planning/decisions/ADR-0002`` for why this is a typed object rather than a
bare string.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from app.core.task import _utcnow  # shared timestamp helper


class ResponseStatus(str, Enum):
    """Outcome of a worker attempt.

    Inheriting from ``str`` keeps the enum JSON-serializable and readable in logs.
    """

    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class Response:
    """A normalized worker response.

    Attributes:
        text: The model's answer. Empty string on failure (see ``error``).
        worker_name: Name of the worker that produced this response. Provenance —
            the Judge and audit trail depend on knowing who said what.
        status: Success or failure of this attempt.
        latency_ms: Wall-clock time from send to response, in milliseconds.
        created_at: When this response object was constructed (UTC).
        error: Human-readable error message when ``status == FAILED``; else ``None``.
    """

    text: str
    worker_name: str
    status: ResponseStatus
    latency_ms: float = 0.0
    created_at: datetime = field(default_factory=_utcnow)
    error: str | None = None

    def __post_init__(self) -> None:
        if self.status is ResponseStatus.FAILED and self.error is None:
            object.__setattr__(self, "error", "Unknown error")
        if self.status is ResponseStatus.SUCCESS and not self.text.strip():
            raise ValueError(
                "A successful Response must carry non-empty text. "
                "Use status=FAILED with an error message instead."
            )
