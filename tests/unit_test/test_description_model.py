import pytest
import exaide.model as m

@pytest.fixture
def desc_model(desc):
    return m.DescriptionModel(desc, ["偏压", "补偿"])


def test_count_paragraphs(desc_model):
    assert desc_model.count_paragraphs() == 76

def test_search_figure_numbers(desc_model):
    fig_nums = desc_model.search_figure_numbers()
    assert fig_nums["图1"][0:3] == [(2, 4), (17, 19), (22, 34)]
    assert fig_nums["图4(a)"][0] == (22, 34)
    assert fig_nums["图8(d)"][0] == (22, 34)

def test_search_sensitive_words(desc_model):
    words = desc_model.search_sensitive_words()
    assert words["偏压"][0] == (7, 9)
    assert words["补偿"][0] == (9, 11)