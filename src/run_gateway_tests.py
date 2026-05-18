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
    print(f"Passed {passed}/{len(results)} gateway tests.")

if __name__ == "__main__":
    main()
