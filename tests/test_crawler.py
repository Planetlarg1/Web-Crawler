from src.crawler import normalise_url, check_url_allowed

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
    result = check_url_allowed(
        "https://quotes.toscrape.com/page/2/",
        "quotes.toscrape.com"
    )
    assert result is True

def test_url_allowed_wrong_domain():
    result = check_url_allowed(
        "http://facebook.com/page/2/",
        "quotes.toscrape.com"
    )
    assert result is False

def test_url_allowed_wrong_scheme():
    result = check_url_allowed(
        "mailto://quotes.toscrape.com/page/2/",
        "quotes.toscrape.com"
    )
    assert result is False