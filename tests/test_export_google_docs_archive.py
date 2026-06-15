import unittest

from scripts.export_google_docs_archive import (
    build_output_filename,
    load_export_metadata,
    sanitize_filename,
)


class ExportGoogleDocsArchiveTests(unittest.TestCase):
    def test_sanitize_filename_replaces_windows_invalid_chars(self) -> None:
        self.assertEqual(
            sanitize_filename('【寶可夢】買之前: 10件/你需要知道的事情?'),
            '【寶可夢】買之前_ 10件_你需要知道的事情_',
        )

    def test_sanitize_filename_falls_back_for_empty_name(self) -> None:
        self.assertEqual(sanitize_filename("   "), "Untitled")

    def test_build_output_filename_prefixes_index_and_extension(self) -> None:
        self.assertEqual(
            build_output_filename(12, "我的文稿"),
            "0012 - 我的文稿.docx",
        )

    def test_load_export_metadata_supports_corpus_shape(self) -> None:
        import json
        from pathlib import Path
        import tempfile

        payload = {
            "records": [
                {
                    "document_id": "doc123",
                    "title": "我的影片稿",
                    "modified_time": "2026-03-31T00:00:00Z",
                    "web_view_link": "https://docs.google.com/document/d/doc123/edit",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "records.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(
                load_export_metadata(path),
                [
                    {
                        "id": "doc123",
                        "name": "我的影片稿",
                        "modifiedTime": "2026-03-31T00:00:00Z",
                        "webViewLink": "https://docs.google.com/document/d/doc123/edit",
                    }
                ],
            )


if __name__ == "__main__":
    unittest.main()
