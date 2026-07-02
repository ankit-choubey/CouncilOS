"""Unit tests for :class:`app.core.response.Response` and :class:`ResponseStatus`."""
from __future__ import annotations

import pytest

from app.core.response import Response, ResponseStatus


class TestResponseStatus:
    def test_is_string_enum(self) -> None:
        # str-Enum keeps values JSON-serializable and readable in logs.
        assert ResponseStatus.SUCCESS.value == "success"
        assert ResponseStatus.FAILED.value == "failed"

    def test_serializes_as_string(self) -> None:
        assert ResponseStatus.SUCCESS == "success"
        assert ResponseStatus.FAILED == "failed"


class TestSuccessResponse:
    def test_builds_minimal_success(self) -> None:
        resp = Response(text="answer", worker_name="chatgpt", status=ResponseStatus.SUCCESS)

        assert resp.text == "answer"
        assert resp.worker_name == "chatgpt"
        assert resp.status is ResponseStatus.SUCCESS
        assert resp.error is None
        assert resp.latency_ms == 0.0
        assert resp.created_at is not None

    def test_rejects_empty_text_on_success(self) -> None:
        # A SUCCESS with no text would mislead the collector — fail loud.
        with pytest.raises(ValueError, match="non-empty"):
            Response(text="", worker_name="w", status=ResponseStatus.SUCCESS)

    def test_rejects_whitespace_only_text_on_success(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            Response(text="   ", worker_name="w", status=ResponseStatus.SUCCESS)


class TestFailedResponse:
    def test_carries_error_message(self) -> None:
        resp = Response(
            text="",
            worker_name="gemini",
            status=ResponseStatus.FAILED,
            error="rate limited",
        )

        assert resp.status is ResponseStatus.FAILED
        assert resp.error == "rate limited"
        assert resp.text == ""

    def test_supplies_default_error_when_missing(self) -> None:
        # A FAILED response should never have a None error — obscure in logs.
        resp = Response(text="", worker_name="w", status=ResponseStatus.FAILED)

        assert resp.error == "Unknown error"


class TestResponseImmutability:
    def test_is_frozen(self) -> None:
        resp = Response(text="a", worker_name="w", status=ResponseStatus.SUCCESS)

        with pytest.raises((AttributeError, Exception)):
            resp.text = "b"  # type: ignore[misc]
