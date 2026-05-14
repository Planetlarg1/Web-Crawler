from src.indexer import (
    tokenise
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