import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gateway import gateway_decision
from report_generator import save_results


class ToolReportTests(unittest.TestCase):
    def test_reports_keep_every_detected_tool_in_order(self):
        names = ["read_file_simulated", "retrieve_context_simulated"]
        result = gateway_decision({
            "id": "R1", "title": "Local lookups", "source_trust": "user_request",
            "expected_decision": "allow",
            "llm_output": "ACTION_REQUESTED: " + " then ".join(names),
        })
        legacy = dict(result)
        del legacy["detected_tools"]
        with tempfile.TemporaryDirectory() as tmp, patch("report_generator.ROOT", Path(tmp)):
            save_results([result, legacy])
            output = Path(tmp) / "results"
            stored = json.loads((output / "gateway_results.json").read_text())[0]
            self.assertEqual(stored["detected_tool"], names[0])
            self.assertEqual(stored["detected_tools"], names)
            with (output / "gateway_results.csv").open(newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(json.loads(rows[0]["detected_tools"]), names)
            self.assertEqual(json.loads(rows[1]["detected_tools"]), names[:1])
            report = (Path(tmp) / "reports/latest_gateway_report.md").read_text()
            self.assertIn("Detected tools: " + ", ".join(names), report)
