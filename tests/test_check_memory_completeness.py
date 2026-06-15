import tempfile
import unittest
from pathlib import Path

from scripts.check_memory_completeness import check_topic_run


class CheckMemoryCompletenessTests(unittest.TestCase):
    def write_file(self, root: Path, relative_path: str, content: str) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_rejects_incomplete_longform_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root, "query-log-reviewed.md", "# Query Log\n")
            self.write_file(root, "decision-log.md", "# Decision Log\n")

            failures = check_topic_run(root)

            self.assertTrue(any("sources.md" in failure for failure in failures))
            self.assertTrue(any("PACKAGE-MANIFEST.md" in failure for failure in failures))
            self.assertTrue(any("source-originals" in failure for failure in failures))
            self.assertTrue(any("tool readiness" in failure for failure in failures))

    def test_accepts_complete_longform_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "source-originals").mkdir()
            (root / "transcripts").mkdir()
            self.write_file(root, "tool-readiness.md", "# Tool Readiness\n")
            self.write_file(
                root,
                "query-log-reviewed.md",
                """# Query Log

## Query 1
- Query platform / site: `youtube` / `YouTube`
- Language: `中文`
- opencli command: `opencli youtube search "game 攻略" --limit 10 -f json`
- Keywords: `game 攻略`
- High-signal hits:
  - `影片 A` - https://www.youtube.com/watch?v=demo
- Included in final conclusion?: `pending`
""",
            )
            self.write_file(
                root,
                "sources.md",
                """# Source Index

## Source 1
- Source name: `影片 A`
- URL: `https://www.youtube.com/watch?v=demo`
- Source type: `YouTube`
- Capture status: `transcript captured`
- Evidence file: `transcripts/video-a.md`
- Actual text read: `逐字稿提到前期資源路線。`
- Supports: `Chapter 1`
- Why keep it?: `中文圈高觀看樣本`
""",
            )
            self.write_file(
                root,
                "decision-log.md",
                """# Decision Log

## Confirmed Facts
- 樣本存在且可追溯。

## Working Inferences
- 需要再做主題簇整理。

## Included In Final Output
- 已保留中文圈高觀看樣本。
""",
            )
            self.write_file(
                root,
                "PACKAGE-MANIFEST.md",
                """# Package Manifest

## Source originals
- source-originals/

## Transcripts
- transcripts/

## Uncaptured sources
- none
""",
            )

            failures = check_topic_run(root)

            self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
