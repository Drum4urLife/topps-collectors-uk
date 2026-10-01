"""Read upcoming releases from the Topps UK release calendar."""

from html.parser import HTMLParser
from urllib.request import Request, urlopen


RELEASE_CALENDAR_URL = "https://uk.topps.com/release-calendar"


class PageTextParser(HTMLParser):
    """Extract visible-ish text from an HTML page."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self._ignored_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data):
        if not self._ignored_depth:
            text = " ".join(data.split())
            if text:
                self.text_parts.append(text)


def fetch_release_calendar() -> str:
    """Download the Topps UK release calendar."""

    request = Request(
        RELEASE_CALENDAR_URL,
        headers={
            "User-Agent": (
                "ToppsCollectorsUK/1.0 "
                "(release calendar monitor; https://github.com/Drum4urLife/topps-collectors-uk)"
            )
        },
    )

    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def extract_page_text(html: str) -> list[str]:
    """Return the page's text as cleaned individual strings."""

    parser = PageTextParser()
    parser.feed(html)
    return parser.text_parts


def main() -> None:
    html = fetch_release_calendar()
    text_parts = extract_page_text(html)

    print(f"Downloaded {len(html):,} characters from Topps UK.")
    print(f"Extracted {len(text_parts):,} text fragments.")
    print()
    print("First 100 text fragments:")
    print("-" * 60)

    for text in text_parts[:100]:
        print(text)


if __name__ == "__main__":
    main()
