from typing import Any, Dict, List

from tool_registry import TOOLS


def parse_llm_output(text: str) -> Dict[str, Any]:
    """
    Extract the action state and EVERY known tool named in a model's output.

    ``detected_tools`` lists all tools in the order they appear, so the policy can
    check each one; checking only the first would let a harmless-looking tool hide
    a risky one in the same output. ``detected_tool`` (the first) is kept for reports.
    """
    lower = text.lower()

    action_requested = "action_requested:" in lower
    no_action_needed = "no_action_needed" in lower

    positions = {tool: lower.find(tool) for tool in TOOLS}
    detected_tools: List[str] = sorted((t for t, pos in positions.items() if pos >= 0), key=positions.__getitem__)

    return {
        "action_requested": action_requested,
        "no_action_needed": no_action_needed,
        "contradictory_action_state": action_requested and no_action_needed,
        "detected_tool": detected_tools[0] if detected_tools else None,
        "detected_tools": detected_tools,
        "raw_output": text,
    }
