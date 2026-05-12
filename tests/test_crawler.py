from src.crawler import normalise_url, check_url_allowed, extract_links

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
SAMPLE_HTML = """
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
    links = extract_links(SAMPLE_HTML, "https://quotes.toscrape.com/")

    assert "https://quotes.toscrape.com/page/2/" in links

def test_extract_links_absolute_links():
    links = extract_links(SAMPLE_HTML, "https://quotes.toscrape.com/")

    assert "https://quotes.toscrape.com/page/3/" in links

def test_extract_links_absolute_links_from_parent():
    links = extract_links(SAMPLE_HTML, "https://quotes.toscrape.com/page/3/info/")

    assert "https://quotes.toscrape.com/page/3/" in links

def test_extract_links_normalisation_and_deduplication():
    links = extract_links(SAMPLE_HTML, "https://quotes.toscrape.com/")

    assert "https://quotes.toscrape.com/page/2/#quotes" not in links
    assert "https://quotes.toscrape.com/page/2/#quotes/" not in links
    assert links.count("https://quotes.toscrape.com/page/2/") == 1

def test_extract_links_ignore_invalid_links():
    links = extract_links(SAMPLE_HTML, "https://quotes.toscrape.com/")

    assert "https://external.example.com/" not in links
    assert "mailto://quotes.toscrape.com" not in links