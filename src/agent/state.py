"""
State schema for the agent.
"""
from __future__ import annotations

import operator
from typing import Annotated, Literal, TypedDict


# This 'TypedDict' defines the shape of our agent's memory.
# It ensures every part of the program knows exactly what information
# is available to read or write.
class AgentState(TypedDict):
    """Shared state flowing through the graph.

    Fields without Annotated use default overwrite semantics (last writer wins).
    Fields with Annotated[..., reducer] use the reducer to merge updates.
    """

    # 1. The Starting Question
    # This stores the user's original input. It is usually set once at
    # the start and stays the same throughout the entire process.
    question: str

    # 2. The Classification (Last-Writer-Wins)
    # This stores whether the query is 'technical' or 'casual'.
    # Because it is NOT 'Annotated', if multiple nodes write to this,
    # the newest value simply replaces the old one.
    category: Literal["technical", "casual", "unknown"]

    # 3. Accumulated Keywords (The 'Append' Rule)
    # 'Annotated' with 'operator.add' tells LangGraph: "Don't delete old data."
    # If Node A finds ['Python'] and Node B finds ['API'], the final
    # list automatically becomes ['Python', 'API'].
    keywords: Annotated[list[str], operator.add]

    # 4. The Final Answer
    # This is the empty slot that the 'responder' node will eventually
    # fill with the actual text response meant for the user.
    response: str

    # 5. The Audit Trail (Debugging Log)
    # Similar to keywords, this uses 'operator.add' to keep a running history.
    # Every node adds a "breadcrumb" here so you can see exactly how
    # the agent arrived at its final answer.
    trace: Annotated[list[str], operator.add]