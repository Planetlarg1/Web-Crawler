"""
Crawler Utilities for web scraping.
Target website: https://quotes.toscrape.com/

Functionality:
- URL normalisation. This is to prevent the crawler from visiting duplicate sites, 
  e.g. https://google.com and https://google.com/
- Ensures URL belongs to quotes.toscrape
"""

from urllib.parse import urldefrag, urlparse

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


def check_url_allowed(url: str, allowed_domain: str) -> bool:
    """
    Privacy is a very important consideration in web scraping, so the URL 
    must be checked to ensure that it belongs to the correct domain.
    Also checks that HTTP or HTTPS are used.

    Input: URL and the allowed domain

    Output: Boolean value for is allowed
    """
    parsed = urlparse(url)

    # Check http/https and domain
    return parsed.scheme in {"http", "https"} and parsed.netloc == allowed_domain