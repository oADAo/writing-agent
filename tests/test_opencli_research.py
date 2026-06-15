import unittest

from scripts.opencli_research import (
    SearchResult,
    SearchTask,
    build_opencli_args,
    build_shorts_tasks,
    build_topic_tasks,
    filter_records_for_task,
    render_query_log,
)


class OpenCliResearchTests(unittest.TestCase):
    def test_build_topic_tasks_cover_broader_platform_matrix(self) -> None:
        tasks = build_topic_tasks({"zh": "寶可夢 Pokopia", "jp": "ぽこポケ", "en": "Pokopia"}, limit=8, breadth="broad")

        providers = {task.provider for task in tasks}
        google_queries = [task.query for task in tasks if task.provider == "google"]

        self.assertIn("youtube", providers)
        self.assertIn("bilibili", providers)
        self.assertIn("reddit", providers)
        self.assertTrue(any("forum.gamer.com.tw" in query for query in google_queries))
        self.assertTrue(any("game8.jp" in query for query in google_queries))
        self.assertTrue(any("gamewith.jp" in query for query in google_queries))
        self.assertTrue(any("steamcommunity.com" in query for query in google_queries))
        self.assertTrue(any("threads.net" in query for query in google_queries))

    def test_build_topic_tasks_max_adds_twitter(self) -> None:
        tasks = build_topic_tasks({"zh": "寶可夢 Pokopia", "jp": "", "en": "Pokopia"}, limit=5, breadth="max")

        providers = {task.provider for task in tasks}

        self.assertIn("twitter", providers)

    def test_build_shorts_tasks_include_required_platform_fallbacks(self) -> None:
        tasks = build_shorts_tasks({"zh": "寶可夢 Pokopia", "jp": "ぽこポケ", "en": "Pokopia"}, limit=8, breadth="broad")

        providers = [task.provider for task in tasks]
        google_queries = [task.query for task in tasks if task.provider == "google"]

        self.assertIn("youtube", providers)
        self.assertIn("tiktok", providers)
        self.assertIn("bilibili", providers)
        self.assertTrue(any("instagram.com/reel/" in query for query in google_queries))
        self.assertTrue(any("forum.gamer.com.tw" in query for query in google_queries))
        self.assertTrue(any("tiktok.com" in query for query in google_queries))
        self.assertTrue(any("threads.net" in query for query in google_queries))

    def test_filter_records_for_shorts_keeps_only_short_urls(self) -> None:
        task = SearchTask(
            provider="youtube",
            language="en",
            site_label="YouTube Shorts",
            query="Pokopia shorts",
            limit=10,
            note="shorts only",
            evidence_family="video",
            shorts_only=True,
            url_must_contain=("/shorts/",),
        )
        records = [
            {"title": "long", "url": "https://www.youtube.com/watch?v=abc"},
            {"title": "short", "url": "https://www.youtube.com/shorts/xyz"},
        ]

        filtered = filter_records_for_task(task, records)

        self.assertEqual(filtered, [records[1]])

    def test_build_opencli_args_for_google_includes_lang_and_json_output(self) -> None:
        task = SearchTask(
            provider="google",
            language="jp",
            site_label="Game8",
            query="site:game8.jp ぽこポケ 攻略",
            limit=12,
            note="jp guide site",
            evidence_family="guide",
        )

        args = build_opencli_args(task, opencli_bin="opencli")

        self.assertEqual(args[:3], ["opencli", "google", "search"])
        self.assertIn("--lang", args)
        self.assertIn("ja", args)
        self.assertEqual(args[-2:], ["-f", "json"])

    def test_build_opencli_args_for_twitter_uses_top_filter(self) -> None:
        task = SearchTask(
            provider="twitter",
            language="en",
            site_label="X / Twitter",
            query="Pokopia",
            limit=6,
            note="social validation",
            evidence_family="community",
            tier="validation",
        )

        args = build_opencli_args(task, opencli_bin="opencli")

        self.assertEqual(args[:3], ["opencli", "twitter", "search"])
        self.assertIn("--filter", args)
        self.assertIn("top", args)

    def test_render_query_log_tracks_family_and_tier(self) -> None:
        task = SearchTask(
            provider="youtube",
            language="zh",
            site_label="YouTube",
            query="寶可夢 Pokopia 攻略",
            limit=10,
            note="中文長片主題簇",
            evidence_family="video",
            tier="core",
        )
        result = SearchResult(
            task=task,
            command='opencli youtube search "寶可夢 Pokopia 攻略" --limit 10 -f json',
            ok=True,
            records=[{"title": "影片 A", "url": "https://www.youtube.com/watch?v=demo", "channel": "玫玫物語"}],
        )

        rendered = render_query_log("topic", {"zh": "寶可夢 Pokopia", "jp": "", "en": ""}, [result], breadth="broad")

        self.assertIn("Evidence family:", rendered)
        self.assertIn("Search tier:", rendered)
        self.assertIn("opencli command:", rendered)
        self.assertIn("Included in final conclusion?:", rendered)


if __name__ == "__main__":
    unittest.main()
