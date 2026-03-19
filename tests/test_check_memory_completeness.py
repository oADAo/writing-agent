import tempfile
import unittest
from pathlib import Path

from scripts.check_memory_completeness import check_topic_run


class CheckMemoryCompletenessTests(unittest.TestCase):
    def write_file(self, root: Path, relative_path: str, content: str) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_rejects_incomplete_topic_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root, "query-log.md", "# Query Log\n")
            self.write_file(root, "decision-log.md", "# Decision Log\n")

            failures = check_topic_run(root)

            self.assertTrue(any("sources.md" in failure for failure in failures))
            self.assertTrue(any("查詢平台 / 站點" in failure for failure in failures))

    def test_accepts_complete_topic_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(
                root,
                "query-log.md",
                """# Query Log

## Query 1
- 查詢平台 / 站點：YouTube
- 語圈：中文
- 使用關鍵字：魔物獵人荒野 新手
- 找到的高訊號內容：高觀看新手影片
- 是否納入主結論：是
""",
            )
            self.write_file(
                root,
                "sources.md",
                """# Source Index

## Source 1
- 類型：影片
- 連結：https://example.com
- 摘要：高觀看新手整理
- 用途：YouTube 交叉驗證
""",
            )
            self.write_file(
                root,
                "decision-log.md",
                """# Decision Log

## Confirmed Facts
- 新手題型在兩語圈重複出現

## Included In Final Output
- 納入開局必做題型
""",
            )

            failures = check_topic_run(root)

            self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
