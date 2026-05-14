"""
Indexing Utilities for web scraping.
Target website: https://quotes.toscrape.com/

Functionality:
- Tokenise text into lowercase list of strings
"""

from __future__ import annotations
import re

def tokenise(text: str) -> list[str]:
    """
    Converts text into lowercase list of word tokens.

    Input: Text extracted from HTML page
    Output: List of word tokens

    E.g. "Hello World!" -> ["hello", "world"]
    """
    # Find all alphanumerics
    return re.findall(r"[a-zA-Z0-9]+", text.lower())