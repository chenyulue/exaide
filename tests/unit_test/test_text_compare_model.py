import pytest
from exaide import model as m

@pytest.fixture
def new_model():
    return m.TextCompareModel("abc", "abd")

def test_new_model(new_model):
    assert new_model._text_original == "abc"
    assert new_model._text_modified == "abd"

def test_reset_comparing_text(new_model):
    new_model.reset_comparing_text("我们", "你们")
    assert new_model._text_original == "我们"
    assert new_model._text_modified == "你们"