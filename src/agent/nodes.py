"""
Node functions — Ollama variant.
"""
from __future__ import annotations

from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from .state import AgentState


# This is a 'Factory'—it's like a machine that builds a specific worker (the analyzer)
# and gives that worker a tool (the local Ollama LLM).
def make_analyzer(llm: ChatOllama):
    """Factory: returns an analyzer node bound to the given LLM."""

    # This is the actual function that runs when the graph hits the 'analyzer' station.
    def analyzer_node(state: AgentState) -> dict:
        # Step 1: Look at the shared memory (State) to see what the user asked.
        question = state["question"]

        # Step 2: Give the AI strict instructions (System Message).
        # We tell it to act like a classifier and use a specific, rigid format.
        system = SystemMessage(content=(
            "You are a classifier. Respond in EXACTLY this format:\n"
            "CATEGORY: <technical|casual>\n"
            "KEYWORDS: <comma-separated list of 2-4 key terms>\n"
            "Nothing else."
        ))

        # Step 3: Ask the LLM to process the question based on our instructions.
        result = llm.invoke([system, HumanMessage(content=question)])
        text = str(result.content).strip()

        # Step 4: Parse the AI's response.
        # Since LLMs can be chatty, we manually loop through the lines of text
        # to find our CATEGORY and KEYWORDS to make them 'computer-readable'.
        category: Literal["technical", "casual", "unknown"] = "unknown"
        keywords: list[str] = []
        for line in text.splitlines():
            if line.upper().startswith("CATEGORY:"):
                val = line.split(":", 1)[1].strip().lower()
                if val in ("technical", "casual"):
                    category = val  # type: ignore[assignment]
            elif line.upper().startswith("KEYWORDS:"):
                raw = line.split(":", 1)[1].strip()
                keywords = [k.strip() for k in raw.split(",") if k.strip()]

        # Step 5: Update the Shared Memory.
        # We return a dictionary that LangGraph will merge into the main 'AgentState'.
        # We also add a 'trace' so we can look back and see what happened at this step.
        return {
            "category": category,
            "keywords": keywords,
            "trace": [f"analyzer: category={category}, keywords={keywords}"],
        }

    return analyzer_node


# This builds the 'responder' worker.
def make_responder(llm: ChatOllama):
    """Factory: returns a responder node bound to the given LLM."""

    # This function runs when the graph moves to the 'responder' station.
    def responder_node(state: AgentState) -> dict:
        # Step 1: Read the latest info from memory.
        # Notice how it can see the 'category' and 'keywords' the analyzer just found!
        question = state["question"]
        category = state["category"]
        keywords = state["keywords"]

        # Step 2: Dynamic Persona Selection.
        # This is where the magic happens. We change how the AI acts based on the
        # category found in the previous step.
        if category == "technical":
            style = (
                "Answer as a senior engineer. Be precise, use correct terminology, "
                "and include a short code example if relevant."
            )
        elif category == "casual":
            style = "Answer conversationally and warmly. Keep it short."
        else:
            style = "Answer helpfully and concisely."

        # Step 3: Prepare the final instructions.
        system = SystemMessage(content=(
            f"{style}\n"
            f"Relevant keywords: {', '.join(keywords) or 'none'}."
        ))

        # Step 4: Generate the final answer for the user.
        result = llm.invoke([system, HumanMessage(content=question)])

        # Step 5: Final update to memory.
        # We save the actual 'response' and add another log to our 'trace'.
        return {
            "response": str(result.content),
            "trace": [f"responder: generated {len(str(result.content))} chars"],
        }

    return responder_node