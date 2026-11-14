"""Command-line interface for VulnLab-RL."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import SCENARIOS, list_scenarios, score_submission


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic AI security-evaluation benchmark")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("demo", help="print available synthetic scenarios")
    score_parser = subparsers.add_parser("score", help="score a JSON agent submission")
    score_parser.add_argument("submission", type=Path)
    args = parser.parse_args()

    if args.command == "demo":
        print(json.dumps(list_scenarios(), indent=2))
        return

    submission = json.loads(args.submission.read_text(encoding="utf-8"))
    print(json.dumps(score_submission(submission), indent=2))


if __name__ == "__main__":
    main()
