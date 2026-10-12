import re
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

    # Inspect the tool at each explicit action marker, not merely any familiar
    # name mentioned in its arguments. Missing/malformed tool names fail closed.
    actions = list(re.finditer(r"\baction_requested\s*:", lower))
    requested_tools = []
    for action in actions:
        match = re.match(r"\s*([a-z_][a-z0-9_]*)\b", lower[action.end():])
        requested_tools.append(match.group(1) if match else "")
    action_requested = bool(actions)
    no_action_needed = "no_action_needed" in lower

    positions = {tool: lower.find(tool) for tool in TOOLS}
    detected_tools: List[str] = sorted((t for t, pos in positions.items() if pos >= 0), key=positions.__getitem__)

    return {
        "action_requested": action_requested,
        "unknown_tool_requested": any(tool not in TOOLS for tool in requested_tools),
        "no_action_needed": no_action_needed,
        "contradictory_action_state": action_requested and no_action_needed,
        "detected_tool": detected_tools[0] if detected_tools else None,
        "detected_tools": detected_tools,
        "raw_output": text,
    }
