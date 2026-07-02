"""Unit tests for :class:`app.core.task.Task`."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.core.task import Task


class TestTaskConstruction:
    def test_creates_task_with_prompt_and_defaults(self) -> None:
        task = Task(prompt="Summarize the architecture.")

        assert task.prompt == "Summarize the architecture."
        # Defaults are populated.
        assert task.id.startswith("task_")
        assert len(task.id) > len("task_")
        assert task.created_at.tzinfo is not None  # tz-aware
        assert task.tags == ()

    def test_preserves_explicit_id_and_tags(self) -> None:
        ts = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)

        task = Task(prompt="hi", id="task_custom", created_at=ts, tags=("a", "b"))

        assert task.id == "task_custom"
        assert task.created_at == ts
        assert task.tags == ("a", "b")

    def test_coerces_list_tags_to_tuple(self) -> None:
        task = Task(prompt="hi", tags=["x", "y"])  # type: ignore[arg-type]

        assert task.tags == ("x", "y")
        assert isinstance(task.tags, tuple)

    def test_assigns_unique_ids_to_two_tasks(self) -> None:
        a = Task(prompt="a")
        b = Task(prompt="b")

        assert a.id != b.id


class TestTaskImmutability:
    def test_is_frozen(self) -> None:
        task = Task(prompt="hi")

        with pytest.raises((AttributeError, Exception)):
            task.prompt = "changed"  # type: ignore[misc]

    def test_uses_slots(self) -> None:
        task = Task(prompt="hi")

        # Frozen+slots dataclasses reject undeclared attributes.
        with pytest.raises((AttributeError, Exception)):
            task.something_else = 1  # type: ignore[attr-defined]


class TestTaskValidation:
    @pytest.mark.parametrize("bad", ["", "   ", "\n\t  "])
    def test_rejects_blank_prompt(self, bad: str) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            Task(prompt=bad)

    def test_rejects_non_string_prompt(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            Task(prompt=123)  # type: ignore[arg-type]
