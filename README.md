# LLM Tool Policy Gateway

A defensive policy gateway that blocks unsafe, contradictory, or unauthorized LLM tool-use requests before connected actions execute.

## Why this exists

In the companion project `llm-connection-safety-scanner`, we found an important failure pattern:

> A model may say `ACTION_REQUESTED` and `NO_ACTION_NEEDED` in the same response.

That is a trust-boundary problem. Even when a model appears to recognize risk, it may still produce a tool-use signal.

The fix is not to trust the model more. The fix is to place a deterministic policy gateway between the model and any connected tool.

## What this repo does

This repo simulates a safety gateway that reviews proposed LLM tool actions and decides:

- allow
- block
- require user confirmation
- quarantine for human review

It does not send real emails, delete files, call webhooks, write memory, or access real APIs.

Everything is simulated and defensive.

## Core idea

```text
LLM output -> Tool Policy Gateway -> Decision -> Simulated tool allowed or blocked
```

The gateway blocks actions when it sees:

- contradictory state: `ACTION_REQUESTED` and `NO_ACTION_NEEDED`
- untrusted content trying to trigger tools
- protected content exposure
- missing user confirmation
- fake authority instructions
- memory-write requests from untrusted content
- external data exfiltration patterns
- unsafe webhook/API calls

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_gateway_tests.py
```

## Output

Reports are saved to:

```text
reports/latest_gateway_report.md
results/gateway_results.json
results/gateway_results.csv
```

## Repository structure

```text
llm-tool-safety-gateway/
├── README.md
├── requirements.txt
├── policies/
│   └── gateway_policy.json
├── scenarios/
│   └── gateway_test_cases.json
├── src/
│   ├── run_gateway_tests.py
│   ├── gateway.py
│   ├── action_parser.py
│   ├── policy_engine.py
│   ├── simulated_tools.py
│   └── report_generator.py
├── reports/
│   └── sample_report.md
└── results/
    └── .gitkeep
```

## Research question

Can a deterministic policy gateway reduce unsafe connected-LLM behavior by blocking contradictory or untrusted tool-use requests before execution?

## Defensive use only

This project is for defensive AI security research and safe tool-use policy design. It does not perform real actions or interact with real systems.


## What this is, and what it is not

This project is a **policy gateway**, not an autonomous agent.

It does not independently plan, monitor live systems, or adapt its own behavior. It deterministically reviews proposed LLM tool-use text and applies policy rules before simulated execution.

That makes the project narrower, safer, and more honest.
