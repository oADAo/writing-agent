import unittest

from scripts.build_article_corpus_index import classify_formula, classify_primary_category


class BuildArticleCorpusIndexTests(unittest.TestCase):
    def test_classifies_recommendation_title(self) -> None:
        title = "【2025年遊戲大作推薦】近年來最豪華的一年，每一款都是必玩神作！"
        self.assertEqual(classify_primary_category(title), "推薦清單")
        self.assertEqual(classify_formula(title), "推薦清單")

    def test_classifies_beginner_title(self) -> None:
        title = "【寶可夢ZA】新手開局必看攻略 學會這10個實用技巧，前期開荒沒煩惱"
        self.assertEqual(classify_primary_category(title), "新手開局")
        self.assertEqual(classify_formula(title), "新手技巧清單")

    def test_classifies_efficiency_title(self) -> None:
        title = "【黑神話悟空】最快速的刷錢方法 1分鐘暴賺6000經驗，簡單又有效率"
        self.assertEqual(classify_primary_category(title), "資源效率")
        self.assertEqual(classify_formula(title), "效率刷法")

    def test_classifies_build_title(self) -> None:
        title = "【版本最強流派】無傷劈爛所有BOSS，學會這一套就能打到通關"
        self.assertEqual(classify_primary_category(title), "配裝流派")
        self.assertEqual(classify_formula(title), "流派 build")

    def test_build_title_with_newbie_phrase_stays_build(self) -> None:
        title = "【版本最強流派】無傷劈爛所有BOSS，適合新手逃課，學會這一套就能打到通關"
        self.assertEqual(classify_primary_category(title), "配裝流派")
        self.assertEqual(classify_formula(title), "流派 build")

    def test_classifies_ranked_title(self) -> None:
        title = "【超實用】Top5 最強武器以及武器入手方式"
        self.assertEqual(classify_primary_category(title), "排行精選")
        self.assertEqual(classify_formula(title), "排行 top list")

    def test_classifies_guide_title(self) -> None:
        title = "【超詳細】火之神殿完全攻略 五鑰匙位置 寶箱位置"
        self.assertEqual(classify_primary_category(title), "完整攻略")
        self.assertEqual(classify_formula(title), "完整攻略")

    def test_hidden_boss_guide_is_not_misclassified_as_build(self) -> None:
        title = "【黑神話悟空】玩第三章前必看，全隱藏支線任務攻略，帶你找到所有隱藏BOSS，解鎖裝備升級"
        self.assertEqual(classify_primary_category(title), "完整攻略")
        self.assertEqual(classify_formula(title), "完整攻略")

    def test_hidden_side_quest_detail_guide_is_complete_guide(self) -> None:
        title = "【黑神話悟空】第五章火焰山全隱藏BOSS，隱藏支線詳細攻略，解鎖最強蓄力劈棍畢業武器"
        self.assertEqual(classify_primary_category(title), "完整攻略")
        self.assertEqual(classify_formula(title), "完整攻略")

    def test_shrine_solution_guide_is_complete_guide(self) -> None:
        title = "【神廟攻略】馬亞奇諾烏神廟解法攻略 | 固定之物 | 薩爾達傳說:王國之淚"
        self.assertEqual(classify_primary_category(title), "完整攻略")
        self.assertEqual(classify_formula(title), "完整攻略")

    def test_blood_moon_mandatory_title_is_mechanic_not_day_one(self) -> None:
        title = "【超詳細】血月後必做的四件事 血月機制詳細解說"
        self.assertEqual(classify_primary_category(title), "完整攻略")
        self.assertEqual(classify_formula(title), "機制拆解")


if __name__ == "__main__":
    unittest.main()
