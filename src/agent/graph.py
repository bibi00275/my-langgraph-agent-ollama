"""
Graph assembly — Ollama variant.

Wires ChatOllama into the same 2-node graph shape as the Anthropic version.
"""
from __future__ import annotations

from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

from .config import Settings
from .nodes import make_analyzer, make_responder
from .state import AgentState


def build_graph(settings: Settings):
    """Construct, compile, and return the runnable graph."""

    # 1. Initialize the Local Brain (LLM)
    # We create a connection to Ollama using your settings.
    # This specifies which model to use (like Llama 3 or Mistral) and
    # how "creative" (temperature) the AI should be.
    llm = ChatOllama(
        model=settings.model,
        base_url=settings.base_url,
        temperature=settings.temperature,
    )

    # 2. Create the Blueprint (StateGraph)
    # We initialize a 'StateGraph' which is like a map for the AI's logic.
    # 'AgentState' is the shared memory; it ensures that what the
    # analyzer finds is available for the responder to read later.
    graph = StateGraph(AgentState)

    # 3. Add the Workers (Nodes)
    # Think of Nodes as 'stations' on an assembly line.
    # We create an "analyzer" station and a "responder" station,
    # giving both of them access to our LLM to do their jobs.
    graph.add_node("analyzer", make_analyzer(llm))
    graph.add_node("responder", make_responder(llm))

    # 4. Define the Starting Point
    # This tells the program: "The moment someone asks a question,
    # send them straight to the analyzer station."
    graph.add_edge(START, "analyzer")

    # 5. Connect the Stations (Edges)
    # This creates the flow: Once the "analyzer" is finished with its work,
    # the data automatically moves forward to the "responder" station.
    graph.add_edge("analyzer", "responder")

    # 6. Define the Exit Point
    # This tells the program that once the "responder" has finished
    # writing the answer, the process is complete.
    graph.add_edge("responder", END)

    # 7. Finalize and Build (Compile)
    # This turns our map and logic into a single 'runnable' object.
    # It's like taking a blueprint and finally opening the factory doors.
    return graph.compile()