"""
Crawler Utilities for web scraping.

Functionality:
- URL normalisation. This is to prevent the crawler from visiting duplicate sites, e.g. https://google.com and https://google.com/
"""

from urllib.parse import urldefrag, urlparse

def normalise_url(url: str) -> str:
    """
    Returns a normalised version of the inputted URL for deduplication. Removes '#section' and adds trailing '/'.
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