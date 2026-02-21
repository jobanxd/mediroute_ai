"""State management for Agents."""
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State of the Agents"""
    messages: Annotated[list, add_messages]
    next_agent: str
