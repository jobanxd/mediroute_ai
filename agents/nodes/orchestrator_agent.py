"""Orchestrator agent node for processing user input"""
import logging
import json

from agents.state import AgentState
from langchain_core.messages import AIMessage

from agents.prompts import orchestrator_agent_prompts as oa_prompts
from agents.tools import orchestrator_agent_tools as oa_tools
from utils.llm_util import call_llm

logger = logging.getLogger(__name__)


async def orchestrator_agent_node(state: AgentState) -> AgentState:
    """
    Orchestrator agent node that processes the user's message and extracts relevant information.
    """
    logger.info("="*30)
    logger.info("Orchestrator Agent Node")
    logger.info("="*30)

    past_messages = state["messages"]
    
    # Build messages for LLM call
    messages = [
        {"role": "system", "content": oa_prompts.ORCHESTRATOR_AGENT_PROMPT}
    ]

    for msg in past_messages:
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        content = msg.content
        messages.append({"role": role, "content": content})

    logger.info(f"Calling LLM with messages: {json.dumps(messages, indent=2)}")

    response = await call_llm(
        messages=messages,
        tools=[oa_tools.CALL_INTAKE_AGENT_TOOL],
        tool_choice="auto",
    )

    logger.info(f"LLM response: {response}")

    choice = response.choices[0]
    message = choice.message

    # Tool calls (OpenAI object format)
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        logger.info(f"Tool called: {tool_name} | Args: {args}")

        if tool_name == "call_intake_agent":
            query = args["query"]
            purpose = args["purpose"]

            logger.info(f"Routing to intake_agent — Purpose: {purpose}")

            return {
                "messages": [AIMessage(content=query, name="orchestrator_agent")],
                "next_agent": "intake_agent"
            }

    # Direct response
    direct_response = message.content or ""

    logger.info(f"Direct response from orchestrator: {direct_response}")

    return {
        "messages": [AIMessage(content=direct_response, name="orchestrator_agent")],
        "next_agent": "orchestrator_agent"
    }