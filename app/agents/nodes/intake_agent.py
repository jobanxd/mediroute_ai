"""Intake agent node for extracting patient information."""
import logging
import json

from agents.state import AgentState
from langchain_core.messages import AIMessage

from agents.prompts import intake_agent_prompts as ia_prompts
from utils.llm_util import call_llm

logger = logging.getLogger(__name__)


async def intake_agent_node(state: AgentState) -> AgentState:
    """
    Intake agent node — single pass extraction of patient info into structured JSON.
    """
    logger.info("="*30)
    logger.info("Intake Agent Node")
    logger.info("="*30)

    past_messages = state["messages"]

    # Build messages for LLM call
    messages = [
        {"role": "system", "content": ia_prompts.INTAKE_AGENT_PROMPT}
    ]

    for msg in past_messages:
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        content = msg.content
        messages.append({"role": role, "content": content})

    logger.info(f"Calling LLM with messages: {json.dumps(messages, indent=2)}")

    response = await call_llm(
        messages=messages,
    )

    logger.info(f"LLM response: {response}")

    # Parse JSON response
    message = response.choices[0].message
    raw_content = message.content or ""

    try:
        extracted = json.loads(raw_content)
        logger.info(f"Extracted intake data: {json.dumps(extracted, indent=2)}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse intake JSON: {e} | Raw: {raw_content}")
        extracted = {
            "symptoms": "unknown",
            "emergency_type": "GENERAL",
            "location": "unknown",
            "insurance_provider": "unknown"
        }

    # Store as stringified JSON in the message so match_agent can parse it
    return {
        "messages": [AIMessage(content=json.dumps(extracted), name="intake_agent")],
        "next_agent": "match_agent"
    }
