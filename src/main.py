"""
Command line interface to interact with web scraping and indexing tool.
Target website: https://quotes.toscrape.com/

Allowed Commands:
- Build
- Load
- Print [word]
- Find [query]
"""

from src.crawler import crawl_site
from src.indexer import build_index
from src.storage import load_index, save_index

INDEX_FILE_PATH = "data/index.json"

def build() -> dict:
    """
    Crawls website and builds the inverted index, storing it in index.json
    """
    # Crawl site
    print("Crawling https://quotes.toscrape.com/...")
    pages = crawl_site(max_pages=5)

    print(f"Crawled {len(pages)} page(s).")
    
    # Build index
    print("Building Index...")

    index_data = build_index(pages)
    save_index(index_data, INDEX_FILE_PATH)

    print(f"Index saved to {INDEX_FILE_PATH}.")


def load() -> dict | None:
    """
    Outputs the inverted index. If index doesn't exist, returns None.
    """
    try:
        index_data = load_index(INDEX_FILE_PATH)
    except FileNotFoundError:
        print("Index does not exist. Please build the index first.")
        return None
    
    print(f"Index loaded from {INDEX_FILE_PATH}")

    return index_data


def run_shell() -> None:
    """
    Run interactive shell for command running.
    """
    current_index: dict | None = None

    # Helpful disclaimers
    print("Running Web Scraper and Indexer...")
    print("Target Website: https://quotes.toscrape.com/")
    print("Available Commands:")
    print("- 'build': Instructs the search tool to crawl the website, build the index, and save the resulting index into the file system.")
    print("- 'load': Loads the index from the file system. Must first build the index.")
    print("- 'print': Prints the inverted index for a particular word. Must first build and load the index.")
    print("- 'find': Finds a given query phrase in the inverted index and returns a list of all pages that contain it. Must first build and load the index.")
    print("- 'exit': Stops and exits the program.")

    # Loop permanently and wait for commands
    while True:
        command = input("> ").strip().lower()
        
        if command == "exit":
            print("Program shutting down...")
            break

        if command == "build":
            current_index = build()
            continue

        if command == "load":
            index = load()
            continue

        if command.startswith("print"):
            continue

        if command.startswith("find"):
            continue

        else:
            print("Missing or unknown command.")


if __name__ == "__main__":
    run_shell()