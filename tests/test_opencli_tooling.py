import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts.opencli_tooling import (
    CommandResult,
    doctor_is_ok,
    fetch_youtube_transcript,
    sanitize_filename,
)


class OpenCliToolingTests(unittest.TestCase):
    def test_doctor_is_ok_requires_connectivity_success(self) -> None:
        result = CommandResult(
            command="opencli doctor",
            ok=True,
            returncode=0,
            stdout="[OK] Connectivity: connected in 0.1s\nEverything looks good!",
        )

        self.assertTrue(doctor_is_ok(result))

    def test_doctor_is_ok_rejects_disconnected_profile(self) -> None:
        result = CommandResult(
            command="opencli doctor",
            ok=False,
            returncode=69,
            stderr='Browser profile "58ku8cmx" is not connected',
        )

        self.assertFalse(doctor_is_ok(result))

    def test_sanitize_filename_keeps_safe_ascii(self) -> None:
        self.assertEqual(sanitize_filename("Forza Horizon 6: AE86 FE?!"), "Forza-Horizon-6-AE86-FE")

    @patch("scripts.opencli_tooling.resolve_yt_dlp_binary", return_value="yt-dlp")
    @patch("scripts.opencli_tooling.resolve_opencli_binary", return_value="opencli")
    @patch("scripts.opencli_tooling.run_command")
    def test_fetch_youtube_transcript_tries_explicit_lang_before_auto(self, mock_run, _opencli, _yt_dlp) -> None:
        mock_run.return_value = CommandResult(
            command="opencli youtube transcript demo --lang en -f md",
            ok=True,
            returncode=0,
            stdout="| timestamp | text |\n| --- | --- |\n| 0:00 | " + ("hello " * 30),
        )

        with TemporaryDirectory() as tmp:
            result = fetch_youtube_transcript(
                "https://www.youtube.com/watch?v=demo",
                Path(tmp),
                label="demo",
                repo_root=Path(tmp),
                languages=("en",),
            )

        self.assertTrue(result.ok)
        self.assertEqual(result.method, "opencli-youtube-transcript")
        self.assertIn("--lang en", result.attempts[0].command)

    @patch("scripts.opencli_tooling.resolve_yt_dlp_binary", return_value="yt-dlp")
    @patch("scripts.opencli_tooling.resolve_opencli_binary", return_value="opencli")
    @patch("scripts.opencli_tooling.run_command")
    def test_fetch_youtube_transcript_falls_back_to_yt_dlp(self, mock_run, _opencli, _yt_dlp) -> None:
        def fake_run(args, *, cwd, timeout):
            command = " ".join(args)
            if args[0] == "opencli":
                return CommandResult(command=command, ok=False, returncode=1, stderr="Caption URL returned empty response")
            output_dir = Path(args[args.index("-o") + 1]).parent
            (output_dir / "demo.en.srt").write_text("1\n00:00:00,000 --> 00:00:01,000\nhello\n", encoding="utf-8")
            return CommandResult(command=command, ok=True, returncode=0, stdout=str(output_dir / "demo.en.srt"))

        mock_run.side_effect = fake_run

        with TemporaryDirectory() as tmp:
            result = fetch_youtube_transcript(
                "https://www.youtube.com/watch?v=demo",
                Path(tmp),
                label="demo",
                repo_root=Path(tmp),
                languages=("en",),
            )

        self.assertTrue(result.ok)
        self.assertEqual(result.method, "yt-dlp-subs")
        self.assertTrue(any(path.endswith("demo.en.srt") for path in result.output_files))


if __name__ == "__main__":
    unittest.main()
