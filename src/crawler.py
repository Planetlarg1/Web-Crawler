"""
Crawler Utilities for web scraping.
Target website: https://quotes.toscrape.com/

Functionality:
- URL normalisation. This is to prevent the crawler from visiting duplicate sites, 
  e.g. https://google.com and https://google.com/
- Ensures URL belongs to quotes.toscrape
"""

from urllib.parse import urldefrag, urlparse, urljoin
from bs4 import BeautifulSoup
from dataclasses import dataclass
import requests

ALLOWED_DOMAIN = "quotes.toscrape.com"
REQUEST_TIMEOUT = 10
USER_AGENT = "COMP3011-Coursework-2-Crawler/1.0"

@dataclass
class CrawledPage:
    """
    Represents a single successfully crawled web page to be passed to the indexer.

    Attributes:
        url: The normalised url of the webpage
        title: The extracted plaintext title of the webpage
        text: The extracted plaintext contents of the webpage
    """
    url: str
    title: str
    text: str

def normalise_url(url: str) -> str:
    """
    Returns a normalised version of the inputted URL for deduplication.
    Removes '#section' and adds trailing '/'.

    Input: URL without normalised format.

    Output: URL with normalised format.
    """
    # Parse and defragment URL
    url_without_fragments, fragment = urldefrag(url)
    parsed = urlparse(url_without_fragments)
    
    # Ignore query string
    normalised_url = parsed.geturl()

    # Check for trailing "/" and add if needed
    path_end = parsed.path.split("/")[-1]

    # Do not add trailing "/" to file URLs (e.g. style.css contains a '.')
    if not normalised_url.endswith("/") and "." not in path_end:
        normalised_url += "/"

    return normalised_url


def check_url_allowed(url: str) -> bool:
    """
    Privacy is a very important consideration in web scraping, so the URL 
    must be checked to ensure that it belongs to the correct domain.
    Also checks that HTTP or HTTPS are used.

    Input: URL to check

    Output: Boolean value for is allowed
    """
    parsed = urlparse(url)

    # Check http/https and domain
    return parsed.scheme in {"http", "https"} and parsed.netloc == ALLOWED_DOMAIN


def extract_links(html: str, base_url: str) -> list[str]:
    """
    Given raw HTML, embedded links must be located, normalised and checked.
    External links and duplicate links are ignored.

    Input: raw HTML and the base URL

    Output: A list of strings representing the processed URLs.
    """
    # Use BeautifulSoup for html parsing
    soup = BeautifulSoup(html, "html.parser")

    links: set[str] = set()

    # Locate and process links
    for anchor in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, anchor["href"])
        normalised_url = normalise_url(absolute_url)

        if check_url_allowed(normalised_url):
            links.add(normalised_url)

    return sorted(links)


def extract_visible_text(html: str) -> tuple[str, str]:
    """
    Given raw HTML, the page title and visible text should be extracted for analysis.
    Script, style, and noscript elements are removed because they aren't useful for search.

    Input: Raw HTML

    Output: Tuple of page title and visible text
    """
    # Use BeautifulSoup for html parsing
    soup = BeautifulSoup(html, "html.parser")

    # Extract title
    title = soup.title.get_text(" ", strip=True) if soup.title else ""

    # Remove invisible componenents
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    if soup.head:
        soup.head.decompose()

    # Extract relevant data if existing
    text = soup.get_text(" ", strip=True) if soup.text else ""

    return title, text


def fetch_page(url: str) -> str | None:
    """
    Fetches a single HTML page.

    Input: URL for the desired web page.

    Output: 
        Response text and webpage HTML on success. 
        None on failure or if contents is not HTML.
    """
    # Attempt to fetch web page
    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": USER_AGENT}
        )
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    # Get content type
    content_type = response.headers.get("Content-Type", "")

    # Check for HTML
    if "text/html" not in content_type:
        return None
    
    return response.text