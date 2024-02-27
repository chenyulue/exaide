import pytest
import exaide.model as m

@pytest.fixture
def desc_model(desc):
    return m.DescriptionModel(desc)


def test_count_paragraphs(desc_model):
    assert desc_model.count_paragraphs() == 76

def test_search_figure_numbers(desc_model):
    fig_nums = desc_model.search_figure_numbers()
    assert fig_nums["图1"][0:3] == [(2, 4), (17, 19), (22, 34)]
    assert fig_nums["图4(a)"][0] == (22, 34)
    assert fig_nums["图8(d)"][0] == (22, 34)