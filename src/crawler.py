"""
Crawler Utilities for web scraping.
Target website: https://quotes.toscrape.com/

Functionality:
- URL normalisation. This is to prevent the crawler from visiting duplicate sites, 
  e.g. https://google.com and https://google.com/
- Ensures URL belongs to quotes.toscrape
- Extract only the internal links from the page
- Extract text and title from HTML
- Fetch page HTML given a URL following the politeness window
- Processing a page given HTML into actionable parts
- Combine functionality into a crawling loop
"""

from urllib.parse import urldefrag, urlparse, urljoin
from bs4 import BeautifulSoup
from dataclasses import dataclass
import requests
import time
from collections import deque

ALLOWED_DOMAIN = "quotes.toscrape.com"
REQUEST_TIMEOUT = 10
USER_AGENT = "COMP3011-Coursework-2-Crawler/1.0"
POLITENESS_DELAY = 6.0


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

    # Locate and process links if allowed
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


def wait_for_politeness(last_request_time: float | None) -> None:
    """
    Enforces politeness window of 6 seconds be respected.

    Input: last_request_time is float timestamp of previous request, or None there has been no request
    """
    # Check if there was a previous request
    if last_request_time is None:
        return
    
    # Delay by remaining window, accounting for computational delays
    elapsed = time.time() - last_request_time
    remaining_delay = POLITENESS_DELAY - elapsed

    if remaining_delay > 0:
        time.sleep(remaining_delay)


def politely_fetch_page(
        url: str,
        last_request_time: float | None,
) -> tuple[str | None, float]:
    """
    Combines utility of fetch_page and wait_for_politeness.

    Input:
        url: The URL to fetch
        last_request_time: Float timestamp of previous request

    Output:
        Tuple containing HTML and updated timestamp
    """
    # Politeness window
    wait_for_politeness(last_request_time)

    # Fetch page
    html = fetch_page(url)
    new_request_time = time.time()

    return html, new_request_time


def process_page(url: str, html: str) -> tuple[CrawledPage, list[str]]:
    """
    Processes a fetched HTML page into actionable parts.

    Input:
        url: The URL that was fetched
        html: The contents of the fetched page

    Output:
        CrawledPage object containing url, title, and text
        List of discovered links
    """
    # Extract relevant data with helper functions
    normalised_url = normalise_url(url)
    title, text = extract_visible_text(html)
    links = extract_links(html, normalised_url)

    page = CrawledPage(
        url=normalised_url,
        title=title,
        text=text
    )

    return page, links


def crawl_site(
        seed_url: str = "https://quotes.toscrape.com/",
        max_pages: int | None = None
) -> list[CrawledPage]:
    """
    Crawl loop on target website.

    Uses frontier queue and visited set for deduplication.
    Only allowed URLs are fetched.
    Politeness window is followed.

    Input:
        seed_url: The starting URL for the crawl, set to given example URL
        max_pages: Optional page limit for tests and demos

    Output:
        A list of CrawledPage objects
    """
    # Initialise frontier queue
    frontier = deque([normalise_url(seed_url)])
    visited: set[str] = set()
    crawled_pages: list[CrawledPage] = []
    last_request_time: float | None = None

    # Loop through URLs and add pages to crawled list
    while frontier:
        # Check if max_pages hit
        if max_pages is not None and len(crawled_pages) >= max_pages:
            break

        # Pop URL
        current_url = normalise_url(frontier.popleft())

        # Check if current page has been visited
        if current_url in visited:
            continue

        # Check if current page is permitted
        if not check_url_allowed(current_url):
            continue

        # Mark page as visited
        visited.add(current_url)

        # Fetch HTML and update request time
        html, last_request_time = politely_fetch_page(current_url, last_request_time)

        # Check HTML exists
        if html is None:
            continue

        # Processes returned HTML
        page, discovered_links = process_page(current_url, html)
        crawled_pages.append(page)

        # Iterate through discovered links and add to queue if new
        for link in discovered_links:
            if link not in visited and link not in frontier:
                frontier.append(link)

    return crawled_pages