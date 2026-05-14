"""
Storage Utilities for web scraping.
Target website: https://quotes.toscrape.com/

Functionality:
- Saves the generated index to a seperate file upon build request
- Loads the index from the seperate file upon load request
"""

from __future__ import annotations
import json
from pathlib import Path


def save_index(index_data: dict, file_path: str) -> None:
    """
    Saves index to a local json file.

    Input:
        index_data: Full inverted index to save
        file_path: Path to local json file
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(index_data, file, indent=2)


def load_index(file_path: str) -> None:
    """
    Loads index from local json file.

    Input: File path to index
    Output: Full inverted index
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
