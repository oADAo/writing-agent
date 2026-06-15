import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


class OpenCliResearchWorkflowTests(unittest.TestCase):
    def test_agents_requires_opencli_for_longform_search(self) -> None:
        content = read("AGENTS.md")
        self.assertIn("opencli youtube search", content)
        self.assertIn("opencli google search", content)
        self.assertIn("opencli bilibili search", content)
        self.assertIn("opencli web read", content)
        self.assertIn("Shorts Research", content)
        self.assertIn("opencli tiktok search", content)

    def test_longform_prompt_is_opencli_first(self) -> None:
        content = read("prompts/topic-research.md")
        self.assertIn("opencli youtube search", content)
        self.assertIn("opencli google search", content)
        self.assertIn("opencli web read", content)
        self.assertIn("Source Capture", content)
        self.assertIn("Longform Research Report", content)

    def test_longform_workflow_requires_source_capture_and_transcripts(self) -> None:
        content = read("docs/workflows/longform-research.md")
        self.assertIn("source-originals/", content)
        self.assertIn("transcripts/", content)
        self.assertIn("PACKAGE-MANIFEST.md", content)
        self.assertIn("python scripts/opencli_tooling.py transcript", content)

    def test_shorts_workflow_requires_short_video_platforms_and_source_capture(self) -> None:
        content = read("docs/workflows/shorts-research.md")
        self.assertIn("YouTube Shorts", content)
        self.assertIn("TikTok", content)
        self.assertIn("IG Reels", content)
        self.assertIn("source-originals/", content)
        self.assertIn("transcripts/", content)
        self.assertIn("Shorts Research Pack", content)
        self.assertIn("--mode shorts-research", content)

    def test_query_log_template_requires_opencli_command_marker(self) -> None:
        content = read("templates/memory/query-log.md")
        self.assertIn("opencli command:", content)
        self.assertIn("Included in final conclusion?:", content)

    def test_source_index_template_requires_capture_markers(self) -> None:
        content = read("templates/memory/source-index.md")
        self.assertIn("Capture status:", content)
        self.assertIn("Evidence file:", content)
        self.assertIn("Actual text read:", content)
        self.assertIn("Included in conclusion?:", content)


if __name__ == "__main__":
    unittest.main()
