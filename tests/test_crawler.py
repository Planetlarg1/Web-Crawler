import requests
from src.crawler import (
    normalise_url,
    check_url_allowed,
    extract_links,
    extract_visible_text,
    CrawledPage,
    fetch_page)

# URL NORMALISATION
def test_normalise_url_removes_fragment():
    result = normalise_url("https://quotes.toscrape.com/page/2/#section")
    assert result == "https://quotes.toscrape.com/page/2/"

def test_normalise_url_trailing_slash_page():
    result = normalise_url("https://quotes.toscrape.com/page/2")
    assert result == "https://quotes.toscrape.com/page/2/"

def test_normalise_url_trailing_slash_file():
    result = normalise_url("https://quotes.toscrape.com/page/style.css")
    assert result == "https://quotes.toscrape.com/page/style.css"

def test_normalise_url_keeps_trailing_slash():
    result = normalise_url("https://quotes.toscrape.com/page/2/")
    assert result == "https://quotes.toscrape.com/page/2/"


# DOMAIN CHECKING
def test_url_allowed_positive():
    result = check_url_allowed("https://quotes.toscrape.com/page/2/")
    assert result is True

def test_url_allowed_wrong_domain():
    result = check_url_allowed("http://facebook.com/page/2/")
    assert result is False

def test_url_allowed_wrong_scheme():
    result = check_url_allowed("mailto://quotes.toscrape.com/page/2/")
    assert result is False


# LINK EXTRACTION
SAMPLE_HTML_LINKS = """
<html>
    <body>
        <a href="/page/2/">Page 2 Relative</a>
        <a href="https://quotes.toscrape.com/page/3/">Page 3 Absolute</a>
        <a href="https://quotes.toscrape.com/page/2/#quotes">Duplicate page with fragment</a>
        <a href="https://external.example.com/">External link</a>
        <a href="mailto://quotes.toscrape.com">Incorrect schema</a>
        <a>No href</a>
    </body>
</html>
"""

def test_extract_links_resolve_relative_links_child():
    links = extract_links(SAMPLE_HTML_LINKS, "https://quotes.toscrape.com/")

    assert "https://quotes.toscrape.com/page/2/" in links

def test_extract_links_absolute_links():
    links = extract_links(SAMPLE_HTML_LINKS, "https://quotes.toscrape.com/")

    assert "https://quotes.toscrape.com/page/3/" in links

def test_extract_links_absolute_links_from_parent():
    links = extract_links(SAMPLE_HTML_LINKS, "https://quotes.toscrape.com/page/3/info/")

    assert "https://quotes.toscrape.com/page/3/" in links

def test_extract_links_normalisation_and_deduplication():
    links = extract_links(SAMPLE_HTML_LINKS, "https://quotes.toscrape.com/")

    assert "https://quotes.toscrape.com/page/2/#quotes" not in links
    assert "https://quotes.toscrape.com/page/2/#quotes/" not in links
    assert links.count("https://quotes.toscrape.com/page/2/") == 1

def test_extract_links_ignore_invalid_links():
    links = extract_links(SAMPLE_HTML_LINKS, "https://quotes.toscrape.com/")

    assert "https://external.example.com/" not in links
    assert "mailto://quotes.toscrape.com" not in links


# VISIBLE TEXT EXTRACTION
SAMPLE_HTML_TEXT = """
<html>
    <head>
        <title>Quotes to Scrape</title>
        <style>
            body { color: red; }
        </style>
    </head>
    <body>
        <h1>Quotes to Scrape</h1>
        <div class="quote">
            <span class="text">The world as we have created it is a process of our thinking.</span>
            <small class="author">Albert Einstein</small>
        </div>
        <script>
            console.log("this should not be indexed");
        </script>
        <noscript>
            JavaScript disabled message
        </noscript>
    </body>
</html>
"""

SAMPLE_HTML_TEXT_NO_TITLE = """
<html>
    <head>
        <style>
            body { color: red; }
        </style>
    </head>
    <body>
        <h1>Quotes to Scrape</h1>
        <div class="quote">
            <span class="text">The world as we have created it is a process of our thinking.</span>
            <small class="author">Albert Einstein</small>
        </div>
        <script>
            console.log("this should not be indexed");
        </script>
        <noscript>
            JavaScript disabled message
        </noscript>
    </body>
</html>
"""

SAMPLE_HTML_TEXT_NO_BODY = """
<html>
    <head>
        <title>Quotes to Scrape</title>
        <style>
            body { color: red; }
        </style>
    </head>
</html>
"""

def test_extract_visible_text_check_title():
    title, text = extract_visible_text(SAMPLE_HTML_TEXT)

    assert title == "Quotes to Scrape"

def test_extract_visible_text_check_contents():
    title, text = extract_visible_text(SAMPLE_HTML_TEXT)

    assert "The world as we have created it is a process of our thinking." in text
    assert "Albert Einstein" in text

def test_extract_visible_text_removes_invisible_data():
    title, text = extract_visible_text(SAMPLE_HTML_TEXT)

    assert "color: red" not in text
    assert "console.log" not in text
    assert "JavaScript disabled message" not in text

def test_extract_visible_text_no_title():
    title, text = extract_visible_text(SAMPLE_HTML_TEXT_NO_TITLE)

    assert title == ""
    assert "Albert Einstein" in text

def test_extract_visible_text_no_body():
    title, text = extract_visible_text(SAMPLE_HTML_TEXT_NO_BODY)

    assert title == "Quotes to Scrape"
    assert text == ""


# PAGE FETCHING
class FakeResponse:
    def __init__(
        self,
        text: str = "",
        content_type: str = "text/html",
        should_raise: bool = False
    ):
        self.text = text
        self.headers = {"Content-Type": content_type}
        self.should_raise = should_raise


    def raise_for_status(self):
        if self.should_raise:
            raise requests.RequestException("HTTP error")
        

def test_fetch_page_returns_html(monkeypatch):
    def fake_get(url, timeout, headers):
        return FakeResponse(
            text="<html><body>Quotes</body></html>",
            content_type="text/html"
        )
    
    monkeypatch.setattr("src.crawler.requests.get", fake_get)

    result = fetch_page("https://quotes.toscrape.com/")

    assert result == "<html><body>Quotes</body></html>"

def test_fetch_page_not_html(monkeypatch):
    def fake_get(url, timeout, headers):
        return FakeResponse(
            text="body { color: red; }",
            content_type="text/css"
        )
    
    monkeypatch.setattr("src.crawler.requests.get", fake_get)

    result = fetch_page("https://quotes.toscrape.com/static/styles.css")

    assert result is None

def test_fetch_page_failed_request(monkeypatch):
    def fake_get(url, timeout, headers):
        raise requests.RequestException("Network failure")
    
    monkeypatch.setattr("src.crawler.requests.get", fake_get)

    result = fetch_page("https://quotes.toscrape.com/")

    assert result is None

def test_fetch_page_attrs_sent(monkeypatch):
    captured_args = {}

    def fake_get(url, timeout, headers):
        captured_args["url"] = url
        captured_args["timeout"] = timeout
        captured_args["headers"] = headers

        return FakeResponse(
            text="<html></html>",
            content_type="text/html"
        )
    
    monkeypatch.setattr("src.crawler.requests.get", fake_get)

    result = fetch_page("https://quotes.toscrape.com/")

    assert captured_args["url"] == "https://quotes.toscrape.com/"
    assert captured_args["timeout"] == 10
    assert "User-Agent" in captured_args["headers"]
    assert captured_args["headers"]["User-Agent"] == "COMP3011-Coursework-2-Crawler/1.0"

def test_fetch_page_http_error(monkeypatch):
    def fake_get(url, timeout, headers):
        return FakeResponse(
            text="<html></html>",
            content_type="text/html",
            should_raise=True
        )
    
    monkeypatch.setattr("src.crawler.requests.get", fake_get)

    result = fetch_page("https://quotes.toscrape.com/missing-page/")

    assert result is None