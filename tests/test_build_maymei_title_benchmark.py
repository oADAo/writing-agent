import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.build_maymei_title_benchmark import build_dataset, render_markdown


HEADER = [
    "內容",
    "影片標題",
    "影片發布時間",
    "時間長度",
    "互動觀看次數",
    "平均觀看比例 (%)",
    "續看觀眾比率 (%)",
    "非重複觀眾人數",
    "每位觀眾的平均觀看次數",
    "熱推",
    "熱推積分",
    "獲得的訂閱人數",
    "流失的訂閱人數",
    "喜歡次數",
    "喜歡的比例 (vs. 不喜歡) (%)",
    "不喜歡次數",
    "分享次數",
    "已新增留言",
    "YouTube Premium 觀看次數",
    "YouTube Premium 觀看時間 (小時)",
    "觀看次數",
    "觀看時間 (小時)",
    "訂閱人數",
    "預估收益 (TWD)",
    "平均觀看時間",
    "曝光次數",
    "曝光點閱率 (%)",
]


class BuildMaymeiTitleBenchmarkTests(unittest.TestCase):
    def write_export(self, rows: list[list[str]]) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "studio-export"
        path.mkdir()
        csv_path = path / "表格資料.csv"
        with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(HEADER)
            writer.writerows(rows)
        return path

    def test_builds_sanitized_title_dataset_from_studio_table(self) -> None:
        source = self.write_export(
            [
                [
                    "總計",
                    "",
                    "",
                    "",
                    "1234",
                    "40.9",
                    "74.75",
                    "",
                    "",
                    "0",
                    "0",
                    "50",
                    "5",
                    "99",
                    "97.3",
                    "1",
                    "10",
                    "2",
                    "0",
                    "0",
                    "1300",
                    "100.0",
                    "45",
                    "9999.9",
                    "0:02:42",
                    "10000",
                    "7.74",
                ],
                [
                    " -HkqawYpHWQ",
                    "【黑神話悟空】最強BOSS排名TOP10 誰才是最難打?",
                    "Aug 30, 2024",
                    "592",
                    "276280",
                    "43.87",
                    "50",
                    "",
                    "",
                    "13",
                    "8390",
                    "713",
                    "26",
                    "2204",
                    "95.83",
                    "96",
                    "882",
                    "366",
                    "93194",
                    "6983.4012",
                    "276281",
                    "19929.616",
                    "687",
                    "17339.388",
                    "0:04:19",
                    "3842512",
                    "5.51",
                ],
                [
                    "short123",
                    "【黑神話：悟空】最悲慘的妖怪 #shorts",
                    "Sep 7, 2024",
                    "58",
                    "275820",
                    "90",
                    "88.56",
                    "",
                    "",
                    "0",
                    "0",
                    "93",
                    "5",
                    "4890",
                    "97.06",
                    "148",
                    "395",
                    "215",
                    "117762",
                    "1473.3779",
                    "321754",
                    "4002.5228",
                    "88",
                    "1081.473",
                    "0:00:52",
                    "4126310",
                    "3.04",
                ],
            ]
        )

        dataset = build_dataset(source, generated_at="2026-05-08T00:00:00+00:00")

        self.assertEqual(dataset["summary"]["total_videos"], 2)
        self.assertEqual(dataset["summary"]["long_videos"], 1)
        self.assertEqual(dataset["summary"]["short_videos"], 1)
        self.assertEqual(dataset["summary"]["trimmed_video_ids"], 1)
        long_record = dataset["records"][0]
        self.assertEqual(long_record["video_id"], "-HkqawYpHWQ")
        self.assertEqual(long_record["format"], "long")
        self.assertEqual(long_record["published_at"], "2024-08-30")
        self.assertEqual(long_record["formula"], "排行 top list")
        self.assertEqual(long_record["game"], "黑神話悟空")
        self.assertEqual(long_record["avg_view_duration_seconds"], 259)
        self.assertAlmostEqual(long_record["ctr_percent"], 5.51)
        self.assertAlmostEqual(long_record["views_per_impression"], 276281 / 3842512)
        self.assertIn("trimmed_video_id", long_record["data_quality_flags"])
        self.assertNotIn("revenue", long_record)

    def test_render_markdown_reports_coverage_quality_and_top_ctr(self) -> None:
        source = self.write_export(
            [
                [
                    "總計",
                    "",
                    "",
                    "",
                    "100",
                    "40",
                    "",
                    "",
                    "",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "100",
                    "10",
                    "0",
                    "0",
                    "0:02:00",
                    "1000",
                    "5",
                ],
                [
                    "abc123",
                    "【超詳細】風之神殿完全攻略",
                    "May 30, 2023",
                    "243",
                    "110726",
                    "54.23",
                    "60",
                    "",
                    "",
                    "0",
                    "0",
                    "100",
                    "1",
                    "3000",
                    "97.57",
                    "78",
                    "1000",
                    "206",
                    "0",
                    "0",
                    "110726",
                    "3790.1042",
                    "99",
                    "1200.5",
                    "0:02:10",
                    "367180",
                    "19.04",
                ],
            ]
        )

        markdown = render_markdown(build_dataset(source, generated_at="2026-05-08T00:00:00+00:00"))

        self.assertIn("# Maymei Title Benchmark", markdown)
        self.assertIn("Long videos: `1`", markdown)
        self.assertIn("CTR: `19.04%`", markdown)
        self.assertIn("公式：`完整攻略`", markdown)

    def test_cli_runs_from_repo_root(self) -> None:
        source = self.write_export(
            [
                [
                    "總計",
                    "",
                    "",
                    "",
                    "100",
                    "40",
                    "",
                    "",
                    "",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "100",
                    "10",
                    "0",
                    "0",
                    "0:02:00",
                    "1000",
                    "5",
                ],
                [
                    "abc123",
                    "【寶可夢ZA】新手開局必看攻略",
                    "Oct 16, 2025",
                    "531",
                    "206096",
                    "42.81",
                    "0",
                    "",
                    "",
                    "17",
                    "12030",
                    "1595",
                    "24",
                    "2127",
                    "96.95",
                    "67",
                    "1071",
                    "35",
                    "75410",
                    "4889.7344",
                    "206097",
                    "13012.5022",
                    "1571",
                    "12246.15",
                    "0:03:47",
                    "2106452",
                    "6.82",
                ],
            ]
        )
        output_dir = source / "out"
        json_output = output_dir / "benchmark.json"
        markdown_output = output_dir / "benchmark.md"

        result = subprocess.run(
            [
                sys.executable,
                "scripts/build_maymei_title_benchmark.py",
                str(source),
                "--json-output",
                str(json_output),
                "--markdown-output",
                str(markdown_output),
            ],
            cwd=Path(__file__).resolve().parents[1],
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json_output.exists())
        self.assertTrue(markdown_output.exists())


if __name__ == "__main__":
    unittest.main()
