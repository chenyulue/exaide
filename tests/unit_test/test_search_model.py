import pytest
from exaide import model as m

@pytest.fixture
def search_model():
    return m.SearchModel("hello world! hello people!", r"el+")

def test_new_model(search_model):
    assert search_model._content == "hello world! hello people!"
    assert search_model._pattern == "el+"

def test_search(search_model):
    from collections.abc import Iterator
    results = search_model.search()
    assert isinstance(results, Iterator)
    assert list(results) == [("ell", 1, 4), ("ell", 14, 17)]