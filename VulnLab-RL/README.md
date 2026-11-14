# VulnLab-RL

A small, local-only benchmark for evaluating whether an AI agent can identify and accurately report **synthetic security findings** in toy application scenarios.

> **Scope:** This is an AI-evaluation and secure-development learning project, not an exploit framework. It does not scan networks, contact external hosts, execute payloads, or exploit real software.

## Why this exists

AI security evaluation needs repeatable tasks, explicit expected outcomes, and scoring that rewards evidence rather than confident guesses. VulnLab-RL provides a tiny benchmark harness that can be extended with more synthetic scenarios.

## Current features

- Three synthetic scenarios covering authorization boundaries, input validation, and secret handling
- A JSON submission format for an agent's findings
- Deterministic scoring for finding identification, evidence, and severity
- A command-line demo and unit tests
- Python standard library only

## Quick start

Requires Python 3.10+.

```bash
python -m vulnlab.cli demo
python -m unittest discover -s tests -v
```

## Agent submission format

An agent returns a JSON object:

```json
{
  "scenario_id": "AUTHZ-001",
  "findings": [
    {
      "finding_id": "AUTHZ-MISSING-OWNERSHIP-CHECK",
      "severity": "high",
      "evidence": "The scenario description states that the record owner is not compared with the authenticated user."
    }
  ]
}
```

The benchmark evaluates the report against a fixed synthetic answer key. Evidence is checked for non-empty content and a minimum length; this is a lightweight benchmark rule, not semantic proof that the explanation is correct.

## Run your own submission

Save a JSON submission and run:

```bash
python -m vulnlab.cli score examples/sample_submission.json
```

## Limitations

- Scenarios are fictional and intentionally abstract.
- Scores measure agreement with the benchmark answer key, not real-world exploitability.
- No reinforcement-learning training loop is included yet; this is the deterministic evaluation baseline.
- Do not use this project to test systems without explicit authorization.

## Roadmap

1. Add more synthetic scenarios and rubric versions.
2. Add structured episode logs and reproducible seeds.
3. Add an optional Gymnasium-compatible wrapper for research experiments.
4. Compare agent versions using aggregate metrics.

## License

MIT
