from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import json
import csv

ROOT = Path(__file__).resolve().parents[1]

def save_results(results: List[Dict[str, Any]]) -> None:
    results_dir = ROOT / "results"
    reports_dir = ROOT / "reports"
    results_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    json_path = results_dir / "gateway_results.json"
    csv_path = results_dir / "gateway_results.csv"
    report_path = reports_dir / "latest_gateway_report.md"

    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    fieldnames = [
        "scenario_id",
        "title",
        "expected_decision",
        "actual_decision",
        "passed",
        "detected_tool",
        "contradictory_action_state",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({key: row.get(key) for key in fieldnames})

    lines = []
    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    lines.append("# LLM Tool Safety Gateway Report")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total scenarios: {total}")
    lines.append(f"- Passed: {passed}")
    lines.append(f"- Failed: {total - passed}")
    lines.append("")
    lines.append("## Results")
    lines.append("")

    for r in results:
        lines.append(f"### {r['scenario_id']} - {r['title']}")
        lines.append("")
        lines.append(f"- Expected decision: {r['expected_decision']}")
        lines.append(f"- Actual decision: {r['actual_decision']}")
        lines.append(f"- Passed: {r['passed']}")
        lines.append(f"- Detected tool: {r['detected_tool']}")
        lines.append(f"- Contradictory action state: {r['contradictory_action_state']}")
        lines.append("")
        lines.append("Triggered rules:")
        if r["triggered_rules"]:
            for rule in r["triggered_rules"]:
                lines.append(f"- {rule['id']} {rule['name']}: {rule['reason']}")
        else:
            lines.append("- None")
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Saved JSON results to {json_path}")
    print(f"Saved CSV results to {csv_path}")
    print(f"Saved Markdown report to {report_path}")
