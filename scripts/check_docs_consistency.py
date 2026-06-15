from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, List


EXPECTED_PACKAGES = {
    "Longform Research Report": [
        "Research Scope",
        "Topic Decision",
        "Query Log",
        "Source Capture Status",
        "Market / Player Demand Signals",
        "Chapter Plan",
        "Chapter Research Cards",
        "Source Evidence Table",
        "Original Text / Transcript Index",
        "Risks / Unknowns",
        "Need In-Game Verification",
        "Suggested Next Research",
    ],
    "Topic Brief": [
        "Inputs",
        "Query Log",
        "Market Signals",
        "Community / Forum Signals",
        "Cross-Language Competitor Hits",
        "Cross-Source Validation",
        "Chinese Audience Fit",
        "5 Topic Options",
        "Top 1 Recommendation",
        "Why Now",
        "Risks / Unknowns",
    ],
    "Title Pack": [
        "Topic",
        "Historical Data Baseline",
        "Thumbnail Data Baseline",
        "Comparable Title Anchors",
        "Top 3",
        "ABC Title + Thumbnail Text Tests",
        "10 Candidate Titles",
        "Title Scorecard",
        "Data-Based Click Hypothesis",
        "Angle Notes",
        "3 Thumbnail Copy Options",
        "3 Thumbnail Composition Directions",
        "Final Title + Thumbnail Pair",
        "Retro Fields",
    ],
    "Script Package": [
        "Outline",
        "Full Draft",
        "Fact Check Notes",
    ],
    "Shorts Package": [
        "Hook Title",
        "Hook Burst Text",
        "Template Marked Script",
    ],
    "Shorts Topic Pack": [
        "Inputs",
        "Query Log",
        "Platform Signals",
        "Comment / Community Signals",
        "Cross-Language Shorts Hits",
        "Cross-Platform Validation",
        "Chinese Audience Fit",
        "5 Shorts Topic Options",
        "Top 1 Recommendation",
        "Why Now",
        "Risks / Unknowns",
    ],
    "Shorts Research Pack": [
        "Research Scope",
        "Query Log",
        "Source Capture Status",
        "Platform Signals",
        "Topic Clusters",
        "Reference Shorts Evidence",
        "Hook / Punch Analysis",
        "Comment / Community Signals",
        "Chinese Audience Fit",
        "Production Research Notes",
        "Source Evidence Table",
        "Original Text / Transcript Index",
        "Risks / Unknowns",
        "Suggested Next Research",
    ],
}

DEFAULT_PATHS = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/workflows/content-production.md"),
    Path("docs/workflows/longform-research.md"),
    Path("docs/workflows/shorts-research.md"),
    Path("docs/workflows/source-capture-research-rules.md"),
    Path("examples/output-outline.md"),
    Path("prompts/topic-research.md"),
    Path("prompts/shorts-topic-research.md"),
    Path("templates/deliverables/longform-research-report.md"),
    Path("templates/deliverables/shorts-topic-pack.md"),
    Path("templates/deliverables/shorts-research-pack.md"),
]


def extract_headings(content: str) -> List[str]:
    headings: List[str] = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line.startswith("#"):
            headings.append(line.lstrip("#").strip())
    return headings


def check_files(paths: Iterable[Path]) -> List[str]:
    failures: List[str] = []
    for path in paths:
        content = Path(path).read_text(encoding="utf-8")
        headings = extract_headings(content)
        for package_name, required_sections in EXPECTED_PACKAGES.items():
            if package_name not in headings:
                continue
            missing = [section for section in required_sections if section not in headings]
            if missing:
                failures.append(f"{path}: missing {package_name} sections: {', '.join(missing)}")
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check repo docs for package heading consistency.")
    parser.add_argument("paths", nargs="*", help="Specific files to check. Defaults to the known docs set.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths = [Path(path) for path in args.paths] if args.paths else DEFAULT_PATHS
    failures = check_files(paths)
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("Docs consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
