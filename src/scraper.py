from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

from src.config import RAW_DATA_DIR, settings


class _TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._inside_title = False
        self.title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self._inside_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._inside_title = False

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self.title_parts.append(data)


class ExampleScraper:
    def __init__(self, url: str = "https://example.com") -> None:
        self.url = url

    def fetch(self) -> str:
        request = Request(
            self.url,
            headers={"User-Agent": settings.user_agent},
        )
        with urlopen(request, timeout=settings.request_timeout) as response:
            return response.read().decode("utf-8", errors="replace")

    def parse_title(self, html: str) -> str:
        parser = _TitleParser()
        parser.feed(html)
        title = "".join(parser.title_parts).strip()
        return title or "No title found"

    def save_raw_html(self, html: str, filename: str = "example.html") -> Path:
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        destination = RAW_DATA_DIR / filename
        destination.write_text(html, encoding="utf-8")
        return destination
