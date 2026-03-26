from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional


REQUIRED_HEADINGS = {
    "topic": {
        "title": "Topic Brief",
        "sections": [
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
    },
    "title": {
        "title": "Title Pack",
        "sections": [
            "Topic",
            "Top 3",
            "10 Candidate Titles",
            "Angle Notes",
            "3 Thumbnail Copy Options",
            "3 Thumbnail Composition Directions",
            "Final Title + Thumbnail Pair",
        ],
    },
    "script": {
        "title": "Script Package",
        "sections": ["Outline", "Full Draft", "Fact Check Notes"],
    },
    "shorts": {
        "title": "Shorts Package",
        "sections": [
            "Hook Title",
            "Hook Burst Text",
            "Template Marked Script",
        ],
    },
    "shorts-topic": {
        "title": "Shorts Topic Pack",
        "sections": [
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
    },
}


def extract_headings(content: str) -> List[str]:
    headings: List[str] = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line.startswith("#"):
            headings.append(line.lstrip("#").strip())
    return headings


def detect_mode(headings: List[str]) -> Optional[str]:
    for mode, config in REQUIRED_HEADINGS.items():
        if headings and headings[0] == config["title"]:
            return mode
    return None


def check_deliverable(path: Path, mode: Optional[str] = None) -> List[str]:
    content = Path(path).read_text(encoding="utf-8")
    headings = extract_headings(content)
    resolved_mode = mode or detect_mode(headings)
    if resolved_mode is None:
        return [f"{path}: unable to detect deliverable mode"]
    if resolved_mode not in REQUIRED_HEADINGS:
        return [f"{path}: unsupported mode '{resolved_mode}'"]

    config = REQUIRED_HEADINGS[resolved_mode]
    failures: List[str] = []
    if not headings or headings[0] != config["title"]:
        failures.append(f"{path}: expected title '# {config['title']}'")

    missing = [section for section in config["sections"] if section not in headings]
    if missing:
        failures.append(f"{path}: missing sections: {', '.join(missing)}")
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a deliverable file for required headings.")
    parser.add_argument("path", help="Path to the deliverable markdown file.")
    parser.add_argument("--mode", choices=sorted(REQUIRED_HEADINGS.keys()))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    failures = check_deliverable(Path(args.path), mode=args.mode)
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("Deliverable shape check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
