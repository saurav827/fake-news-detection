"""Safe URL article extraction helpers.

The extractor is intentionally separate from the deployed prediction pipeline.
It returns plain text that can be pasted into the existing Streamlit text box.
"""

from html.parser import HTMLParser
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DEFAULT_TIMEOUT_SECONDS = 8
DEFAULT_MAX_CHARS = 12000
USER_AGENT = "Mozilla/5.0 (compatible; AcademicFakeNewsDetector/1.0)"


class _ParagraphHTMLParser(HTMLParser):
    """Small fallback parser used when BeautifulSoup is unavailable."""

    def __init__(self):
        super().__init__()
        self._capture = False
        self._parts = []
        self._title_parts = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in {"p", "article", "main"}:
            self._capture = True
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag in {"p", "article", "main"}:
            self._capture = False
            self._parts.append(" ")
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._capture:
            self._parts.append(data)
        if self._in_title:
            self._title_parts.append(data)

    @property
    def text(self):
        return " ".join(self._parts)

    @property
    def title(self):
        return " ".join(self._title_parts)


def _clean_article_text(text):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def _safe_result(ok, url, text="", title="", source="", error=""):
    text = _clean_article_text(text)
    return {
        "ok": ok,
        "url": url,
        "title": _clean_article_text(title),
        "text": text,
        "char_count": len(text),
        "word_count": len(text.split()),
        "source": source,
        "error": error,
    }


def is_valid_article_url(url):
    """Return True only for http/https URLs with a network location."""
    try:
        parsed = urlparse((url or "").strip())
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


def _extract_with_newspaper(url, timeout):
    try:
        from newspaper import Article
    except Exception:
        return None

    try:
        article = Article(url)
        article.download(input_html=None, title=None, recursion_counter=0)
        article.parse()
        return _safe_result(
            True,
            url,
            text=article.text,
            title=article.title,
            source="newspaper3k",
        )
    except Exception:
        return None


def _fetch_html(url, timeout):
    try:
        import requests

        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
        )
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "html" not in content_type.lower():
            return "", f"URL did not return an HTML article page ({content_type})."
        return response.text, ""
    except ImportError:
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=timeout) as response:
                content_type = response.headers.get("content-type", "")
                if "html" not in content_type.lower():
                    return "", f"URL did not return an HTML article page ({content_type})."
                return response.read().decode("utf-8", errors="ignore"), ""
        except Exception as exc:
            return "", f"Article download failed: {exc}"
    except Exception as exc:
        return "", f"Article download failed: {exc}"


def _extract_with_beautifulsoup(url, timeout):
    html, error = _fetch_html(url, timeout)
    if error:
        return _safe_result(False, url, error=error)

    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()

        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        containers = soup.select("article, main")
        paragraphs = []
        for container in containers or [soup]:
            paragraphs.extend(
                paragraph.get_text(" ", strip=True)
                for paragraph in container.find_all("p")
            )

        text = _clean_article_text(" ".join(part for part in paragraphs if part))
        return _safe_result(True, url, text=text, title=title, source="BeautifulSoup")
    except Exception:
        parser = _ParagraphHTMLParser()
        try:
            parser.feed(html)
            return _safe_result(
                True,
                url,
                text=parser.text,
                title=parser.title,
                source="html.parser fallback",
            )
        except Exception as exc:
            return _safe_result(False, url, error=f"HTML parsing failed: {exc}")


def extract_article_text(url, timeout=DEFAULT_TIMEOUT_SECONDS, max_chars=DEFAULT_MAX_CHARS):
    """Extract article text from a URL without changing the prediction pipeline."""
    clean_url = (url or "").strip()
    if not is_valid_article_url(clean_url):
        return _safe_result(False, clean_url, error="Enter a valid http or https URL.")

    try:
        result = _extract_with_newspaper(clean_url, timeout)
        if not result or not result.get("text"):
            result = _extract_with_beautifulsoup(clean_url, timeout)

        if not result.get("ok"):
            return result

        text = result.get("text", "")[:max_chars]
        if len(text.split()) < 20:
            return _safe_result(
                False,
                clean_url,
                title=result.get("title", ""),
                source=result.get("source", ""),
                error="Could not extract enough article text from this URL.",
            )

        result["text"] = text
        result["char_count"] = len(text)
        result["word_count"] = len(text.split())
        result["truncated"] = len(result.get("text", "")) >= max_chars
        return result
    except Exception as exc:
        return _safe_result(False, clean_url, error=f"Safe URL extraction failed: {exc}")
