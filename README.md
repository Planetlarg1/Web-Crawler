# COMP3011 Coursework 2
# Search Engine Tool

## Overview
The search engine tool is a command line tool for crawling the target website, "https://quotes.toscrape.com/", building and managing an inverted index, and querying specific terms.

## Installation
From command line, run 
```bash
pip install -r requirements.txt
```
## Features
- Crawls the target website
- 6 second politeness window
- Uses BeautifulSoup for HTML parsing
- Uses Python Requests for composing HTTP requests
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

- **'build':** Instructs the search tool to crawl the website, build the index, and save the resulting index into the file system. For simplicity, it saves the entire index to a single file. An optional page limit can be passed to speed up crawling for demonstration.

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
Manual testing was also carried out to test the performance of the bash console which brings all the functionality together. Edge cases, such as empty inputs or invalid syntax, were rigorously tested alongside expected inputs/outputs.

<u>Performance Testing</u>
Light performance testing was implemented in the file */tests/test_performance.py*. This tests the delay in building an index and querying a term against generated pages where tests were ran with 100, 500, and 2500 pages. The politeness window was ignored for the sake of these tests, as this gave clearer insight into the performance of the crawler itself, and as the pages were manually generated, the window is not relevant. 

A delay of less than 1 second per 1000 pages was observed in all cases across a number of tests. This can be considered to be negligible compared to the delay caused by the politeness window, which would observe a delay of 6 seconds per page, or 1 hour and 40 minutes per 1000 pages. This suggests that the indexing, and query-processing logic are effectively implemented with minimal overhead.

## Design Rationale
The index uses a nested dictionary of the structure *term -> document_id -> {frequency, position}*. This gives support for fast term lookup and commands for 'print' and 'find'. Document metadata, such as title and url, is stored in a separate mapping so that they are not duplicated in every posting.
- Frequencies support simple relevance rankings.
- Positions support possible phrase/proximity extension.
- Using document IDs avoid repeated URLs throughout postings.
- JSON stores the full index in a single file for simplicity.
- Precomputed scores are not calculated beforehand to allow for flexibility.

<u>Complexity</u>
- Single-word lookup: *O(1)*
- Display *n* postings: *O(n)*
- Multi-word querying, where $x_i$ represents the number of documents containing the $i$'th term in the query for $k$ total terms in the query: *O($x_1 + x_2 + ... + x_k$)*
- Scoring and sorting results: *O($rk + r log(r)$)* where $r$ is the number of matching documents.

## Architecture Overview
The implementation is split up into several modular components:
- *crawler.py:* Handles URL normalisation, polite HTML fetching, link checking and extraction, body and title extraction, and crawling frontier implementation.
- *indexer.py:* Handles text tokenisation, word frequency and positioning analysis, and inverted index generation.
- *search.py:* Retrieves relevant index entries and documents for 'find' and 'print' commands.
- *storage.py:* Saves the generated index to a seperate file upon build request, and loads said index upon load request.
- *main.py:* Combines utility from other files and runs an interactive shell for the user.
- */tests/:* Multiple testing suites used to test functionality of each system component.

## GenAI Usage
Generative AI was used as a tool for development. Examples of prompts, as well as the benefits and limitations of its usage can be found in */docs/AI_usage.md*