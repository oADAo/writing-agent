import subprocess
import unittest
from pathlib import Path

from scripts.analyze_maymei_style_samples import analyze_style_text
from scripts.build_maymei_formula_cards import build_formula_cards
from scripts.build_maymei_golden_samples import infer_game_name, match_video_to_sources, select_golden_samples
from scripts.build_maymei_writing_system import (
    WritingSample,
    build_decision_cards,
    classify_writing_formula,
    extract_transform_pairs,
    title_from_path,
)
from scripts.build_maymei_video_metrics import parse_yt_dlp_video
from scripts.check_maymei_final_draft import evaluate_final_draft
from scripts.retrieve_maymei_writing_guidance import retrieve_guidance
from scripts.retrieve_maymei_samples import retrieve_samples


ROOT = Path(__file__).resolve().parents[1]


class MaymeiFinalizerPipelineTests(unittest.TestCase):
    def test_analyze_script_can_run_as_file(self) -> None:
        result = subprocess.run(
            [
                "python",
                str(ROOT / "scripts" / "analyze_maymei_style_samples.py"),
                "--help",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("style forensics", result.stdout)

    def test_writing_system_script_can_run_as_file(self) -> None:
        result = subprocess.run(
            [
                "python",
                str(ROOT / "scripts" / "build_maymei_writing_system.py"),
                "--help",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("writing decision system", result.stdout)

    def test_parse_yt_dlp_video_handles_missing_likes(self) -> None:
        record = parse_yt_dlp_video(
            {
                "id": "abc123",
                "title": "Sample Guide",
                "webpage_url": "https://www.youtube.com/watch?v=abc123",
                "view_count": 1000,
                "like_count": None,
                "comment_count": 12,
                "upload_date": "20260420",
                "duration": 605,
            }
        )

        self.assertEqual(record["video_id"], "abc123")
        self.assertEqual(record["view_count"], 1000)
        self.assertEqual(record["like_count"], 0)
        self.assertEqual(record["like_rate"], 0.0)
        self.assertEqual(record["comment_count"], 12)

    def test_golden_sample_selection_balances_formulas(self) -> None:
        candidates = [
            self.metric("a", "Beginner A", 10000, 900),
            self.metric("b", "Beginner B", 9000, 800),
            self.metric("c", "Beginner C", 8000, 700),
            self.metric("d", "Build D", 3000, 500),
            self.metric("e", "Build E", 2500, 450),
        ]
        sources = [
            self.source("Beginner A", "新手技巧清單"),
            self.source("Beginner B", "新手技巧清單"),
            self.source("Beginner C", "新手技巧清單"),
            self.source("Build D", "流派 build"),
            self.source("Build E", "流派 build"),
        ]

        selected = select_golden_samples(candidates, sources, target_count=4, per_formula_cap=2)

        formulas = [item["formula"] for item in selected]
        self.assertEqual(formulas.count("新手技巧清單"), 2)
        self.assertEqual(formulas.count("流派 build"), 2)

    def test_video_to_source_match_rejects_weak_match(self) -> None:
        metric = self.metric("x", "Completely Different Video", 1000, 100)
        sources = [self.source("No Shared Words Here", "一般攻略")]

        match = match_video_to_sources(metric, sources, min_similarity=0.55)

        self.assertIsNone(match)

    def test_game_name_is_inferred_from_video_or_source_title(self) -> None:
        self.assertEqual(
            infer_game_name("【黑神話悟空】最快速的刷錢方法 | 刷錢攻略"),
            "黑神話悟空",
        )
        self.assertEqual(
            infer_game_name("【超詳細】血月後必做的四件事 | 薩爾達傳說 : 王國之淚"),
            "薩爾達傳說：王國之淚",
        )

    def test_metric_title_game_beats_generic_source_fragment(self) -> None:
        selected = select_golden_samples(
            [self.metric("moon", "【超詳細】血月後必做的四件事 | 薩爾達傳說 : 王國之淚", 1000, 100)],
            [
                {
                    "title": "強制血月刷新",
                    "formula": "機制拆解",
                    "primary_category": "機制拆解",
                    "source_path": "docs/moon.docx",
                    "opening_promise": "血月後必做的四件事",
                }
            ],
            target_count=1,
        )

        self.assertEqual(selected[0]["game"], "薩爾達傳說：王國之淚")

    def test_style_forensics_extracts_required_sections(self) -> None:
        analysis = analyze_style_text(
            "大家好，這裡是玫玫物語。\n"
            "我自己最推薦先做這件事，因為真的會省很多時間。\n"
            "第一個重點，是先把地圖開起來。\n"
            "這樣你後面跑素材時，就不用一直繞路。\n"
            "最後一點，如果你是新手，我會建議不要太早亂花資源。",
            title="新手開局必看攻略",
            formula="新手技巧清單",
        )

        for key in (
            "opening_promise_pattern",
            "first_person_experience",
            "emotional_player_alignment",
            "sentence_rhythm",
            "transitions",
            "information_order",
            "maymei_like_lines",
            "data_only_lines",
            "learnable_structure",
            "do_not_copy",
        ):
            self.assertIn(key, analysis)
        self.assertTrue(analysis["maymei_like_lines"])
        self.assertTrue(analysis["learnable_structure"])

    def test_formula_cards_mark_insufficient_data_under_minimum(self) -> None:
        forensics = [
            {"formula": "新手技巧清單", "opening_promise_pattern": "promise", "learnable_structure": ["a"]},
            {"formula": "新手技巧清單", "opening_promise_pattern": "promise", "learnable_structure": ["b"]},
        ]

        cards = build_formula_cards(forensics, min_samples=5)

        self.assertEqual(cards["新手技巧清單"]["status"], "insufficient_data")
        self.assertEqual(cards["新手技巧清單"]["sample_count"], 2)

    def test_retrieve_samples_returns_main_and_auxiliary(self) -> None:
        samples = [
            self.golden("a", "寶可夢 新手 開局", "新手技巧清單", 95),
            self.golden("b", "寶可夢 前期 技巧", "新手技巧清單", 90),
            self.golden("c", "寶可夢 必看 攻略", "新手技巧清單", 80),
            self.golden("d", "魔物 刷素材", "效率刷法", 99),
            self.golden("e", "寶可夢 最強排行", "排行 top list", 88),
            self.golden("f", "寶可夢 機制解析", "機制拆解", 70),
        ]

        result = retrieve_samples(
            samples,
            topic="寶可夢 前期 新手必看",
            game="寶可夢",
            formula="新手技巧清單",
            main_count=3,
            auxiliary_count=2,
        )

        self.assertEqual(len(result["main_samples"]), 3)
        self.assertEqual(len(result["auxiliary_samples"]), 2)
        self.assertTrue(all(item["formula"] == "新手技巧清單" for item in result["main_samples"]))

    def test_final_draft_evaluator_flags_ai_cliches_and_missing_judgment(self) -> None:
        result = evaluate_final_draft(
            "總體來說，這是一個不錯的選擇。\n"
            "不只是可以提升效率，更是能改善體驗。\n"
            "對玩家來說是一個值得注意的系統。",
            allowed_facts=["提升效率"],
        )

        self.assertLess(result["score"], 85)
        self.assertIn("ai_cliche", result["failed_checks"])
        self.assertIn("judgment_voice", result["failed_checks"])

    def test_final_draft_evaluator_flags_not_but_pattern(self) -> None:
        result = evaluate_final_draft(
            "大家好~這裡是玫玫物語。\n"
            "這次是買前必看攻略，玩家可以少踩坑。\n"
            "我推薦先看版本差異，這不是單純換地圖，而是整個進度節奏都變了。",
        )

        self.assertIn("ai_cliche", result["failed_checks"])

    def test_writing_system_extracts_fact_to_voice_pairs(self) -> None:
        sample = WritingSample(
            sample_id="sample",
            title="買前必看",
            source_path="sample.docx",
            primary_category="推薦清單",
            formula="推薦清單",
            char_count=100,
            paragraph_count=5,
            trust_level="test",
            priority=100,
            opening=[],
            chapter_heads=[],
            judgment_lines=[],
            player_lines=[],
            ai_tone_hits=[],
        )

        pairs = extract_transform_pairs(
            sample,
            [
                "官方確認 PS5 版會在 2026 年稍後推出，但還沒有日期。",
                "PS5 玩家目前就先等，不要現在就把它當同步首發。",
            ],
        )

        self.assertEqual(len(pairs), 1)
        self.assertIn("PS5 玩家", pairs[0].maymei_line)

    def test_writing_system_decision_cards_include_human_drafting_rules(self) -> None:
        card = build_decision_cards(
            [
                WritingSample(
                    sample_id="sample",
                    title="買前必看",
                    source_path="sample.docx",
                    primary_category="推薦清單",
                    formula="推薦清單",
                    char_count=100,
                    paragraph_count=5,
                    trust_level="test",
                    priority=100,
                    opening=[],
                    chapter_heads=["版本選擇"],
                    judgment_lines=["我自己覺得標準版最適合先試試看。"],
                    player_lines=["新手可以先從標準版開始。"],
                    ai_tone_hits=[],
                )
            ]
        )["推薦清單"]

        self.assertIn("drafting_directives", card)
        self.assertTrue(any("玩家該怎麼判斷" in item for item in card["must_not"]))

    def test_writing_system_classifies_buy_before_and_cleans_numbered_title(self) -> None:
        self.assertEqual(
            title_from_path(Path("0030 - 【死亡擱淺2】買之前 10件 你需要知道的事情.docx")),
            "【死亡擱淺2】買之前 10件 你需要知道的事情",
        )
        self.assertEqual(classify_writing_formula("【死亡擱淺2】買之前 10件 你需要知道的事情"), "買前必看")

    def test_retrieve_writing_guidance_returns_decision_card_and_pairs(self) -> None:
        system = {
            "samples": [
                {
                    "title": "【死亡擱淺2】買之前 10件 你需要知道的事情",
                    "formula": "買前必看",
                    "priority": 90,
                    "source_path": "sample.docx",
                }
            ],
            "transform_pairs": [
                {
                    "title": "【死亡擱淺2】買之前 10件 你需要知道的事情",
                    "formula": "買前必看",
                    "fact_line": "PS5 版稍後推出，尚未公布日期。",
                    "maymei_line": "PS5 玩家目前就先等。",
                    "transformation": "把資料條件轉成購買或行動建議。",
                }
            ],
            "decision_cards": {
                "買前必看": {
                    "formula": "買前必看",
                    "drafting_directives": ["平台、版本、價格放後段。"],
                    "must_not": ["不要只列官方功能。"],
                }
            },
        }

        guidance = retrieve_guidance(system, topic="死亡擱淺2 買之前", formula="買前必看")

        self.assertEqual(guidance["decision_card"]["formula"], "買前必看")
        self.assertEqual(len(guidance["reference_samples"]), 1)
        self.assertEqual(len(guidance["line_transform_pairs"]), 1)

    @staticmethod
    def metric(video_id: str, title: str, views: int, likes: int) -> dict:
        return {
            "video_id": video_id,
            "title": title,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "view_count": views,
            "like_count": likes,
            "like_rate": likes / views,
            "comment_count": 10,
            "upload_date": "20260420",
            "duration": 600,
        }

    @staticmethod
    def source(title: str, formula: str) -> dict:
        return {
            "title": title,
            "formula": formula,
            "primary_category": formula,
            "source_path": f"docs/{title}.docx",
            "opening_promise": title,
        }

    @staticmethod
    def golden(video_id: str, title: str, formula: str, score: int) -> dict:
        return {
            "video_id": video_id,
            "title": title,
            "formula": formula,
            "primary_category": formula,
            "source_doc": f"docs/{video_id}.docx",
            "score": score,
            "selected_as_gold": True,
        }


if __name__ == "__main__":
    unittest.main()
