CALL_INTAKE_AGENT_TOOL = {
    "type": "function",
    "function": {
        "name": "call_intake_agent",
        "description": (
            "Use this tool when the patient has provided their symptoms or emergency condition, "
            "their current location, and their insurance provider. "
            "This will route the request to the intake agent for structured extraction and hospital matching."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The full original message from the patient describing their emergency, location, and insurance provider."
                },
                "purpose": {
                    "type": "string",
                    "description": "Brief reason why this is being routed to the intake agent (e.g. 'Patient described cardiac symptoms with location and insurance info provided')."
                }
            },
            "required": ["query", "purpose"]
        }
    }
}