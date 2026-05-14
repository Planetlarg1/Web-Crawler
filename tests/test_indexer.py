from src.indexer import (
    tokenise,
    index_page,
    CrawledPage
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
        text="Hello. World's-testing! hello TeSTING hello",
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
        text="",
    ))

    assert page_index == {}