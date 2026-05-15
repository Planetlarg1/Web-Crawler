import json

from src.main import build, find, load, print_index, run_shell


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
    }
}


#########
# BUILD #
#########
def test_build_crawls_and_saves_index(monkeypatch, tmp_path, capsys):
    fake_pages = ["fake page"]
    fake_index = {"documents": {}, "index": {}}
    saved = {}

    def fake_crawl_site(max_pages=None):
        saved["max_pages"] = max_pages
        return fake_pages
    
    def fake_build_index(pages):
        saved["pages"] = pages
        return fake_index
    
    def fake_save_index(index_data, file_path):
        saved["index_data"] = index_data
        saved["file_path"] = file_path

    monkeypatch.setattr("src.main.crawl_site", fake_crawl_site)
    monkeypatch.setattr("src.main.build_index", fake_build_index)
    monkeypatch.setattr("src.main.save_index", fake_save_index)
    monkeypatch.setattr("src.main.INDEX_FILE_PATH", str(tmp_path / "index.json"))

    build()

    captured = capsys.readouterr()

    assert saved["pages"] == fake_pages
    assert saved["index_data"] == fake_index
    assert saved["file_path"] == str(tmp_path / "index.json")
    assert "Index saved" in captured.out


########
# LOAD #
########
def test_load_returns_index_with_file(monkeypatch, tmp_path, capsys):
    def fake_load_index(file_path):
        return SAMPLE_INDEX_DATA
    
    monkeypatch.setattr("src.main.load_index", fake_load_index)
    monkeypatch.setattr("src.main.INDEX_FILE_PATH", str(tmp_path / "index.json"))

    result = load()

    captured = capsys.readouterr()

    assert result == SAMPLE_INDEX_DATA
    assert "Index loaded" in captured.out


def test_load_returns_none_with_missing_file(monkeypatch, tmp_path, capsys):
    def fake_load_index(file_path):
        raise FileNotFoundError
    
    monkeypatch.setattr("src.main.load_index", fake_load_index)
    monkeypatch.setattr("src.main.INDEX_FILE_PATH", str(tmp_path / "missing.json"))

    result = load()

    captured = capsys.readouterr()

    assert result is None
    assert "Index does not exist" in captured.out


def test_load_returns_none_with_invalid_json(monkeypatch, tmp_path, capsys):
    def fake_load_index(file_path):
        raise json.JSONDecodeError("Invalid JSON", "doc", 0)
    
    monkeypatch.setattr("src.main.load_index", fake_load_index)
    monkeypatch.setattr("src.main.INDEX_FILE_PATH", str(tmp_path / "index.json"))

    result = load()

    captured = capsys.readouterr()

    assert result is None
    assert "Index file is invalid or corrupted" in captured.out


#########
# PRINT #
#########
def test_print_index_requires_loaded_index(capsys):
    print_index(None, "print good")

    captured = capsys.readouterr()

    assert "No index loaded" in captured.out


def test_print_index_requires_input(capsys):
    print_index(SAMPLE_INDEX_DATA, "print ")

    captured = capsys.readouterr()

    assert "Please provide a term to index" in captured.out


def test_print_index_rejects_multiple_words(capsys):
    print_index(SAMPLE_INDEX_DATA, "print good bad")

    captured = capsys.readouterr()

    assert "Print can only be used to index a single term" in captured.out


def test_print_no_results(capsys):
    print_index(SAMPLE_INDEX_DATA, "print orange")

    captured = capsys.readouterr()

    assert "No postings found for 'orange'" in captured.out


def test_print_outputs_results(capsys):
    print_index(SAMPLE_INDEX_DATA, "print good")

    captured = capsys.readouterr()

    assert "Postings for 'good'" in captured.out
    assert "Document 1" in captured.out
    assert "Frequency: 2" in captured.out
    assert "Location(s): 0, 3" in captured.out


########
# FIND #
########
def test_find_requires_loaded_index(capsys):
    find(None, "find good friends")

    captured = capsys.readouterr()

    assert "No index loaded" in captured.out


def test_find_requires_input(capsys):
    find(SAMPLE_INDEX_DATA, "find ")

    captured = capsys.readouterr()

    assert "Please provide a query to find" in captured.out


def test_find_displays_results_single_term(capsys):
    find(SAMPLE_INDEX_DATA, "find good")

    captured = capsys.readouterr()

    assert "Results for 'good' [2 page(s)]" in captured.out
    assert "https://quotes.toscrape.com/" in captured.out
    assert "https://quotes.toscrape.com/page/2/" in captured.out
    assert "Score: 2" in captured.out


def test_find_displays_results_multiple_terms(capsys):
    find(SAMPLE_INDEX_DATA, "find good friends")

    captured = capsys.readouterr()

    assert "Results for 'good friends' [1 page(s)]" in captured.out
    assert "https://quotes.toscrape.com/" in captured.out
    assert "Score: 3" in captured.out


def test_find_missing_results(capsys):
    find(SAMPLE_INDEX_DATA, "find good oranges")

    captured = capsys.readouterr()

    assert "No results for 'good oranges'" in captured.out


#########
# SHELL #
#########
def test_shell_disclaimers_print(monkeypatch, capsys):
    inputs = iter(["exit"])

    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    run_shell()

    captured = capsys.readouterr()

    assert "Running Web Scraper and Indexer..." in captured.out
    assert "- 'build'" in captured.out
    assert "- 'exit'" in captured.out


def test_shell_exits(monkeypatch, capsys):
    inputs = iter(["exit"])

    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    run_shell()

    captured = capsys.readouterr()

    assert "Program shutting down" in captured.out


def test_shell_unknown_command(monkeypatch, capsys):
    inputs = iter(["buildd", "exit"])

    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    run_shell()

    captured = capsys.readouterr()

    assert "Missing or unknown command" in captured.out


def test_shell_empty_command(monkeypatch, capsys):
    inputs = iter(["", "exit"])

    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    run_shell()

    captured = capsys.readouterr()

    assert "Missing or unknown command" in captured.out