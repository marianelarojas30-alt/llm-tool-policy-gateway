import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from action_parser import parse_llm_output
from policy_engine import evaluate_policy


class PolicyBoundaryTests(unittest.TestCase):
    def decide(self, output, authorized=False):
        return evaluate_policy(parse_llm_output(output), {
            "source_trust": "user_request", "trusted_user_authorized_action": authorized,
            "protected_content": "SYNTHETIC-SECRET",
        })["decision"]

    def test_response_only_cannot_disclose_protected_content(self):
        self.assertEqual(self.decide("NO_ACTION_NEEDED: SYNTHETIC-SECRET"), "block")

    def test_string_false_does_not_authorize_external_action(self):
        for value in ("false", "true", 1, [True], {"authorized": True}):
            with self.subTest(value=value):
                self.assertEqual(self.decide("ACTION_REQUESTED: send_email_simulated", value), "require_confirmation")

    def test_unknown_tool_cannot_hide_after_known_tool(self):
        self.assertEqual(self.decide("ACTION_REQUESTED: read_file_simulated x; ACTION_REQUESTED: unregistered_tool y"), "block")

    def test_unknown_tool_cannot_borrow_known_tool_in_arguments(self):
        self.assertEqual(self.decide("ACTION_REQUESTED: unregistered_tool note=read_file_simulated"), "block")

    def test_explicit_authorization_still_works(self):
        self.assertEqual(self.decide("ACTION_REQUESTED: send_email_simulated", True), "allow")
