import pytest
import exaide.model as m

@pytest.fixture
def desc_model(desc):
    return m.DescriptionModel(desc)


def test_count_paragraphs(desc_model):
    assert desc_model.count_paragraphs() == 76