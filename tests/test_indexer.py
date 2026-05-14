from src.indexer import (
    tokenise,
    index_page,
    CrawledPage,
    build_index
)

################
# TOKENISATION #
################
def test_tokenisation_lowercase():
    tokens = tokenise("Hello WORLD")

    assert tokens == ["hello", "world"]

def test_tokenisation_punctuation():
    tokens = tokenise("Hello. World's-testing!")

    assert tokens == ["hello", "world", "s", "testing"]

def test_tokenisation_numbers():
    tokens = tokenise("Hello 4 World 8.8")

    assert tokens == ["hello", "4", "world", "8", "8"]

def test_tokenisation_empty():
    tokens = tokenise("")

    assert tokens == []


############
# INDEXING #
############
page = CrawledPage(
        url="https://quotes.toscrape.com/",
        title="Test Page",
        text="Hello. World's-testing! hello TeSTING hello"
    )

def test_page_indexing_frequency():
    page_index = index_page(page)

    assert page_index["hello"]["frequency"] == 3
    assert page_index["testing"]["frequency"] == 2
    assert page_index["world"]["frequency"] == 1

def test_page_indexing_positions():
    page_index = index_page(page)

    assert page_index["hello"]["positions"] == [0, 4, 6]
    assert page_index["testing"]["positions"] == [3, 5]
    assert page_index["world"]["positions"] == [1]

def test_page_indexing_empty():
    page_index = index_page(CrawledPage(
        url="https://quotes.toscrape.com/",
        title="Test Page",
        text=""
    ))

    assert page_index == {}

###########################
# INVERTED INDEX BUILDING #
###########################
pages = [
        CrawledPage(
            url="https://quotes.toscrape.com/",
            title="Page 1",
            text="Hello. World's-testing! hello TeSTING hello"
        ),
        CrawledPage(
            url="https://quotes.toscrape.com/page/2/",
            title="Page 2",
            text="Page 2: New. new PAGE- data/data daTA hello"
        ),
    ]

def test_build_index_documents():
    result = build_index(pages)

    assert result["documents"] == {
        "1": {
            "url": "https://quotes.toscrape.com/",
            "title": "Page 1",
            "token_count": 7
        },
        "2": {
            "url": "https://quotes.toscrape.com/page/2/",
            "title": "Page 2",
            "token_count": 9
        }
    }

def test_build_index_term_across_pages():
    result = build_index(pages)

    assert result["index"]["hello"] == {
        "1": {
            "frequency": 3,
            "positions": [0, 4, 6]
        },
        "2": {
            "frequency": 1,
            "positions": [8]
        }
    }

def test_build_index_term_in_single_page():
    result = build_index(pages)

    assert "1" in result["index"]["world"]
    assert "2" not in result["index"]["world"]
    assert "1" not in result["index"]["new"]
    assert "2" in result["index"]["new"]

def test_build_index_no_pages():
    result = build_index([])

    assert result == {
        "documents": {},
        "index": {}
    }

def test_build_index_empty_pages():
    pages = [
        CrawledPage(
            url="https://quotes.toscrape.com/",
            title="Page 1",
            text=""
        )
    ]

    result = build_index(pages)

    assert result == {
        "documents": {
            "1": {
                "url": "https://quotes.toscrape.com/",
                "title": "Page 1",
                "token_count": 0
            }
        },
        "index": {}
    }