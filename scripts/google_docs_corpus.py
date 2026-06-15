from __future__ import annotations

import argparse
import json
import os
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
import urllib.error

from scripts.build_article_corpus_index import (
    detect_voice_markers,
    pick_opening_promise,
    classify_formula,
    classify_primary_category,
)


GOOGLE_DOC_MIME = "application/vnd.google-apps.document"
GOOGLE_SCOPES = (
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
)


@dataclass(frozen=True)
class GoogleInstalledClient:
    client_id: str
    client_secret: str
    auth_uri: str
    token_uri: str


@dataclass
class GoogleDocRecord:
    document_id: str
    title: str
    modified_time: str
    web_view_link: str
    primary_category: str
    formula: str
    char_count: int
    paragraph_count: int
    intro_line: str
    has_maymei_intro: bool
    opening_promise: str
    voice_markers: list[str]
    fetch_error: str | None = None


def load_client(path: Path) -> GoogleInstalledClient:
    payload = json.loads(path.read_text(encoding="utf-8"))
    installed = payload.get("installed") or {}
    required = ("client_id", "client_secret", "auth_uri", "token_uri")
    missing = [key for key in required if not installed.get(key)]
    if missing:
        raise ValueError(f"Client secret file is missing required fields: {', '.join(missing)}")
    return GoogleInstalledClient(
        client_id=installed["client_id"],
        client_secret=installed["client_secret"],
        auth_uri=installed["auth_uri"],
        token_uri=installed["token_uri"],
    )


def extract_drive_id(value: str | None) -> str | None:
    if not value:
        return None
    raw = value.strip()
    if not raw:
        return None
    for marker in ("/folders/", "/d/"):
        if marker in raw:
            return raw.split(marker, 1)[1].split("/", 1)[0].split("?", 1)[0]
    if "://" not in raw and "/" not in raw and len(raw) >= 10:
        return raw
    return None


def build_drive_query(folder_id: str | None = None) -> str:
    clauses = [f"mimeType='{GOOGLE_DOC_MIME}'", "trashed=false"]
    if folder_id:
        clauses.append(f"'{folder_id}' in parents")
    return " and ".join(clauses)


def build_authorization_url(
    client: GoogleInstalledClient,
    *,
    redirect_uri: str,
    scopes: tuple[str, ...] = GOOGLE_SCOPES,
    state: str = "writing-agent-google-docs",
) -> str:
    params = {
        "client_id": client.client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "consent",
        "state": state,
    }
    return f"{client.auth_uri}?{urllib.parse.urlencode(params)}"


def load_saved_token(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_token(path: Path, token_payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(token_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def token_is_valid(token_payload: dict[str, Any] | None) -> bool:
    if not token_payload or not token_payload.get("access_token"):
        return False
    expires_at = token_payload.get("expires_at")
    if not expires_at:
        return False
    try:
        expiry = datetime.fromisoformat(expires_at)
    except ValueError:
        return False
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=UTC)
    return expiry > datetime.now(UTC) + timedelta(seconds=60)


def normalize_token_payload(response_payload: dict[str, Any], *, fallback_refresh_token: str | None = None) -> dict[str, Any]:
    expires_in = int(response_payload.get("expires_in", 0))
    expires_at = (datetime.now(UTC) + timedelta(seconds=expires_in)).isoformat()
    refresh_token = response_payload.get("refresh_token") or fallback_refresh_token
    return {
        "access_token": response_payload["access_token"],
        "refresh_token": refresh_token,
        "scope": response_payload.get("scope", " ".join(GOOGLE_SCOPES)),
        "token_type": response_payload.get("token_type", "Bearer"),
        "expires_at": expires_at,
    }


def post_form(url: str, data: dict[str, str]) -> dict[str, Any]:
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return json.loads(response.read().decode(charset))


def exchange_code_for_token(client: GoogleInstalledClient, *, code: str, redirect_uri: str) -> dict[str, Any]:
    response_payload = post_form(
        client.token_uri,
        {
            "code": code,
            "client_id": client.client_id,
            "client_secret": client.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    return normalize_token_payload(response_payload)


def refresh_access_token(client: GoogleInstalledClient, *, refresh_token: str) -> dict[str, Any]:
    response_payload = post_form(
        client.token_uri,
        {
            "client_id": client.client_id,
            "client_secret": client.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )
    return normalize_token_payload(response_payload, fallback_refresh_token=refresh_token)


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    server_version = "WritingAgentOAuth/1.0"

    def do_GET(self) -> None:  # noqa: N802
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        self.server.auth_code = query.get("code", [None])[0]  # type: ignore[attr-defined]
        self.server.auth_error = query.get("error", [None])[0]  # type: ignore[attr-defined]

        message = "Google authorization received. You can close this window."
        if self.server.auth_error:  # type: ignore[attr-defined]
            message = f"Google authorization failed: {self.server.auth_error}"  # type: ignore[attr-defined]

        body = message.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def obtain_authorization_code(client: GoogleInstalledClient, *, timeout_seconds: int = 300) -> tuple[str, str]:
    server = ThreadingHTTPServer(("localhost", 0), OAuthCallbackHandler)
    server.auth_code = None  # type: ignore[attr-defined]
    server.auth_error = None  # type: ignore[attr-defined]

    redirect_uri = f"http://localhost:{server.server_port}/"
    auth_url = build_authorization_url(client, redirect_uri=redirect_uri)

    print("Open this URL and complete the Google sign-in if the browser does not open automatically:")
    print(auth_url)

    def serve_once() -> None:
        server.handle_request()

    thread = threading.Thread(target=serve_once, daemon=True)
    thread.start()
    try:
        with contextlib_suppress():
            webbrowser.open(auth_url, new=1)
        thread.join(timeout=timeout_seconds)
        if thread.is_alive():
            raise TimeoutError("Timed out waiting for Google OAuth callback.")
        if server.auth_error:  # type: ignore[attr-defined]
            raise RuntimeError(f"Google OAuth returned an error: {server.auth_error}")  # type: ignore[attr-defined]
        if not server.auth_code:  # type: ignore[attr-defined]
            raise RuntimeError("Google OAuth did not return an authorization code.")
        return redirect_uri, server.auth_code  # type: ignore[attr-defined]
    finally:
        server.server_close()


class contextlib_suppress:
    def __enter__(self) -> None:
        return None

    def __exit__(self, exc_type, exc, tb) -> bool:
        return True


def ensure_access_token(
    client: GoogleInstalledClient,
    *,
    token_path: Path,
    force_reauth: bool = False,
) -> str:
    saved = None if force_reauth else load_saved_token(token_path)
    if token_is_valid(saved):
        return saved["access_token"]

    if saved and saved.get("refresh_token") and not force_reauth:
        refreshed = refresh_access_token(client, refresh_token=saved["refresh_token"])
        save_token(token_path, refreshed)
        return refreshed["access_token"]

    redirect_uri, code = obtain_authorization_code(client)
    token_payload = exchange_code_for_token(client, code=code, redirect_uri=redirect_uri)
    save_token(token_path, token_payload)
    return token_payload["access_token"]


def google_json_get(url: str, *, access_token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return json.loads(response.read().decode(charset))


def google_json_get_with_retry(url: str, *, access_token: str, retries: int = 3) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            return google_json_get(url, access_token=access_token)
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
    raise RuntimeError("Unknown Google API fetch failure.")


def list_google_docs(
    *,
    access_token: str,
    folder_id: str | None = None,
    limit: int | None = 100,
) -> list[dict[str, Any]]:
    query = build_drive_query(folder_id=folder_id)
    results: list[dict[str, Any]] = []
    next_page_token: str | None = None

    while limit is None or len(results) < limit:
        page_size = 100 if limit is None else min(100, limit - len(results))
        params = {
            "q": query,
            "orderBy": "modifiedTime desc",
            "fields": "nextPageToken,files(id,name,modifiedTime,webViewLink)",
            "pageSize": str(page_size),
            "supportsAllDrives": "true",
            "includeItemsFromAllDrives": "true",
        }
        if next_page_token:
            params["pageToken"] = next_page_token
        url = f"https://www.googleapis.com/drive/v3/files?{urllib.parse.urlencode(params)}"
        payload = google_json_get_with_retry(url, access_token=access_token)
        results.extend(payload.get("files", []))
        next_page_token = payload.get("nextPageToken")
        if not next_page_token:
            break

    return results


def extract_paragraph_texts(document_payload: dict[str, Any]) -> list[str]:
    paragraphs: list[str] = []

    def visit_elements(elements: list[dict[str, Any]]) -> None:
        for element in elements:
            if "paragraph" in element:
                text_chunks: list[str] = []
                for item in element["paragraph"].get("elements", []):
                    text_run = item.get("textRun")
                    if text_run and text_run.get("content"):
                        text_chunks.append(text_run["content"])
                text = "".join(text_chunks).replace("\n", " ").strip()
                if text:
                    paragraphs.append(text)
            if "table" in element:
                for row in element["table"].get("tableRows", []):
                    for cell in row.get("tableCells", []):
                        visit_elements(cell.get("content", []))
            if "tableOfContents" in element:
                visit_elements(element["tableOfContents"].get("content", []))

    visit_elements(document_payload.get("body", {}).get("content", []))
    return paragraphs


def normalize_for_match(text: str) -> str:
    lowered = text.lower()
    lowered = lowered.replace(" ", "")
    lowered = lowered.replace("~", "")
    lowered = lowered.replace("～", "")
    return lowered


def find_intro_line(paragraphs: list[str]) -> str:
    for paragraph in paragraphs[:12]:
        normalized = normalize_for_match(paragraph)
        if "玫玫物語" in normalized:
            return paragraph
    return ""


def fetch_google_doc_record(metadata: dict[str, Any], *, access_token: str) -> GoogleDocRecord:
    document_id = metadata["id"]
    url = f"https://docs.googleapis.com/v1/documents/{urllib.parse.quote(document_id)}"
    document_payload = google_json_get_with_retry(url, access_token=access_token)
    paragraphs = extract_paragraph_texts(document_payload)
    full_text = " ".join(paragraphs)
    title = metadata.get("name", document_payload.get("title", document_id))
    intro_line = find_intro_line(paragraphs)
    return GoogleDocRecord(
        document_id=document_id,
        title=title,
        modified_time=metadata.get("modifiedTime", ""),
        web_view_link=metadata.get("webViewLink", ""),
        primary_category=classify_primary_category(title),
        formula=classify_formula(title),
        char_count=len(full_text),
        paragraph_count=len(paragraphs),
        intro_line=intro_line,
        has_maymei_intro=bool(intro_line),
        opening_promise=pick_opening_promise([title, *paragraphs]),
        voice_markers=detect_voice_markers([title, *paragraphs]),
    )


def fetch_google_doc_record_safe(metadata: dict[str, Any], *, access_token: str) -> GoogleDocRecord:
    try:
        return fetch_google_doc_record(metadata, access_token=access_token)
    except Exception as exc:
        title = metadata.get("name", metadata["id"])
        return GoogleDocRecord(
            document_id=metadata["id"],
            title=title,
            modified_time=metadata.get("modifiedTime", ""),
            web_view_link=metadata.get("webViewLink", ""),
            primary_category=classify_primary_category(title),
            formula=classify_formula(title),
            char_count=0,
            paragraph_count=0,
            intro_line="",
            has_maymei_intro=False,
            opening_promise="",
            voice_markers=[],
            fetch_error=str(exc),
        )


def render_markdown(records: list[GoogleDocRecord], *, folder_id: str | None) -> str:
    counts = Counter(record.primary_category for record in records)
    grouped: dict[str, list[GoogleDocRecord]] = defaultdict(list)
    for record in records:
        grouped[record.primary_category].append(record)

    lines = [
        "# Google Docs Corpus Index",
        "",
        "## Source",
        f"- Folder filter: `{folder_id or 'all accessible Google Docs'}`",
        f"- Total docs: `{len(records)}`",
        f"- Generated at: `{datetime.now(UTC).isoformat()}`",
        "",
        "## Category Counts",
    ]
    for category, count in sorted(counts.items()):
        lines.append(f"- `{category}`: {count}")

    lines.extend(["", "## Entries"])
    for category in sorted(grouped):
        lines.extend(["", f"### {category}"])
        for record in grouped[category]:
            marker_summary = " / ".join(record.voice_markers) if record.voice_markers else "無"
            lines.extend(
                [
                    "",
                    f"#### {record.title}",
                    f"- Google Doc ID: `{record.document_id}`",
                    f"- Formula: `{record.formula}`",
                    f"- Modified time: `{record.modified_time or 'unknown'}`",
                    f"- Approx chars: `{record.char_count}`",
                    f"- Paragraphs: `{record.paragraph_count}`",
                    f"- Has 玫玫物語 intro: `{record.has_maymei_intro}`",
                    f"- Intro line: {record.intro_line or '無'}",
                    f"- Voice markers: `{marker_summary}`",
                    f"- Opening promise: {record.opening_promise or '無'}",
                    f"- Fetch error: {record.fetch_error or '無'}",
                    f"- Link: {record.web_view_link or '無'}",
                ]
            )
    lines.append("")
    return "\n".join(lines)


def write_outputs(
    records: list[GoogleDocRecord],
    *,
    folder_id: str | None,
    markdown_output: Path,
    json_output: Path,
) -> None:
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.parent.mkdir(parents=True, exist_ok=True)

    markdown_output.write_text(
        render_markdown(records, folder_id=folder_id),
        encoding="utf-8",
    )
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "folder_id": folder_id,
        "total_docs": len(records),
        "records": [asdict(record) for record in records],
    }
    json_output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Authenticate to Google and build a classified index from Google Docs."
    )
    parser.add_argument("--client-secret", required=True, help="Path to the Google OAuth client secret JSON.")
    parser.add_argument("--token-path", default=str(repo_root / ".auth" / "google_docs_token.json"))
    parser.add_argument("--folder", help="Drive folder ID or folder URL to limit the scan.")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--force-reauth", action="store_true")
    parser.add_argument("--auth-only", action="store_true")
    parser.add_argument(
        "--markdown-output",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "google-docs-corpus.md"),
    )
    parser.add_argument(
        "--json-output",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "google-docs-corpus.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    client = load_client(Path(args.client_secret))
    token_path = Path(args.token_path)
    access_token = ensure_access_token(
        client,
        token_path=token_path,
        force_reauth=args.force_reauth,
    )

    if args.auth_only:
        print(f"Google OAuth succeeded. Token saved to {token_path}")
        return 0

    folder_id = extract_drive_id(args.folder)
    records = [
        fetch_google_doc_record_safe(item, access_token=access_token)
        for item in list_google_docs(access_token=access_token, folder_id=folder_id, limit=args.limit)
    ]
    write_outputs(
        records,
        folder_id=folder_id,
        markdown_output=Path(args.markdown_output),
        json_output=Path(args.json_output),
    )
    print(f"Indexed {len(records)} Google Docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
