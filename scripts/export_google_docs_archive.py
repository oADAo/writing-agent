from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from scripts.google_docs_corpus import (
    ensure_access_token,
    extract_drive_id,
    list_google_docs,
    load_client,
)


DOCX_EXPORT_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
INVALID_FILENAME_CHARS = '<>:"/\\|?*'
SAFE_FILENAME_RE = re.compile(r"\s+")


def sanitize_filename(name: str, *, max_length: int = 120) -> str:
    cleaned = "".join("_" if char in INVALID_FILENAME_CHARS else char for char in name)
    cleaned = SAFE_FILENAME_RE.sub(" ", cleaned).strip(" .")
    if not cleaned:
        cleaned = "Untitled"
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip(" .")
    return cleaned or "Untitled"


def build_output_filename(index: int, title: str) -> str:
    return f"{index:04d} - {sanitize_filename(title)}.docx"


def load_export_metadata(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    source_records = payload.get("records", payload)
    items: list[dict[str, Any]] = []
    for record in source_records:
        items.append(
            {
                "id": record.get("document_id") or record.get("id"),
                "name": record.get("title") or record.get("name") or "",
                "modifiedTime": record.get("modified_time") or record.get("modifiedTime") or "",
                "webViewLink": record.get("web_view_link") or record.get("webViewLink") or "",
            }
        )
    return [item for item in items if item.get("id")]


def google_bytes_get(url: str, *, access_token: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def google_bytes_get_with_retry(url: str, *, access_token: str, retries: int = 3) -> bytes:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            return google_bytes_get(url, access_token=access_token)
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504} or attempt == retries - 1:
                raise
        except urllib.error.URLError as exc:
            last_error = exc
            if attempt == retries - 1:
                raise
        time.sleep(1.5 * (attempt + 1))
    if last_error is not None:
        raise last_error
    raise RuntimeError("Unknown Google export failure.")


def export_google_doc_as_docx(metadata: dict[str, Any], *, access_token: str, output_path: Path) -> None:
    file_id = metadata["id"]
    params = urllib.parse.urlencode({"mimeType": DOCX_EXPORT_MIME})
    url = f"https://www.googleapis.com/drive/v3/files/{urllib.parse.quote(file_id)}/export?{params}"
    payload = google_bytes_get_with_retry(url, access_token=access_token)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(payload)


def write_manifest(records: list[dict[str, Any]], path: Path) -> None:
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def write_manifest_csv(records: list[dict[str, Any]], path: Path) -> None:
    fieldnames = [
        "index",
        "title",
        "document_id",
        "modified_time",
        "web_view_link",
        "filename",
        "status",
        "error",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)


def write_failed_shortcut(record: dict[str, Any], directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    base_name = Path(record["filename"]).stem
    shortcut_path = directory / f"{base_name}.url"
    shortcut_path.write_text(
        "[InternetShortcut]\n"
        f"URL={record['web_view_link']}\n",
        encoding="utf-8",
    )


def build_archive(zip_output: Path, source_dir: Path) -> None:
    zip_output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_output, "w", ZIP_DEFLATED) as archive:
        for file_path in sorted(source_dir.rglob("*")):
            if file_path.is_file():
                archive.write(file_path, arcname=file_path.relative_to(source_dir.parent))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    today = datetime.now(UTC).date().isoformat()
    default_output_dir = repo_root / "workspace" / "source-docs" / f"google-docs-export-{today}"
    default_zip_output = repo_root / "workspace" / "source-docs" / f"google-docs-export-{today}.zip"

    parser = argparse.ArgumentParser(
        description="Export all accessible Google Docs as DOCX files and package them into a zip archive."
    )
    parser.add_argument("--client-secret", required=True, help="Path to the Google OAuth client secret JSON.")
    parser.add_argument("--token-path", default=str(repo_root / ".auth" / "google_docs_token.json"))
    parser.add_argument("--folder", help="Drive folder ID or folder URL to limit the export.")
    parser.add_argument("--limit", type=int, help="Optional max number of Google Docs to export. Defaults to all.")
    parser.add_argument("--records-json", help="Optional JSON file containing a filtered records list to export.")
    parser.add_argument("--force-reauth", action="store_true")
    parser.add_argument("--output-dir", default=str(default_output_dir))
    parser.add_argument("--zip-output", default=str(default_zip_output))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    client = load_client(Path(args.client_secret))
    access_token = ensure_access_token(
        client,
        token_path=Path(args.token_path),
        force_reauth=args.force_reauth,
    )

    folder_id = extract_drive_id(args.folder)
    if args.records_json:
        docs = load_export_metadata(Path(args.records_json))
    else:
        docs = list_google_docs(
            access_token=access_token,
            folder_id=folder_id,
            limit=args.limit,
        )

    output_dir = Path(args.output_dir)
    docs_dir = output_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    manifest_records: list[dict[str, Any]] = []
    for index, item in enumerate(docs, start=1):
        filename = build_output_filename(index, item.get("name", item["id"]))
        output_path = docs_dir / filename
        record = {
            "index": index,
            "title": item.get("name", ""),
            "document_id": item["id"],
            "modified_time": item.get("modifiedTime", ""),
            "web_view_link": item.get("webViewLink", ""),
            "filename": filename,
            "status": "ok",
            "error": "",
        }
        try:
            export_google_doc_as_docx(item, access_token=access_token, output_path=output_path)
        except Exception as exc:
            record["status"] = "error"
            record["error"] = str(exc)
            if record["web_view_link"]:
                write_failed_shortcut(record, output_dir / "failed-links")
        manifest_records.append(record)

    write_manifest(manifest_records, output_dir / "manifest.json")
    write_manifest_csv(manifest_records, output_dir / "manifest.csv")
    build_archive(Path(args.zip_output), output_dir)

    success_count = sum(1 for item in manifest_records if item["status"] == "ok")
    error_count = len(manifest_records) - success_count
    print(f"Exported {success_count} Google Docs")
    print(f"Failed {error_count} Google Docs")
    print(f"Output folder: {output_dir}")
    print(f"Zip archive: {args.zip_output}")
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
