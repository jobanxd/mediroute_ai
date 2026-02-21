"""Models for chat request and response."""
from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request model for chat interactions."""
    session_id: str
    user_input: str


class ChatResponse(BaseModel):
    """Response model for chat interactions."""
    session_id: str
    response: str
    agent_name: Optional[str] = None
    next_agent: Optional[str] = None
