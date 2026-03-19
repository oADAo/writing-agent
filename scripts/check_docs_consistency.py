from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, List


EXPECTED_PACKAGES = {
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
        "Top 3",
        "10 Candidate Titles",
        "Angle Notes",
        "3 Thumbnail Copy Options",
        "3 Thumbnail Composition Directions",
        "Final Title + Thumbnail Pair",
    ],
    "Script Package": [
        "Outline",
        "Full Draft",
        "Fact Check Notes",
    ],
    "Shorts Package": [
        "Hook Title",
        "Final Short Script",
    ],
}

DEFAULT_PATHS = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/workflows/content-production.md"),
    Path("examples/output-outline.md"),
    Path("prompts/topic-research.md"),
    Path("prompts/title-ideation.md"),
    Path("prompts/script-writing.md"),
    Path("prompts/shorts-writing.md"),
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
