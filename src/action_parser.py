from typing import Dict, Any

def parse_llm_output(text: str) -> Dict[str, Any]:
    lower = text.lower()

    action_requested = "action_requested:" in lower
    no_action_needed = "no_action_needed" in lower

    detected_tool = None
    known_tools = [
        "send_email_simulated",
        "write_memory_simulated",
        "delete_file_simulated",
        "call_webhook_simulated",
        "read_file_simulated",
        "retrieve_context_simulated",
    ]

    for tool in known_tools:
        if tool in lower:
            detected_tool = tool
            break

    return {
        "action_requested": action_requested,
        "no_action_needed": no_action_needed,
        "contradictory_action_state": action_requested and no_action_needed,
        "detected_tool": detected_tool,
        "raw_output": text,
    }
