from src.search import get_index_for_word, find_query


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
        "hello": {
            "1": {
                "frequency": 1,
                "positions": [2]
            },
            "2": {
                "frequency": 3,
                "positions": [0, 1, 3]
            }
        }
    },
}


##############################
# FIND INDEX FOR SINGLE TERM #
##############################
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


##############
# FIND QUERY #
##############
def test_find_single_term():
    results = find_query(SAMPLE_INDEX_DATA, "good")

    assert results == [
        {
            "document_id": "1",
            "url": "https://quotes.toscrape.com/",
            "title": "Home",
            "score": 2,
            "matched_terms": ["good"]
        },
        {
            "document_id": "2",
            "url": "https://quotes.toscrape.com/page/2/",
            "title": "Page 2",
            "score": 1,
            "matched_terms": ["good"]
        }
    ]


def test_find_several_terms():
    results = find_query(SAMPLE_INDEX_DATA, "good friends")

    assert results == [
        {
            "document_id": "1",
            "url": "https://quotes.toscrape.com/",
            "title": "Home",
            "score": 3,
            "matched_terms": ["good", "friends"]
        }
    ]


def test_find_case_and_punctuation_insensitive():
    results = find_query(SAMPLE_INDEX_DATA, "GOOD. friends! ")

    assert results == [
        {
            "document_id": "1",
            "url": "https://quotes.toscrape.com/",
            "title": "Home",
            "score": 3,
            "matched_terms": ["good", "friends"]
        }
    ]


def test_find_correct_ranking():
    results = find_query(SAMPLE_INDEX_DATA, "hello")

    assert results == [
        {
            "document_id": "2",
            "url": "https://quotes.toscrape.com/page/2/",
            "title": "Page 2",
            "score": 3,
            "matched_terms": ["hello"]
        },
        {
            "document_id": "1",
            "url": "https://quotes.toscrape.com/",
            "title": "Home",
            "score": 1,
            "matched_terms": ["hello"]
        }
    ]


def test_find_missing_query():
    results = find_query(SAMPLE_INDEX_DATA, "hello world")

    assert results == []


def test_find_empty_query():
    results = find_query(SAMPLE_INDEX_DATA, "")

    assert results == []