"""
Indexing Utilities for web scraping.
Target website: https://quotes.toscrape.com/

Functionality:
- Tokenise text into lowercase list of strings
- Record word frequency and positions in a single page
- Creates full inverted index for multiple documents
"""

from __future__ import annotations
import re

from src.crawler import CrawledPage


def tokenise(text: str) -> list[str]:
    """
    Converts text into lowercase list of word tokens.

    Input: Text extracted from HTML page
    Output: List of word tokens

    E.g. "Hello World!" -> ["hello", "world"]
    """
    # Find all alphanumerics
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def index_page(page: CrawledPage) -> dict[str, dict[str, list[int] | int]]:
    """
    Return the frequency and locations (0 based) of words in a given crawled page.

    Input: CrawledPage object
    Output: Dict mapping of each token to frequency and position(s)
    """
    # Tokenise page contents
    tokens = tokenise(page.text)
    page_index: dict[str, dict[str, list[int] | int]] = {}

    # Iterate through tokens and assign value
    for position, token in enumerate(tokens):
        # Add token to index
        if token not in page_index:
            page_index[token] = {
                "frequency": 0,
                "positions": []
            }

        # Increment values
        page_index[token]["frequency"] += 1
        page_index[token]["positions"].append(position)

    return page_index


def build_index(pages: list[CrawledPage]) -> dict:
    """
    Builds a full inverted index for a list of crawled pages.

    Input: List of CrawledPage objects
    Output: Dict mapping of pages and tokens
    """
    # Initialise documents and index using existing schemas
    documents: dict[str, dict[str, str | int]] = {}
    inverted_index: dict[str, dict[str, dict[str, list[int] | int]]]= {}

    # Create mappings for each page
    for doc_id, page in enumerate(pages, start=1):
        doc_id = str(doc_id)
        tokens = tokenise(page.text)

        # Create document mapping
        documents[doc_id] = {
            "url": page.url,
            "title": page.title,
            "token_count": len(tokens)
        }

        page_index = index_page(page)

        # Add words and counts to inverted index per page
        for word, count in page_index.items():
            if word not in inverted_index:
                # Add to index
                inverted_index[word] = {}

            # Set frequency for token in page
            inverted_index[word][doc_id] = count

    return {
        "documents": documents,
        "index": inverted_index
    }