from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List


TOPIC_REQUIRED_FILES = [
    "query-log.md",
    "sources.md",
    "decision-log.md",
]

TOPIC_REQUIRED_MARKERS = {
    "query-log.md": [
        "查詢平台 / 站點",
        "使用關鍵字",
        "是否納入主結論",
    ],
    "sources.md": [
        "連結",
        "用途",
    ],
    "decision-log.md": [
        "Confirmed Facts",
        "Included In Final Output",
    ],
}


def check_topic_run(path: Path) -> List[str]:
    failures: List[str] = []
    root = Path(path)

    for file_name in TOPIC_REQUIRED_FILES:
        file_path = root / file_name
        if not file_path.exists():
            failures.append(f"{root}: missing required file {file_name}")
            continue

        content = file_path.read_text(encoding="utf-8")
        for marker in TOPIC_REQUIRED_MARKERS[file_name]:
            if marker not in content:
                failures.append(f"{file_path}: missing marker '{marker}'")
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a topic memory run for required files and markers.")
    parser.add_argument("path", help="Path to the topic run directory.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    failures = check_topic_run(Path(args.path))
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("Memory completeness check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
