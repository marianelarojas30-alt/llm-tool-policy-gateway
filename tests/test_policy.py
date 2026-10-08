import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from action_parser import parse_llm_output  # noqa: E402
from gateway import gateway_decision  # noqa: E402
from tool_registry import TOOLS  # noqa: E402


def scenario(llm_output, trust="user_request", authorized=False, protected=""):
    return {"id": "T", "title": "t", "expected_decision": "", "llm_output": llm_output,
            "source_trust": trust, "trusted_user_authorized_action": authorized, "protected_content": protected}


class ParserTests(unittest.TestCase):
    def test_finds_every_tool_in_order_of_appearance(self):
        p = parse_llm_output("ACTION_REQUESTED: read_file_simulated a; then send_email_simulated b")
        self.assertEqual(p["detected_tools"], ["read_file_simulated", "send_email_simulated"])
        self.assertEqual(p["detected_tool"], "read_file_simulated")

    def test_parser_and_policy_share_one_tool_list(self):
        for tool in TOOLS:
            self.assertEqual(parse_llm_output(f"ACTION_REQUESTED: {tool}")["detected_tools"], [tool])


class PolicyTests(unittest.TestCase):
    def test_risky_tool_cannot_hide_behind_harmless_one(self):
        out = "ACTION_REQUESTED: write_memory_simulated x, then delete_file_simulated /important.txt"
        self.assertEqual(gateway_decision(scenario(out))["actual_decision"], "require_confirmation")

    def test_block_beats_confirmation_across_tools(self):
        out = "ACTION_REQUESTED: send_email_simulated a, call_webhook_simulated https://x"
        r = gateway_decision(scenario(out, trust="retrieved_document"))
        self.assertEqual(r["actual_decision"], "block")

    def test_single_tools_keep_previous_decisions(self):
        cases = [
            ("ACTION_REQUESTED: delete_file_simulated /a", "user_request", False, "require_confirmation"),
            ("ACTION_REQUESTED: send_email_simulated to=a", "user_request", True, "allow"),
            ("ACTION_REQUESTED: read_file_simulated a", "retrieved_document", False, "block"),
            ("ACTION_REQUESTED: write_memory_simulated a", "retrieved_document", False, "block"),
            ("Just answering, NO_ACTION_NEEDED", "user_request", False, "allow_response_only"),
            ("ACTION_REQUESTED: launch_rocket", "user_request", False, "block"),
        ]
        for out, trust, auth, expected in cases:
            with self.subTest(out=out):
                self.assertEqual(gateway_decision(scenario(out, trust, auth))["actual_decision"], expected)

    def test_rules_are_not_duplicated_for_repeated_tools(self):
        out = "ACTION_REQUESTED: delete_file_simulated a and delete_file_simulated b"
        ids = [r["id"] for r in gateway_decision(scenario(out))["triggered_rules"]]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
