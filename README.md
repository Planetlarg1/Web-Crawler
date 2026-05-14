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
**pytest** was used for testing, with details being found in */tests/*.

## GenAI Usage
Generative AI was used as a tool for development. Examples of prompts, as well as the benefits and limitations of its usage can be found in */docs/AI_usage.md*