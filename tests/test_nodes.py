"""
Tests for node functions.

Notice these tests are IDENTICAL to the Anthropic version's tests.
Because we inject a fake LLM, the tests don't care which provider the
real code uses. This is a huge production win — you can swap providers
without rewriting your test suite.
"""
from __future__ import annotations

from dataclasses import dataclass

from agent.nodes import make_analyzer, make_responder


@dataclass
class FakeResult:
    content: str


class FakeLLM:
    def __init__(self, reply: str) -> None:
        self._reply = reply

    def invoke(self, _messages):
        return FakeResult(content=self._reply)


def test_analyzer_parses_category_and_keywords():
    fake = FakeLLM("CATEGORY: technical\nKEYWORDS: python, gil, threading")
    analyzer = make_analyzer(fake)  # type: ignore[arg-type]

    state = {
        "question": "How does the GIL work?",
        "category": "unknown",
        "keywords": [],
        "response": "",
        "trace": [],
    }
    update = analyzer(state)

    assert update["category"] == "technical"
    assert update["keywords"] == ["python", "gil", "threading"]


def test_analyzer_falls_back_to_unknown_on_malformed_output():
    fake = FakeLLM("this is not the expected format")
    analyzer = make_analyzer(fake)  # type: ignore[arg-type]

    state = {
        "question": "?",
        "category": "unknown",
        "keywords": [],
        "response": "",
        "trace": [],
    }
    update = analyzer(state)

    assert update["category"] == "unknown"
    assert update["keywords"] == []


def test_responder_produces_response_and_trace():
    fake = FakeLLM("Here is the answer.")
    responder = make_responder(fake)  # type: ignore[arg-type]

    state = {
        "question": "Hi",
        "category": "casual",
        "keywords": ["greeting"],
        "response": "",
        "trace": [],
    }
    update = responder(state)

    assert update["response"] == "Here is the answer."
    assert update["trace"][0].startswith("responder:")
