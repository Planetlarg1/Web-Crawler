# COMP3011 Coursework 2
# Search Engine Tool

## Overview
The search engine tool is a command line tool for scraping a given example website, "https://quotes.toscrape.com/", building and managing an inverted index, and querying specific terms.

## Installation
From command line, run 
```bash
pip install -r requirements.txt
```
## Features
- Crawls the target website
- 6 second politeness window
- Uses BeautifulSoup for HTML parsing
- Uses Python Requests for composing HTML requests
- Builds a case-insensitive inverted index
- Stores word frequencies and positions
- Saves and loads the index file
- Has a command line interface for usage

## Usage
Run the file from the command line using
```bash
python -m src.main
```

Commands:

- **'build':** Instructs the search tool to crawl the website, build the index, and save the resulting index into the file system. For simplicity, it saving the entire index to a single file. 

- **'load':** This command loads the index from the file system. Obviously, this command will only work if the index has been created previously with the ’build’ command.

- **'print** *[input]***':** This command prints the inverted index for a particular word. The following example will print the inverted index for the word 'nonsense'.

```bash
    print nonsense
```

- **'find** *[input]***':** This command is used to find a given query phrase in the inverted index and returns a list of all pages that contain it. The first example will return a list of all pages containing the word 'indifference'. The second example will return all pages containing the words 'good' and 'friends'.

```bash
    find indifference
    find good friends
```

## Testing
**pytest** was used for unit and integration testing, with specific tests being found in */tests/* folder. Expected outcomes, edge cases, and error handling were all tested (e.g. malformed HTML or empty inputs). An average coverage of 95% was observed when running the following command:
```bash
    python -m pytest --cov=src --cov-report=term-missing
```
 To run the automated testing, run the following command from the command line:
```bash
    python -m pytest -v
```
Manual testing was also carried out to test the performance of the bash console which brings all the functionality together. Edge cases, such as empty inputs or invalid syntax, were rigorously tested alongisde expected inputs/outputs.

<u>Performance Testing</u>
Light performance testing was implemented in the file */tests/test_performance.py*. This tests the delay in building an index and querying a term against generated pages where tests were ran with 100, 500, and 2500 pages. The politeness window was ignored, as this gave clearer insight into the performance of the crawler itself, and as the pages were manually generated, the window is not enforced. 

A delay of less than 1 second per 1000 pages was observed in all cases across a number of tests. This can be considered to be negligent compared to the delay caused by the politeness window, which would observe a delay of 6 seconds per page, or 1 hour and 40 minutes per 1000 pages. This suggests that the crawling, indexing, and searching logic is all effectively implemented with minimal overhead.

## Design Rationale
The index uses a nested dictionary of the structure *term -> document_id -> {frequency, position}*. This gives support for fast term lookup and commands for 'print' and 'find'. Document metadata, such as title and url, is stored in a seperate mapping so that they aren not duplicated in every posting.
- Frequencies support simple relevance rankings.
- Positions support possible phrase/proximity extension.
- Utilising document IDs avoid repeated URLs throughout postings.
- JSON stores the full index in a single file for simplicity.
- Precomputed scores are not calculated beforehand to allow for flexibility.

<u>Complexity</u>
- Single-word lookup: *O(1)*
- Display *n* postings: *O(n)*
- Multi-word querying, where $x_i$ represents the number of documents containing the $i$'th term in the query: *O($x_1 + x_2 + ... + x_i$)*

## GenAI Usage
Generative AI was used as a tool for development. Examples of prompts, as well as the benefits and limitations of its usage can be found in */docs/AI_usage.md*