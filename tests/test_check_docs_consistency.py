import tempfile
import unittest
from pathlib import Path

from scripts.check_docs_consistency import check_files


class CheckDocsConsistencyTests(unittest.TestCase):
    def write_file(self, root: Path, relative_path: str, content: str) -> Path:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_reports_missing_topic_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            malformed = self.write_file(
                root,
                "README.md",
                """# README

```md
# Topic Brief
## Inputs
## Market Signals
## Cross-Language Competitor Hits
## Chinese Audience Fit
## 5 Topic Options
## Top 1 Recommendation
## Why Now
## Risks / Unknowns
```
""",
            )

            failures = check_files([malformed])

            self.assertEqual(len(failures), 1)
            self.assertIn("Query Log", failures[0])
            self.assertIn("Community / Forum Signals", failures[0])
            self.assertIn("Cross-Source Validation", failures[0])

    def test_accepts_well_formed_topic_sections(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
