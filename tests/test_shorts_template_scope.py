import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


class ShortsTemplateScopeTests(unittest.TestCase):
    def test_shorts_template_only_lives_in_shorts_flow(self) -> None:
        self.assertIn("universal_video_template.md", read("prompts/shorts-writing.md"))
        self.assertIn("universal_video_template.md", read("docs/profiles/may-story/shorts_rules.md"))

        self.assertNotIn("universal_video_template.md", read("prompts/script-writing.md"))
        self.assertNotIn("universal_video_template.md", read("docs/profiles/may-story/script_template.md"))
        self.assertNotIn("通用節奏模板記憶", read("docs/profiles/may-story/voice_memory.md"))

    def test_agents_only_points_to_template_once_for_shorts_mode(self) -> None:
        content = read("AGENTS.md")
        self.assertEqual(content.count("universal_video_template.md"), 1)

    def test_template_marked_script_uses_chapter_marker_not_markdown_heading(self) -> None:
        for rel_path in [
            "prompts/shorts-writing.md",
            "docs/profiles/may-story/shorts_rules.md",
            "docs/profiles/may-story/universal_video_template.md",
            "examples/output-outline.md",
            "workspace/deliverables/shorts/2026-03-20-pokopia-rocket-best-short.md",
        ]:
            content = read(rel_path)
            self.assertIn("[chapter]", content, rel_path)
            self.assertNotIn("# 第一章", content, rel_path)


if __name__ == "__main__":
    unittest.main()
