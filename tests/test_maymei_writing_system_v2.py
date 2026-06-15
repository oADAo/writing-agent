import unittest

from scripts.check_maymei_ai_patterns import evaluate_ai_patterns
from scripts.check_maymei_read_aloud_friction import evaluate_read_aloud_friction
from scripts.check_maymei_retention_beats import evaluate_retention_beats
from scripts.learn_from_user_revision import align_revisions


class MaymeiWritingSystemV2Tests(unittest.TestCase):
    def test_ai_pattern_checker_flags_formulaic_chinese(self) -> None:
        result = evaluate_ai_patterns("總體來說，這不是一般冒險，而是一款沉浸式體驗。")

        self.assertFalse(result["passed"])
        self.assertIn("總體來說", result["hits"])

    def test_read_aloud_checker_flags_long_comma_chain(self) -> None:
        result = evaluate_read_aloud_friction(
            "這款遊戲包含潛行、格鬥、射擊、追車、Q裝備、話術、社交潛入、挑戰模式，而且還有很多內容可以體驗。"
        )

        self.assertFalse(result["passed"])
        self.assertGreaterEqual(result["comma_heavy_count"], 1)

    def test_retention_checker_accepts_buy_before_shape_with_broll(self) -> None:
        result = evaluate_retention_beats(
            "# Final Draft\n"
            "007 買之前必看，這次先幫玩家判斷首發要不要等。\n"
            "## 這不是下一款刺客任務\n"
            "如果你喜歡刺客任務，我會先把期待放在寬線性潛入。這段 B-roll 用肯辛頓晚宴。\n"
            "## PC 版先等\n"
            "PC 玩家如果介意 Denuvo，我推薦先等首發評測。畫面放 Steam 頁面。\n"
        )

        self.assertTrue(result["passed"])
        self.assertEqual(result["weak_sections"], [])

    def test_revision_learning_pairs_ai_and_user_blocks(self) -> None:
        pairs = align_revisions(
            "本作提供了豐富的內容。",
            "這裡我會先看它到底能不能讓玩家玩得夠久。",
        )

        self.assertEqual(len(pairs), 1)
        self.assertIn("user_line", pairs[0])


if __name__ == "__main__":
    unittest.main()
