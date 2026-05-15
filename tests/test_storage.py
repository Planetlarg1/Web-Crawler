from src.storage import save_index, load_index
from tests.test_search import SAMPLE_INDEX_DATA
import json


################
# INDEX SAVING #
################
def test_save_index_creates_file(tmp_path):
    file_path = tmp_path / "index.json"

    save_index(SAMPLE_INDEX_DATA, str(file_path))

    assert file_path.exists()


def test_save_stores_index(tmp_path):
    file_path = tmp_path / "index.json"

    save_index(SAMPLE_INDEX_DATA, str(file_path))

    with open(file_path, "r", encoding="utf-8") as file:
        assert json.load(file) == SAMPLE_INDEX_DATA


#################
# INDEX LOADING #
#################
def test_load_returns_index(tmp_path):
    file_path = tmp_path / "index.json"

    save_index(SAMPLE_INDEX_DATA, str(file_path))
    index = load_index(str(file_path))

    assert index == SAMPLE_INDEX_DATA