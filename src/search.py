"""
Search Utilities for web scraping.
Target website: https://quotes.toscrape.com/

Functionality:
- Retrieve inverted index for a particular word for 'find' command
"""

from __future__ import annotations

from src.indexer import tokenise


def get_index_for_word(index_data: dict, word: str) -> dict:
    """
    Returns the inverted index entry for a given word.

    Input:
        index_data: Full index structure to search
        word: Inputted word used to search index
    
    Output:
        Dictionary mapping of all documents for the given word
    """
    # Only accept 1 token
    tokens = tokenise(word)

    if len(tokens) != 1:
        return {}
    
    term = tokens[0]

    # 
    return index_data.get("index", {}).get(term, {})