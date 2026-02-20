"""Chat Service for MediRoute AI."""
import logging

from typing import Dict, List
from langchain_core.messages import HumanMessage, AIMessage

from agents.graph import graph

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.sessions: Dict[str, List] = {}

    async def process_message(
            self,
            session_id: str,
            user_input: str,
    ) -> Dict:
        """Process user message and return response."""
        
        # Get or create session
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            logger.info(f"NEW SESSION | Session: {session_id}")
        else:
            logger.info(f"CONTINUING SESSION | Session: {session_id}")

        # Append user message to session history
        user_message = HumanMessage(content=user_input)
        self.sessions[session_id].append(user_message)

        logger.info(f"USER: {user_input}")
        logger.info(f"Total messages in session: {len(self.sessions[session_id])}")


        # Invoke Graph
        final_state = await graph.ainvoke(
            {"messages": self.sessions[session_id]},
        )

        final_messages = final_state.get("messages", [])

        # Append new messages to session (avoid duplicates)
        for msg in final_messages:
            if msg not in self.sessions[session_id]:
                self.sessions[session_id].append(msg)

        # Get last AI message
        ai_message = None
        for msg in reversed(final_messages):
            if isinstance(msg, AIMessage):
                ai_message = msg
                break

        if not ai_message:
            logger.warning("No AI message found in final state.")
            return {
                "session_id": session_id,
                "response": "Something went wrong. Please try again.",
                "next_agent": final_state.get("next_agent", "unknown")
            }

        logger.info(f"AI RESPONSE: {ai_message.content}")

        return {
            "session_id": session_id,
            "response": ai_message.content,
            "next_agent": final_state.get("next_agent", "unknown"),
            "agent_name": ai_message.name if hasattr(ai_message, "name") else None
        }

# Singleton
chat_service = ChatService()