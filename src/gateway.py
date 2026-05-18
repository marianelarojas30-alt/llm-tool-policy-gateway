from typing import Dict, Any

from action_parser import parse_llm_output
from policy_engine import evaluate_policy

def gateway_decision(scenario: Dict[str, Any]) -> Dict[str, Any]:
    parsed = parse_llm_output(scenario["llm_output"])
    policy_result = evaluate_policy(parsed, scenario)

    return {
        "scenario_id": scenario["id"],
        "title": scenario["title"],
        "expected_decision": scenario["expected_decision"],
        "actual_decision": policy_result["decision"],
        "passed": policy_result["decision"] == scenario["expected_decision"],
        "detected_tool": policy_result["detected_tool"],
        "contradictory_action_state": policy_result["contradictory_action_state"],
        "triggered_rules": policy_result["triggered_rules"],
        "llm_output": scenario["llm_output"],
    }
