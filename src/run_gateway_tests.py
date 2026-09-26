import json
from pathlib import Path

from gateway import gateway_decision
from report_generator import save_results

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_PATH = ROOT / "scenarios" / "gateway_test_cases.json"

def main():
    scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    results = []

    for scenario in scenarios:
        print(f"Testing {scenario['id']} - {scenario['title']}")
        result = gateway_decision(scenario)
        results.append(result)

    save_results(results)

    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    print(f"Passed {passed}/{total} gateway tests.")
    return 0 if passed == total else 1

if __name__ == "__main__":
    raise SystemExit(main())
