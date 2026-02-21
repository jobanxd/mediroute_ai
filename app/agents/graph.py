"""MediRoute AI - LangGraph Graph Definition"""
from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentState
from app.agents.nodes.orchestrator_agent import orchestrator_agent_node
from app.agents.nodes.intake_agent import intake_agent_node
from app.agents.nodes.match_agent import match_agent_node
from app.agents.nodes.response_agent import response_agent_node


async def _get_routing_decision(state: AgentState) -> str:
    """Reads next_agent from state to determine routing."""
    return state["next_agent"]

# ── Build Graph ────────────────────────────────────────────────
builder = StateGraph(AgentState)

# ── Nodes ────────────────────────────────────────────────
builder.add_node("orchestrator_agent", orchestrator_agent_node)
builder.add_node("intake_agent", intake_agent_node)
builder.add_node("match_agent", match_agent_node)
builder.add_node("response_agent", response_agent_node)

# ── Edges ────────────────────────────────────────────────
builder.add_edge(START, "orchestrator_agent")

# After each sub-agent completes, flow goes forward (not back to orchestrator)
builder.add_edge("intake_agent", "match_agent")
builder.add_edge("match_agent", "response_agent")
builder.add_edge("response_agent", END)

# Orchestrator either answers directly (FINISH) or routes to intake
builder.add_conditional_edges(
    "orchestrator_agent",
    _get_routing_decision,
    {
        "orchestrator_agent": END,   # direct answer, no emergency detected
        "intake_agent": "intake_agent"
    }
)

graph = builder.compile()
