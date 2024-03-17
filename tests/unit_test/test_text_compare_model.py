import pytest
from exaide import model as m

@pytest.fixture
def new_model():
    return m.TextCompareModel("abc", "abd")

def test_new_model(new_model):
    assert new_model.text_original == "abc"
    assert new_model.text_modified == "abd"

def test_reset_comparing_text(new_model):
    new_model.reset_comparing_text("我们", "你们")
    assert new_model.text_original == "我们"
    assert new_model.text_modified == "你们"

def test_compare(new_model):
    result = new_model.compare()
    assert result == [("equal", 0, 2, 0, 2), ("replace", 2, 3, 2, 3)]

def test_get_similarity_ratio(new_model):
    assert new_model.get_similarity_ratio() == 2/3