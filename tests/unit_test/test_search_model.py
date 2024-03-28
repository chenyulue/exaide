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

def test_fignum_pattern():
    fignums = [
        "图1", "图12", "图 23", "图1、2和4", 
    ]
    fignum_p = m.SearchModel("\n".join(fignums), m.SettingModel().fignum_pattern)
    assert set(s.replace(' ', '').replace('图','') for s in fignums) == set(m.match.group(1) for m in fignum_p.search())