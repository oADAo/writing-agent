import tempfile
import unittest
from pathlib import Path

from scripts.check_deliverable_shape import check_deliverable


class CheckDeliverableShapeTests(unittest.TestCase):
    def write_file(self, content: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "deliverable.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_accepts_valid_topic_brief(self) -> None:
        path = self.write_file(
            """# Topic Brief

## Inputs
## Query Log
## Market Signals
## Community / Forum Signals
## Cross-Language Competitor Hits
## Cross-Source Validation
## Chinese Audience Fit
## 5 Topic Options
## Top 1 Recommendation
## Why Now
## Risks / Unknowns
"""
        )

        result = check_deliverable(path)

        self.assertEqual(result, [])

    def test_rejects_missing_required_heading(self) -> None:
        path = self.write_file(
            """# Shorts Package

## Hook Title
"""
        )

        result = check_deliverable(path, mode="shorts")

        self.assertEqual(len(result), 1)
        self.assertIn("Final Short Script", result[0])


if __name__ == "__main__":
    unittest.main()
