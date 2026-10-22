#!/usr/bin/env python3
"""Offline planner and illustrative cost estimator for GPTQuotaPrewarm.

No network, no access to account usage, no API keys, no Codex credit conversion.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Dict, List

FIELDS = ("name", "reuse", "stability", "deliverable", "confidence", "scope_cost", "sensitivity")
WEIGHTS = {"reuse": 3, "stability": 2, "deliverable": 2, "confidence": 1,
           "scope_cost": -2, "sensitivity": -3}


def score_candidate(candidate: Dict[str, str]) -> Dict[str, object]:
    """Score candidate 1-5 scales, applying hard gates for sensitive content."""
    name = (candidate.get("name") or "").strip()
    if not name:
        raise ValueError("Candidate 'name' must be non-empty")
    values = {}
    for field in FIELDS[1:]:
        try:
            val = int(str(candidate[field]).strip())
        except (KeyError, ValueError, TypeError) as exc:
            raise ValueError(f"{name}: '{field}' must be an integer 1..5") from exc
        if not 1 <= val <= 5:
            raise ValueError(f"{name}: '{field}' must be in 1..5")
        values[field] = val
    score = sum(values[field] * weight for field, weight in WEIGHTS.items())
    if values["sensitivity"] >= 4:
        label, reason = "reject", "high sensitivity"
    elif values["reuse"] <= 1:
        label, reason = "defer", "no credible future reuse"
    elif values["stability"] <= 2:
        label, reason = "defer", "unstable context"
    elif values["deliverable"] <= 2:
        label, reason = "defer", "weak durable outcome"
    elif score >= 24:
        label, reason = "pilot", "promising bounded pilot"
    else:
        label, reason = "defer", "benefit insufficient or uncertain"
    return {"name": name, "score": score, "decision": label, "reason": reason, **values}


def rank_file(path: Path) -> List[Dict[str, object]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        missing = set(FIELDS) - set(reader.fieldnames or ())
        if missing:
            raise ValueError("CSV missing columns: " + ", ".join(sorted(missing)))
        rows = [score_candidate(row) for row in reader]
    return sorted(rows, key=lambda row: (row["decision"] == "pilot", row["score"]), reverse=True)


def estimate(prefix_tokens: int, future_reuses: int, hit_probability: float,
             cached_read_ratio: float, write_ratio: float,
             overhead_units: float = 0) -> Dict[str, object]:
    """Illustrative input-cost units, *not* subscription credits."""
    if prefix_tokens < 1:
        raise ValueError("prefix_tokens must be >= 1")
    if future_reuses < 0:
        raise ValueError("future_reuses must be >= 0")
    for name, value in (("hit_probability", hit_probability),
                        ("cached_read_ratio", cached_read_ratio)):
        if not math.isfinite(value) or not (0 <= value <= 1):
            raise ValueError(f"{name} must be between 0 and 1")
    for name, value in (("write_ratio", write_ratio), ("overhead_units", overhead_units)):
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be non-negative and finite")
    gross = future_reuses * hit_probability * prefix_tokens * (1 - cached_read_ratio)
    seed = prefix_tokens * write_ratio + overhead_units
    net = gross - seed
    denom = hit_probability * prefix_tokens * (1 - cached_read_ratio)
    breakeven = math.inf if denom == 0 else seed / denom
    return {
        "future_gross_saved_input_units": round(gross, 2),
        "prewarm_input_equivalent_units": round(seed, 2),
        "lifetime_net_input_units": round(net, 2),
        "minimum_expected_future_uses_to_break_even": (
            None if math.isinf(breakeven) else math.floor(breakeven) + 1),
        "unit": "illustrative uncached-input equivalent tokens (NOT subscription credits)",
        "limitations": "Excludes model output, reasoning, tools, latency, actual cache policy and artifact value except user-supplied overhead.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    rank = sub.add_parser("rank", help="Rank future-work candidates from a CSV")
    rank.add_argument("csv_path", type=Path)
    rank.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    est = sub.add_parser("estimate", help="Estimate hypothetical cache ROI")
    est.add_argument("--prefix-tokens", required=True, type=int)
    est.add_argument("--future-reuses", required=True, type=int)
    est.add_argument("--hit-probability", required=True, type=float)
    est.add_argument("--cached-read-ratio", required=True, type=float)
    est.add_argument("--write-ratio", required=True, type=float)
    est.add_argument("--overhead-units", default=0, type=float)
    args = parser.parse_args()
    try:
        if args.command == "rank":
            rows = rank_file(args.csv_path)
            if args.json:
                print(json.dumps(rows, indent=2, ensure_ascii=False))
            else:
                print(f"{'score':>6}  {'decision':<9} {'candidate'}")
                print("-" * 75)
                for row in rows:
                    print(f"{row['score']:>6}  {row['decision']:<9} {row['name']} ({row['reason']})")
        else:
            values = estimate(args.prefix_tokens, args.future_reuses,
                              args.hit_probability, args.cached_read_ratio,
                              args.write_ratio, args.overhead_units)
            print(json.dumps(values, indent=2, ensure_ascii=False))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
