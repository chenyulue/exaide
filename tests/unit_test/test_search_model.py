import pytest
from exaide import model as m

@pytest.fixture
def search_model():
    return m.SearchModel("hello world! hello people!", r"el+")

def test_new_model(search_model):
    assert search_model._content == "hello world! hello people!"
    assert search_model._pattern.pattern == "el+"

def test_search(search_model):
    from collections.abc import Iterator
    results = search_model.search()
    assert isinstance(results, Iterator)
    assert [(match.group(0), start, end) for match, start, end in results] == [("ell", 1, 4), ("ell", 14, 17)]