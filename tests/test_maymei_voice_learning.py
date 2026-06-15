import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


class MaymeiVoiceLearningTests(unittest.TestCase):
    def test_long_form_prompt_references_taxonomy_and_google_corpus(self) -> None:
        content = read("prompts/script-writing.md")
        self.assertIn("article_taxonomy.md", content)
        self.assertIn("google-maymei-game-scripts.md", content)

    def test_content_rules_point_to_current_voice_memory_and_fixed_intro(self) -> None:
        content = read("docs/profiles/may-story/content_rules.md")
        self.assertNotIn("script_voice_memory.md", content)
        self.assertIn("google-maymei-game-scripts.md", content)

    def test_shorts_rules_inherit_voice_without_default_self_intro(self) -> None:
        content = read("docs/profiles/may-story/shorts_rules.md")
        self.assertIn("article_taxonomy.md", content)
        self.assertIn("google-maymei-game-scripts.md", content)

    def test_agents_points_to_longform_research_contract(self) -> None:
        content = read("AGENTS.md")
        self.assertIn("docs/workflows/longform-research.md", content)
        self.assertIn("docs/workflows/source-capture-research-rules.md", content)
        self.assertIn("prompts/topic-research.md", content)
        self.assertIn("長片研究報告", content)
        self.assertIn("--mode longform-research", content)
        self.assertIn("source-originals/", content)
        self.assertIn("transcripts/", content)
        self.assertNotIn("article_taxonomy.md", content)
        self.assertNotIn("universal_video_template.md", content)
        self.assertNotIn("[ending]", content)


if __name__ == "__main__":
    unittest.main()
