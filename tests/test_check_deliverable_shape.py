import tempfile
import unittest
from pathlib import Path

from scripts.check_deliverable_shape import check_deliverable


VALID_LONGFORM_REPORT = """# Longform Research Report

## Research Scope
- Game:

## Topic Decision
- Recommended topic:

## Query Log
- opencli command:

## Source Capture Status
- Tool readiness file:
- Source originals folder:
- Transcript folder:
- Package manifest:

## Market / Player Demand Signals

## Chapter Plan

## Chapter Research Cards
- Needs in-game verification:

## Source Evidence Table
- Evidence file:
- Actual text read:
- Included in conclusion?:

## Original Text / Transcript Index

## Risks / Unknowns

## Need In-Game Verification

## Suggested Next Research
"""


VALID_SHORTS_RESEARCH_PACK = """# Shorts Research Pack

## Research Scope
- Game:

## Query Log
| Platform / Site | Language | opencli command | Keywords | High-signal hits | Included in conclusion? |

## Source Capture Status
- Tool readiness file:
- Source originals folder:
- Transcript folder:
- Package manifest:

## Platform Signals

## Topic Clusters

## Reference Shorts Evidence
- Shorts URL:
- Evidence file:
- Actual text read:
- Capture status:
- Included in conclusion?:

## Hook / Punch Analysis

## Comment / Community Signals

## Chinese Audience Fit

## Production Research Notes

## Source Evidence Table

## Original Text / Transcript Index

## Risks / Unknowns

## Suggested Next Research
"""


class CheckDeliverableShapeTests(unittest.TestCase):
    def write_file(self, content: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "deliverable.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_accepts_valid_longform_research_report(self) -> None:
        path = self.write_file(VALID_LONGFORM_REPORT)

        result = check_deliverable(path, mode="longform-research")

        self.assertEqual(result, [])

    def test_detects_longform_research_report_by_title(self) -> None:
        path = self.write_file(VALID_LONGFORM_REPORT)

        result = check_deliverable(path)

        self.assertEqual(result, [])

    def test_rejects_longform_report_missing_required_heading(self) -> None:
        path = self.write_file(
            VALID_LONGFORM_REPORT.replace("## Source Evidence Table\n", "")
        )

        result = check_deliverable(path, mode="longform-research")

        self.assertEqual(len(result), 1)
        self.assertIn("Source Evidence Table", result[0])

    def test_rejects_longform_report_missing_source_capture_markers(self) -> None:
        path = self.write_file(
            VALID_LONGFORM_REPORT.replace("- Evidence file:\n", "").replace(
                "- Actual text read:\n", ""
            )
        )

        result = check_deliverable(path, mode="longform-research")

        self.assertEqual(len(result), 1)
        self.assertIn("Evidence file:", result[0])
        self.assertIn("Actual text read:", result[0])

    def test_accepts_legacy_topic_brief_for_old_deliverables(self) -> None:
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

        result = check_deliverable(path, mode="topic")

        self.assertEqual(result, [])

    def test_accepts_valid_shorts_research_pack(self) -> None:
        path = self.write_file(VALID_SHORTS_RESEARCH_PACK)

        result = check_deliverable(path, mode="shorts-research")

        self.assertEqual(result, [])

    def test_rejects_shorts_research_pack_missing_capture_markers(self) -> None:
        path = self.write_file(
            VALID_SHORTS_RESEARCH_PACK.replace("- Shorts URL:\n", "").replace(
                "- Evidence file:\n", ""
            )
        )

        result = check_deliverable(path, mode="shorts-research")

        self.assertEqual(len(result), 1)
        self.assertIn("Shorts URL:", result[0])
        self.assertIn("Evidence file:", result[0])


if __name__ == "__main__":
    unittest.main()
