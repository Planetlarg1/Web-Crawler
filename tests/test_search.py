from src.search import get_index_for_word

SAMPLE_INDEX_DATA = {
    "documents": {
        "1": {
            "url": "https://quotes.toscrape.com/",
            "title": "Home",
            "token_count": 5,
        },
        "2": {
            "url": "https://quotes.toscrape.com/page/2/",
            "title": "Page 2",
            "token_count": 4,
        },
    },
    "index": {
        "good": {
            "1": {
                "frequency": 2,
                "positions": [0, 3],
            },
            "2": {
                "frequency": 1,
                "positions": [2],
            },
        },
        "friends": {
            "1": {
                "frequency": 1,
                "positions": [1],
            },
        },
    },
}

# FIND INDEX FOR SINGLE TERM
def test_find_existing_term():
    postings = get_index_for_word(SAMPLE_INDEX_DATA, "good")

    assert postings == {
        "1": {
            "frequency": 2,
            "positions": [0, 3]
        },
        "2": {
            "frequency": 1,
            "positions": [2],
        }
    }

def test_find_term_case_punctuation_insensitive():
    postings = get_index_for_word(SAMPLE_INDEX_DATA, " GooD.!")

    assert postings == {
        "1": {
            "frequency": 2,
            "positions": [0, 3]
        },
        "2": {
            "frequency": 1,
            "positions": [2],
        }
    }

def test_find_empty_term():
    postings = get_index_for_word(SAMPLE_INDEX_DATA, "")

    assert postings == {}

def test_find_missing_term():
    postings = get_index_for_word(SAMPLE_INDEX_DATA, "missing")

    assert postings == {}

def test_find_multiple_terms():
    postings = get_index_for_word(SAMPLE_INDEX_DATA, "good friends")

    assert postings == {}