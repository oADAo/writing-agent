import tempfile
import unittest
from pathlib import Path

from scripts.check_docs_consistency import check_files


LONGFORM_REPORT_BLOCK = """```md
# Longform Research Report
## Research Scope
## Topic Decision
## Query Log
## Source Capture Status
## Market / Player Demand Signals
## Chapter Plan
## Chapter Research Cards
## Source Evidence Table
## Original Text / Transcript Index
## Risks / Unknowns
## Need In-Game Verification
## Suggested Next Research
```
"""


SHORTS_RESEARCH_BLOCK = """```md
# Shorts Research Pack
## Research Scope
## Query Log
## Source Capture Status
## Platform Signals
## Topic Clusters
## Reference Shorts Evidence
## Hook / Punch Analysis
## Comment / Community Signals
## Chinese Audience Fit
## Production Research Notes
## Source Evidence Table
## Original Text / Transcript Index
## Risks / Unknowns
## Suggested Next Research
```
"""


class CheckDocsConsistencyTests(unittest.TestCase):
    def write_file(self, root: Path, relative_path: str, content: str) -> Path:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_reports_missing_longform_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            malformed = self.write_file(
                root,
                "README.md",
                """# README

```md
# Longform Research Report
## Research Scope
## Topic Decision
## Query Log
## Source Capture Status
## Chapter Plan
## Chapter Research Cards
## Risks / Unknowns
```
""",
            )

            failures = check_files([malformed])

            self.assertEqual(len(failures), 1)
            self.assertIn("Market / Player Demand Signals", failures[0])
            self.assertIn("Source Evidence Table", failures[0])
            self.assertIn("Original Text / Transcript Index", failures[0])

    def test_accepts_well_formed_longform_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            well_formed = self.write_file(
                root,
                "README.md",
                "# README\n\n" + LONGFORM_REPORT_BLOCK,
            )

            failures = check_files([well_formed])

            self.assertEqual(failures, [])

    def test_still_accepts_legacy_topic_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            well_formed = self.write_file(
                root,
                "README.md",
                """# README

```md
# Topic Brief
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
```
""",
            )

            failures = check_files([well_formed])

            self.assertEqual(failures, [])

    def test_accepts_well_formed_shorts_research_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            well_formed = self.write_file(
                root,
                "README.md",
                "# README\n\n" + SHORTS_RESEARCH_BLOCK,
            )

            failures = check_files([well_formed])

            self.assertEqual(failures, [])

    def test_reports_missing_shorts_research_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            malformed = self.write_file(
                root,
                "README.md",
                """# README

```md
# Shorts Research Pack
## Research Scope
## Query Log
## Source Capture Status
## Platform Signals
## Topic Clusters
## Reference Shorts Evidence
## Risks / Unknowns
```
""",
            )

            failures = check_files([malformed])

            self.assertEqual(len(failures), 1)
            self.assertIn("Hook / Punch Analysis", failures[0])
            self.assertIn("Production Research Notes", failures[0])
            self.assertIn("Source Evidence Table", failures[0])


if __name__ == "__main__":
    unittest.main()
