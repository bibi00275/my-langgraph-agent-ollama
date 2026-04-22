"""
CLI entry point. Run with:
    python scripts/run_agent.py "your question here"
"""
from __future__ import annotations

import sys

from agent.config import load_settings
from agent.graph import build_graph
from agent.state import AgentState


def main() -> None:
    question = (
        " ".join(sys.argv[1:])
        or "How does Python's GIL affect multi-threaded CPU-bound code?"
    )

    settings = load_settings()
    app = build_graph(settings)

    initial_state: AgentState = {
        "question": question,
        "category": "unknown",
        "keywords": [],
        "response": "",
        "trace": [],
    }
    final = app.invoke(initial_state)

    print("=" * 60)
    print("QUESTION: ", final["question"])
    print("CATEGORY: ", final["category"])
    print("KEYWORDS: ", final["keywords"])
    print("-" * 60)
    print("RESPONSE:")
    print(final["response"])
    print("-" * 60)
    print("TRACE:")
    for entry in final["trace"]:
        print("  -", entry)
    print("=" * 60)


if __name__ == "__main__":
    main()
