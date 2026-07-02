"""The :class:`Task` — the unit of work a worker executes.

A Task carries a prompt plus optional metadata (id, created timestamp, tags). It is
deliberately transport-agnostic: the same Task can be fanned out to a ChatGPT
worker, a Gemini worker, or any future worker without modification. Workers and
executors never mutate a Task.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


def _utcnow() -> datetime:
    """Return the current UTC time.

    A tiny helper exists so tests can monkeypatch the timestamp source without
    monkeypatching the stdlib ``datetime`` module globally.
    """
    return datetime.now(timezone.utc)


def _new_id() -> str:
    """Return a new unique task id."""
    return f"task_{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True, slots=True)
class Task:
    """A unit of work: a prompt and the metadata to track it.

    Instances are immutable (``frozen=True``) so they can be safely shared across
    concurrent workers during fan-out. ``slots=True`` keeps them cheap and prevents
    accidental attribute assignment.
    """

    prompt: str
    id: str = field(default_factory=_new_id)
    created_at: datetime = field(default_factory=_utcnow)
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # ``frozen`` blocks normal assignment; ``object.__setattr__`` is the
        # supported way to normalize fields in a frozen dataclass.
        if not isinstance(self.prompt, str) or not self.prompt.strip():
            raise ValueError("Task.prompt must be a non-empty string")
        object.__setattr__(self, "tags", tuple(self.tags))
