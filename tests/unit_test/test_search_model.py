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

@pytest.mark.parametrize(
    "text, expected",
    [("这是图1。", {"图1"}), 
     ("说明书中有图12和图 1A", {"图12", "图 1A"}),
     ("图1(4)是一个子图，图1()不是完整的图号，但是也能检查出来", {"图1(4)", "图1()"}),
     ("(图1(4a'))在括号中", {"图1(4a')"}),
     ("连续图号图 1A、45，(b), ()、78a'和99(b)", {"图 1A、45，(b), ()、78a'和99(b)"}),
     ("连字号(图4-9)、图5或6、图8至9A，以及图9到10", {"图4-9", "图5或6", "图8至9A", "图9到10"}),
     ("图9到图10有两个图号", {"图9", "图10"})]
)
def test_fignum_pattern(text, expected):
    fignum = m.SearchModel(text, m.SettingModel().fignum_pattern)
    assert expected == set(m.match.group(0) for m in fignum.search())