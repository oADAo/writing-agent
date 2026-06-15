import json
import subprocess
import unittest
from unittest.mock import patch

from scripts.opencli_research import SearchResult, SearchTask, run_search_task, search_youtube_data_api


class YouTubeApiFallbackTests(unittest.TestCase):
    def make_task(self, *, shorts_only: bool = False) -> SearchTask:
        return SearchTask(
            provider="youtube",
            language="en",
            site_label="YouTube Shorts" if shorts_only else "YouTube",
            query="Pokopia shorts" if shorts_only else "Pokopia guide",
            limit=5,
            note="test task",
            evidence_family="video",
            shorts_only=shorts_only,
            url_must_contain=("/shorts/",) if shorts_only else (),
        )

    @patch("scripts.opencli_research.attempt_youtube_api_fallback")
    @patch("scripts.opencli_research.subprocess.run")
    def test_run_search_task_uses_fallback_when_opencli_youtube_fails(self, mock_run, mock_fallback) -> None:
        task = self.make_task()
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="boom")
        mock_fallback.return_value = SearchResult(
            task=task,
            command='opencli youtube search "Pokopia guide" --limit 5 -f json',
            ok=True,
            records=[{"title": "API result", "url": "https://www.youtube.com/watch?v=demo"}],
            backend="youtube-data-api",
            fallback_reason="opencli command failed",
        )

        result = run_search_task(task, opencli_bin="opencli")

        self.assertTrue(result.ok)
        self.assertEqual(result.backend, "youtube-data-api")
        self.assertEqual(result.fallback_reason, "opencli command failed")
        mock_fallback.assert_called_once()

    @patch("scripts.opencli_research.attempt_youtube_api_fallback")
    @patch("scripts.opencli_research.subprocess.run")
    def test_run_search_task_uses_fallback_when_shorts_filter_removes_opencli_hits(self, mock_run, mock_fallback) -> None:
        task = self.make_task(shorts_only=True)
        mock_run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=json.dumps(
                [{"title": "Long video", "url": "https://www.youtube.com/watch?v=notshort"}],
                ensure_ascii=False,
            ),
            stderr="",
        )
        mock_fallback.return_value = SearchResult(
            task=task,
            command='opencli youtube search "Pokopia shorts" --limit 5 -f json',
            ok=True,
            records=[{"title": "Short result", "url": "https://www.youtube.com/shorts/demo"}],
            backend="youtube-data-api",
            fallback_reason="opencli returned no retained hits",
        )

        result = run_search_task(task, opencli_bin="opencli")

        self.assertTrue(result.ok)
        self.assertEqual(result.records[0]["url"], "https://www.youtube.com/shorts/demo")
        mock_fallback.assert_called_once()

    @patch("scripts.opencli_research.attempt_youtube_api_fallback")
    @patch("scripts.opencli_research.subprocess.run")
    def test_run_search_task_does_not_fallback_for_non_youtube_providers(self, mock_run, mock_fallback) -> None:
        task = SearchTask(
            provider="google",
            language="en",
            site_label="Google",
            query="Pokopia guide",
            limit=5,
            note="test task",
            evidence_family="guide",
        )
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="boom")

        result = run_search_task(task, opencli_bin="opencli")

        self.assertFalse(result.ok)
        mock_fallback.assert_not_called()

    @patch("scripts.opencli_research.fetch_json")
    def test_search_youtube_data_api_normalizes_video_fields(self, mock_fetch_json) -> None:
        task = self.make_task()
        mock_fetch_json.side_effect = [
            {
                "items": [
                    {
                        "id": {"videoId": "abc123"},
                        "snippet": {
                            "title": "Pokopia Guide",
                            "channelTitle": "May Story",
                            "publishedAt": "2026-04-16T01:02:03Z",
                        },
                    }
                ]
            },
            {
                "items": [
                    {
                        "id": "abc123",
                        "statistics": {"viewCount": "1953"},
                        "contentDetails": {"duration": "PT5M9S"},
                    }
                ]
            },
        ]

        records = search_youtube_data_api(task, api_key="demo-key")

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["title"], "Pokopia Guide")
        self.assertEqual(records[0]["channel"], "May Story")
        self.assertEqual(records[0]["duration"], "5:09")
        self.assertEqual(records[0]["views"], "觀看次數：1,953次")
        self.assertEqual(records[0]["url"], "https://www.youtube.com/watch?v=abc123")

    @patch("scripts.opencli_research.fetch_json")
    def test_search_youtube_data_api_builds_shorts_urls_for_short_candidates(self, mock_fetch_json) -> None:
        task = self.make_task(shorts_only=True)
        mock_fetch_json.side_effect = [
            {
                "items": [
                    {
                        "id": {"videoId": "short123"},
                        "snippet": {
                            "title": "Pokopia Shorts",
                            "channelTitle": "May Story",
                            "publishedAt": "2026-04-16T01:02:03Z",
                        },
                    }
                ]
            },
            {
                "items": [
                    {
                        "id": "short123",
                        "statistics": {"viewCount": "88"},
                        "contentDetails": {"duration": "PT59S"},
                    }
                ]
            },
        ]

        records = search_youtube_data_api(task, api_key="demo-key")

        self.assertEqual(records[0]["url"], "https://www.youtube.com/shorts/short123")


if __name__ == "__main__":
    unittest.main()
