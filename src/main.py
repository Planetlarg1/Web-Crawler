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
from src.search import get_index_for_word, find_query

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


def print_index(index_data: dict | None, command: str) -> dict | None:
    """
    Prints the index posting for a given word.
    """
    # Check index exists
    if index_data is None:
        print("No index loaded. Please run 'build' and 'load' first.")
        return
    
    # Check valid syntax
    parts = command.split()
    if len(parts) == 1:
        print("Please provide a term to index.")
        return
    elif len(parts) > 2:
        print("Print can only be used to index a single term.")
        return
    
    word = parts[1].strip()
    postings = get_index_for_word(index_data, word)

    if not postings:
        print(f"No postings found for '{word}'.")
        return
    
    # Print structured postings
    docs = index_data.get("documents", {})
    print(f"Postings for '{word}':")
    print(" " + "-" * 100)
    for doc_id, info in postings.items():
        doc = docs.get(doc_id, {})
        url = doc.get("url", "[Unknown URL]")

        print(f"| Document {doc_id}: {url}")
        print(f"| Frequency: {info['frequency']}")
        print(f"| Location(s): {', '.join(map(str, info['positions']))}")
        print(" " + "-" * 100)


def run_shell() -> None:
    """
    Run interactive shell for command running.
    """
    index: dict | None = None

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
            build()
            continue

        if command == "load":
            index = load()
            continue

        if command.startswith("print"):
            print_index(index, command)
            continue

        if command.startswith("find"):
            continue

        else:
            print("Missing or unknown command.")


if __name__ == "__main__":
    run_shell()