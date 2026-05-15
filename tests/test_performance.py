import time

from src.crawler import CrawledPage
from src.indexer import build_index
from src.search import find_query


def make_fake_pages(page_count: int) -> list[CrawledPage]:
    pages = []

    for i in range(page_count):
        text = (
            "It is our choices, Harry, that show what we truly are, far more than our abilities. "
            "Try not to become a man of success. Rather become a man of value."
        ) * 50

        pages.append(
            CrawledPage(
                url=f"https://quotes.toscrape.com/page/{i}/",
                title=f"Page {i}",
                text=text
            )
        )

    return pages


################################
# INDEX GENERATION PERFORMANCE #
################################
def test_build_index_performance():
    pages_100 = make_fake_pages(100)
    pages_500 = make_fake_pages(500)
    pages_2500 = make_fake_pages(2500)

    # 100 pages
    start_time = time.perf_counter()
    index_100 = build_index(pages_100)
    elapsed_100 = time.perf_counter() - start_time

    # 500 pages
    start_time = time.perf_counter()
    index_500 = build_index(pages_500)
    elapsed_500 = time.perf_counter() - start_time

    # 2500 pages
    start_time = time.perf_counter()
    index_2500 = build_index(pages_2500)
    elapsed_2500 = time.perf_counter() - start_time

    assert len(index_100["documents"]) == 100
    assert len(index_500["documents"]) == 500
    assert len(index_2500["documents"]) == 2500

    assert elapsed_100 < 0.1
    assert elapsed_500 < 0.5
    assert elapsed_2500 < 2.5


#####################
# QUERY PERFORMANCE #
#####################
def test_query_performance():
    pages_100 = make_fake_pages(100)
    pages_500 = make_fake_pages(500)
    pages_2500 = make_fake_pages(2500)

    index_100 = build_index(pages_100)
    index_500 = build_index(pages_500)
    index_2500 = build_index(pages_2500)

    # 100 pages
    start_time = time.perf_counter()
    results_100 = find_query(index_100, "Harry value")
    elapsed_100 = time.perf_counter() - start_time

    # 500 pages
    start_time = time.perf_counter()
    results_500 = find_query(index_500, "Harry value")
    elapsed_500 = time.perf_counter() - start_time

    # 2500 pages
    start_time = time.perf_counter()
    results_2500 = find_query(index_2500, "Harry value")
    elapsed_2500 = time.perf_counter() - start_time

    assert len(results_100) == 100
    assert len(results_500) == 500
    assert len(results_2500) == 2500

    assert elapsed_100 < 0.1
    assert elapsed_500 < 0.5
    assert elapsed_2500 < 2.5

