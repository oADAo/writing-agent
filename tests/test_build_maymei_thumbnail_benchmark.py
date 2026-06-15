import tempfile
import unittest
from pathlib import Path

from scripts.build_maymei_thumbnail_benchmark import (
    build_dataset,
    pick_best_thumbnail,
    render_markdown,
)


class BuildMaymeiThumbnailBenchmarkTests(unittest.TestCase):
    def test_picks_largest_thumbnail(self) -> None:
        thumbnails = [
            {"url": "https://example.test/small.jpg", "width": 120, "height": 90},
            {"url": "https://example.test/large.jpg", "width": 1280, "height": 720},
            {"url": "https://example.test/medium.jpg", "width": 640, "height": 360},
        ]

        self.assertEqual(pick_best_thumbnail(thumbnails), "https://example.test/large.jpg")

    def test_builds_thumbnail_dataset_matched_to_title_benchmark(self) -> None:
        channel_records = [
            {
                "id": "abc123",
                "title": "【測試】新手開局必看攻略",
                "url": "https://www.youtube.com/watch?v=abc123",
                "duration": 620,
                "thumbnails": [
                    {"url": "https://example.test/abc-small.jpg", "width": 120, "height": 90},
                    {"url": "https://example.test/abc-large.jpg", "width": 1280, "height": 720},
                ],
            },
            {
                "id": "short123",
                "title": "短片",
                "url": "https://www.youtube.com/watch?v=short123",
                "duration": 45,
                "thumbnails": [
                    {"url": "https://example.test/short.jpg", "width": 1280, "height": 720},
                ],
            },
        ]
        title_benchmark = {
            "records": [
                {
                    "video_id": "abc123",
                    "title": "【測試】新手開局必看攻略",
                    "format": "long",
                    "formula": "新手技巧清單",
                    "game": "測試遊戲",
                    "ctr_percent": 7.5,
                    "impressions": 100000,
                    "view_count": 9000,
                    "avg_view_percent": 42.0,
                    "data_quality_flags": [],
                }
            ]
        }

        dataset = build_dataset(
            channel_records,
            title_benchmark,
            channel_url="https://www.youtube.com/@maymei_gaming/videos",
            generated_at="2026-05-08T00:00:00+00:00",
            thumbnail_dir=Path("workspace/memory/style-corpus/thumbnails"),
            download=False,
        )

        self.assertEqual(dataset["summary"]["total_channel_records"], 2)
        self.assertEqual(dataset["summary"]["matched_to_title_benchmark"], 1)
        self.assertEqual(dataset["summary"]["long_videos"], 1)
        self.assertEqual(dataset["summary"]["short_videos"], 1)
        record = dataset["records"][0]
        self.assertEqual(record["video_id"], "abc123")
        self.assertEqual(record["thumbnail_url"], "https://example.test/abc-large.jpg")
        self.assertEqual(record["thumbnail_text"], "")
        self.assertEqual(record["thumbnail_text_source"], "pending_manual_review")
        self.assertEqual(record["ctr_percent"], 7.5)
        self.assertNotIn("revenue", record)

    def test_render_markdown_includes_review_columns(self) -> None:
        dataset = {
            "source_channel_url": "https://www.youtube.com/@maymei_gaming/videos",
            "generated_at": "2026-05-08T00:00:00+00:00",
            "summary": {
                "total_channel_records": 1,
                "matched_to_title_benchmark": 1,
                "long_videos": 1,
                "short_videos": 0,
                "downloaded_thumbnails": 0,
                "annotated_thumbnail_texts": 1,
            },
            "records": [
                {
                    "video_id": "abc123",
                    "title": "【測試】新手開局必看攻略",
                    "format": "long",
                    "formula": "新手技巧清單",
                    "game": "測試遊戲",
                    "ctr_percent": 7.5,
                    "impressions": 100000,
                    "view_count": 9000,
                    "thumbnail_url": "https://example.test/abc.jpg",
                    "thumbnail_path": "workspace/memory/style-corpus/thumbnails/abc123.jpg",
                    "thumbnail_text": "",
                    "thumbnail_text_source": "pending_manual_review",
                }
            ],
        }

        markdown = render_markdown(dataset)

        self.assertIn("# Maymei Thumbnail Benchmark", markdown)
        self.assertIn("Thumbnail text", markdown)
        self.assertIn("Annotated thumbnail text rows: `1`", markdown)
        self.assertIn("pending_manual_review", markdown)

    def test_applies_manual_thumbnail_text_annotations(self) -> None:
        channel_records = [
            {
                "id": "abc123",
                "title": "FH6 beginner guide",
                "url": "https://www.youtube.com/watch?v=abc123",
                "duration": 620,
                "thumbnails": [
                    {"url": "https://example.test/abc-large.jpg", "width": 1280, "height": 720},
                ],
            }
        ]
        title_benchmark = {
            "records": [
                {
                    "video_id": "abc123",
                    "title": "FH6 beginner guide",
                    "format": "long",
                    "formula": "newbie_guide",
                    "game": "forza-horizon-6",
                    "ctr_percent": 7.5,
                    "impressions": 100000,
                    "view_count": 9000,
                    "avg_view_percent": 42.0,
                }
            ]
        }
        annotations = {
            "abc123": {
                "thumbnail_text": "newbie 10 tips",
                "thumbnail_text_source": "manual_youtube_review",
                "thumbnail_notes": "Read from channel thumbnail.",
            }
        }

        dataset = build_dataset(
            channel_records,
            title_benchmark,
            channel_url="https://www.youtube.com/@maymei_gaming/videos",
            generated_at="2026-05-08T00:00:00+00:00",
            thumbnail_dir=Path("workspace/memory/style-corpus/thumbnails"),
            download=False,
            annotations=annotations,
        )

        record = dataset["records"][0]
        self.assertEqual(record["thumbnail_text"], "newbie 10 tips")
        self.assertEqual(record["thumbnail_text_source"], "manual_youtube_review")
        self.assertEqual(record["thumbnail_notes"], "Read from channel thumbnail.")
        self.assertEqual(dataset["summary"]["annotated_thumbnail_texts"], 1)


if __name__ == "__main__":
    unittest.main()
