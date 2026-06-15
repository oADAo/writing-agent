import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


class ShortsTemplateScopeTests(unittest.TestCase):
    def test_shorts_research_is_current_entrypoint_but_shorts_writing_is_not(self) -> None:
        current_entrypoints = {
            "AGENTS.md": ["docs/workflows/shorts-research.md"],
            "README.md": ["docs/workflows/shorts-research.md"],
            "docs/project-map.md": ["docs/workflows/shorts-research.md"],
            "docs/agents/skill-routing.md": ["docs/workflows/shorts-research.md"],
        }
        for rel_path, expected in current_entrypoints.items():
            content = read(rel_path)
            for marker in expected:
                self.assertIn(marker, content, rel_path)

        for rel_path in [
            "AGENTS.md",
            "README.md",
            "docs/project-map.md",
            "docs/agents/skill-routing.md",
            "docs/workflows/longform-research.md",
            "prompts/topic-research.md",
        ]:
            content = read(rel_path)
            self.assertNotIn("universal_video_template.md", content, rel_path)
            self.assertNotIn("prompts/shorts-writing.md` |", content, rel_path)

    def test_shorts_research_pack_template_has_source_capture_contract(self) -> None:
        content = read("templates/deliverables/shorts-research-pack.md")
        self.assertIn("# Shorts Research Pack", content)
        self.assertIn("Shorts URL:", content)
        self.assertIn("Evidence file:", content)
        self.assertIn("Actual text read:", content)
        self.assertIn("Production Research Notes", content)

    def test_legacy_shorts_template_still_keeps_chapter_marker(self) -> None:
        for rel_path in [
            "prompts/shorts-writing.md",
            "docs/profiles/may-story/shorts_rules.md",
            "docs/profiles/may-story/universal_video_template.md",
        ]:
            content = read(rel_path)
            self.assertIn("[chapter]", content, rel_path)
            self.assertNotIn("# 第一章", content, rel_path)


if __name__ == "__main__":
    unittest.main()
