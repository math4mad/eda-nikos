#!/usr/bin/env python3
"""Create a small, dependency-free EDA report from Irene's sample data."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "research-irene" / "data" / "papers.csv"
REPORT = ROOT / "eda-nikos" / "reports" / "sample-study.json"
FIGURE = ROOT / "eda-nikos" / "figures" / "citations-by-year.svg"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8", newline="")))
    by_year: Counter[str] = Counter()
    by_topic: Counter[str] = Counter()
    for row in rows:
        by_year[row["year"]] += int(row["citations"])
        by_topic[row["topic"]] += 1

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    FIGURE.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({
        "input": str(INPUT.relative_to(ROOT)),
        "input_sha256": sha256(INPUT),
        "rows": len(rows),
        "citations_by_year": dict(sorted(by_year.items())),
        "papers_by_topic": dict(sorted(by_topic.items())),
    }, indent=2) + "\n", encoding="utf-8")

    max_value = max(by_year.values(), default=1)
    bars = []
    for index, (year, value) in enumerate(sorted(by_year.items())):
        width = round(420 * value / max_value)
        y = 34 + index * 38
        bars.append(f'<text x="10" y="{y + 16}" font-size="14">{year}</text>')
        bars.append(f'<rect x="62" y="{y}" width="{width}" height="22" fill="#c75b45"/>')
        bars.append(f'<text x="{70 + width}" y="{y + 16}" font-size="14">{value}</text>')
    FIGURE.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="560" height="180" '
        'viewBox="0 0 560 180"><rect width="100%" height="100%" fill="#f5f1e8"/>'
        '<text x="10" y="20" font-family="Georgia" font-size="16" fill="#164b63">Citations by year</text>'
        + "".join(bars) + "</svg>\n",
        encoding="utf-8",
    )
    print(f"EDA PASSED: {len(rows)} rows -> {REPORT.relative_to(ROOT)} and {FIGURE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()