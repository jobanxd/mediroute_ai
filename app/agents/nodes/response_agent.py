"""Response agent node — delivers empathetic hospital recommendation to the patient."""
import logging
import json

from langchain_core.messages import AIMessage

from app.agents.state import AgentState
from app.agents.prompts import response_agent_prompts as ra_prompts
from app.utils.llm_util import call_llm

logger = logging.getLogger(__name__)


async def response_agent_node(state: AgentState) -> AgentState:
    """
    Response agent node — takes match results and generates
    a warm, human-readable recommendation for the patient.
    """
    logger.info("="*30)
    logger.info("Response Agent Node")
    logger.info("="*30)

    # Parse match agent output from last message
    last_message = state["messages"][-1]
    try:
        match_data = json.loads(last_message.content)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse match data: %s", e)
        return {
            "messages": [AIMessage(
                content=("I'm sorry, I encountered an issue finding hospitals. "
                         "Please call 911 immediately for emergency assistance."),
                name="response_agent"
            )],
            "next_agent": "END"
        }

    intake_data = match_data.get("intake_data", {})
    matches = match_data.get("matches", [])
    no_match_reason = match_data.get("no_match_reason", None)

    # Build the user message to send to LLM
    if no_match_reason:
        user_content = f"""
The patient has the following emergency:
- Symptoms: {intake_data.get('symptoms', 'unknown')}
- Emergency Type: {intake_data.get('emergency_type', 'GENERAL')}
- Location: {intake_data.get('location', 'unknown')}
- Insurance Provider: {intake_data.get('insurance_provider', 'unknown')}

Unfortunately, no matching hospitals were found.
Reason: {no_match_reason}

Please respond to the patient with empathy and advise them to call 911 immediately.
"""
    else:
        # Format hospital matches clearly for the LLM
        hospitals_text = ""
        for match in matches:
            caps = match.get("capabilities", {})
            available_caps = [cap.replace("_", " ").title() for cap, val in caps.items() if val]
            hospitals_text += f"""
Rank {match['rank']}:
- Name: {match['name']}
- Address: {match['address']}
- Distance: {match['distance_km']} km from patient
- Emergency Contact: {match['emergency_contact']}
- Available Capabilities: {', '.join(available_caps)}
"""

        user_content = f"""
The patient has the following emergency:
- Symptoms: {intake_data.get('symptoms', 'unknown')}
- Emergency Type: {intake_data.get('emergency_type', 'GENERAL')}
- Location: {intake_data.get('location', 'unknown')}
- Insurance Provider: {intake_data.get('insurance_provider', 'unknown')}

Matched hospitals ranked by distance and capability:
{hospitals_text}

Please deliver the hospital recommendation to the patient in a warm, empathetic, and clear way.
"""

    logger.info("Calling LLM with user content: %s", user_content)

    messages = [
        {"role": "system", "content": ra_prompts.RESPONSE_AGENT_PROMPT},
        {"role": "user", "content": user_content}
    ]

    response = await call_llm(
        messages=messages,
    )

    try:
        message = response.choices[0].message
        final_response = (message.content or
                          "I'm sorry, something went wrong. Please call 911 immediately.")
    except (AttributeError, IndexError):
        logger.error("Malformed LLM response structure.")
        final_response = "I'm sorry, something went wrong. Please call 911 immediately."

    logger.info("LLM Response: %s", final_response)

    return {
        "messages": [
            AIMessage(content=final_response, name="response_agent")
        ],
        "next_agent": "END"
    }
