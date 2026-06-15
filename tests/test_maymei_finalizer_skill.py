import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maymei-script-finalizer"


class MaymeiFinalizerSkillTests(unittest.TestCase):
    def test_skill_instructions_are_complete(self):
        skill_md = SKILL_DIR / "SKILL.md"

        text = skill_md.read_text(encoding="utf-8")

        self.assertNotIn("TODO", text)
        self.assertIn("maymei-script-finalizer", text)
        self.assertIn("retrieve_maymei_samples.py", text)
        self.assertIn("check_maymei_final_draft.py", text)
        self.assertIn("Final Draft", text)
        self.assertIn("Voice Check", text)
        self.assertIn("Fact Check Notes", text)
        self.assertIn("85", text)

    def test_reference_guides_exist(self):
        required = {
            "finalizer-rubric.md": ["rubric", "anti-AI", "85"],
            "golden-sample-selection.md": ["golden", "style forensics", "formula card"],
        }

        for filename, markers in required.items():
            with self.subTest(filename=filename):
                text = (SKILL_DIR / "references" / filename).read_text(encoding="utf-8")
                for marker in markers:
                    self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
