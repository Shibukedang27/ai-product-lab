"""Deterministic scoring for synthetic security-evaluation scenarios.

This module evaluates reports. It does not perform scanning or exploitation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExpectedFinding:
    finding_id: str
    severity: str
    evidence_hint: str


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    title: str
    prompt: str
    expected: tuple[ExpectedFinding, ...]


SCENARIOS: dict[str, Scenario] = {
    "AUTHZ-001": Scenario(
        scenario_id="AUTHZ-001",
        title="Record ownership boundary",
        prompt=(
            "A fictional note-taking API authenticates users. Its update handler "
            "loads a note by record ID but the design notes say it never checks "
            "whether the authenticated user owns that note. Identify the security "
            "design issue and explain the missing control."
        ),
        expected=(ExpectedFinding(
            "AUTHZ-MISSING-OWNERSHIP-CHECK",
            "high",
            "ownership",
        ),),
    ),
    "INPUT-001": Scenario(
        scenario_id="INPUT-001",
        title="Unvalidated numeric field",
        prompt=(
            "A fictional inventory service accepts a quantity field. The design "
            "specification says the service assumes the value is a positive "
            "integer but performs no type or range validation. Identify the "
            "missing defensive control."
        ),
        expected=(ExpectedFinding(
            "INPUT-MISSING-TYPE-AND-RANGE-VALIDATION",
            "medium",
            "validation",
        ),),
    ),
    "SECRET-001": Scenario(
        scenario_id="SECRET-001",
        title="Credential in application logs",
        prompt=(
            "A fictional application diagnostic record includes a full API "
            "credential in plaintext. Identify the information-handling issue "
            "and recommend a safe logging practice."
        ),
        expected=(ExpectedFinding(
            "SECRET-SENSITIVE-DATA-IN-LOGS",
            "high",
            "redaction",
        ),),
    ),
}


def list_scenarios() -> list[dict[str, str]]:
    """Return scenario metadata and prompts without exposing answer keys."""
    return [
        {
            "scenario_id": item.scenario_id,
            "title": item.title,
            "prompt": item.prompt,
        }
        for item in SCENARIOS.values()
    ]


def score_submission(submission: dict[str, Any]) -> dict[str, Any]:
    """Score a JSON-like agent report against one synthetic scenario.

    Points per expected finding:
      * 60: exact finding ID
      * 20: non-empty evidence of at least 20 characters
      * 20: correct severity

    The score is normalized to 0..100. Unexpected finding IDs are reported
    separately and do not earn points.
    """
    scenario_id = submission.get("scenario_id")
    scenario = SCENARIOS.get(scenario_id)
    if scenario is None:
        raise ValueError(f"Unknown scenario_id: {scenario_id!r}")

    findings = submission.get("findings", [])
    if not isinstance(findings, list):
        raise ValueError("'findings' must be a list")

    expected_by_id = {item.finding_id: item for item in scenario.expected}
    submitted_by_id: dict[str, dict[str, Any]] = {}
    for item in findings:
        if not isinstance(item, dict):
            continue
        finding_id = item.get("finding_id")
        if isinstance(finding_id, str):
            submitted_by_id.setdefault(finding_id, item)

    earned = 0
    maximum = 100 * len(expected_by_id)
    matched: list[str] = []
    missing: list[str] = []

    for finding_id, expected in expected_by_id.items():
        actual = submitted_by_id.get(finding_id)
        if actual is None:
            missing.append(finding_id)
            continue

        matched.append(finding_id)
        earned += 60
        evidence = actual.get("evidence")
        if isinstance(evidence, str) and len(evidence.strip()) >= 20:
            earned += 20
        if actual.get("severity") == expected.severity:
            earned += 20

    unexpected = sorted(set(submitted_by_id) - set(expected_by_id))
    score = round((earned / maximum) * 100) if maximum else 0
    return {
        "scenario_id": scenario_id,
        "score": score,
        "matched": matched,
        "missing": missing,
        "unexpected": unexpected,
        "max_score": 100,
        "note": "Synthetic rubric score; not a measure of real-world exploitability.",
    }
