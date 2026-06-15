import unittest

from scripts.google_docs_corpus import (
    build_authorization_url,
    build_drive_query,
    extract_drive_id,
    extract_paragraph_texts,
    find_intro_line,
    GoogleInstalledClient,
)


class GoogleDocsCorpusTests(unittest.TestCase):
    def test_extract_drive_id_from_folder_url(self) -> None:
        value = "https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWxYz?usp=sharing"
        self.assertEqual(extract_drive_id(value), "1AbCdEfGhIjKlMnOpQrStUvWxYz")

    def test_extract_drive_id_from_raw_id(self) -> None:
        self.assertEqual(extract_drive_id("1AbCdEfGhIjKlMnOpQrStUvWxYz"), "1AbCdEfGhIjKlMnOpQrStUvWxYz")

    def test_build_drive_query_without_folder(self) -> None:
        self.assertEqual(
            build_drive_query(),
            "mimeType='application/vnd.google-apps.document' and trashed=false",
        )

    def test_build_drive_query_with_folder(self) -> None:
        self.assertIn("'folder123' in parents", build_drive_query("folder123"))

    def test_build_authorization_url_contains_expected_params(self) -> None:
        client = GoogleInstalledClient(
            client_id="client-id",
            client_secret="secret",
            auth_uri="https://accounts.example.com/auth",
            token_uri="https://accounts.example.com/token",
        )
        url = build_authorization_url(client, redirect_uri="http://localhost:8765/")
        self.assertIn("client_id=client-id", url)
        self.assertIn("redirect_uri=http%3A%2F%2Flocalhost%3A8765%2F", url)
        self.assertIn("access_type=offline", url)
        self.assertIn("documents.readonly", url)

    def test_extract_paragraph_texts_handles_nested_structures(self) -> None:
        payload = {
            "body": {
                "content": [
                    {
                        "paragraph": {
                            "elements": [
                                {"textRun": {"content": "第一段內容\n"}},
                            ]
                        }
                    },
                    {
                        "table": {
                            "tableRows": [
                                {
                                    "tableCells": [
                                        {
                                            "content": [
                                                {
                                                    "paragraph": {
                                                        "elements": [
                                                            {"textRun": {"content": "表格內文\n"}}
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                ]
            }
        }
        self.assertEqual(extract_paragraph_texts(payload), ["第一段內容", "表格內文"])

    def test_find_intro_line_detects_maymei_intro(self) -> None:
        paragraphs = [
            "前言",
            "大家好~這裡是玫玫物語",
            "這部影片要來分享寶可夢攻略",
        ]
        self.assertEqual(find_intro_line(paragraphs), "大家好~這裡是玫玫物語")


if __name__ == "__main__":
    unittest.main()
