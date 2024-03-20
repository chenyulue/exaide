import pytest
import exaide.model as m


@pytest.fixture
def desc_model():
    desc = "[0001]这是第一段，包含图1和图2。\n[0002]这是第二段，包含图1、图2和图3。王总，这是编撰的。王总你改一改。"
    sw = ["王总", "编撰"]
    figs = "图1\n图5"
    return m.DescriptionModel(desc, sw, figs)


def test_count_paragraphs():
    desc = "[0001]这是第一段\n[0002]这是第二段"
    sw = ["王总", "编撰"]
    desc_model = m.DescriptionModel(desc, sw, "")
    assert desc_model.count_paragraphs() == 2


def test_search_figure_numbers(desc_model):
    desc_fig_diff, drawings_fig_diff = desc_model.search_figure_numbers()
    assert desc_fig_diff["图2"] == [(17, 19), (38, 40)]
    assert desc_fig_diff["图3"] == [(41, 43)]
    assert drawings_fig_diff["图5"] == [(3, 5)]


def test_search_figure_numbers_with_consistent_figures():
    desc = "说明书有图4(a)和图5-7"
    sw = ["王总", "编撰"]
    figs = "图4(a)\n图5-7"
    desc_model = m.DescriptionModel(desc, sw, figs)
    desc_fig_diff, drawings_fig_diff = desc_model.search_figure_numbers()
    assert desc_fig_diff == {}
    assert drawings_fig_diff == {}


def test_search_figure_numbers_with_hyphen():
    desc = "说明书有图4(a)和图5-7"
    sw = ["王总", "编撰"]
    figs = "图5-6"
    desc_model = m.DescriptionModel(desc, sw, figs)
    desc_fig_diff, drawings_fig_diff = desc_model.search_figure_numbers()
    assert desc_fig_diff["图4(a)"] == [(4, 9)]
    assert desc_fig_diff["图5-7"] == [(10, 14)]
    assert drawings_fig_diff["图5-6"] == [(0, 4)]


def test_search_figure_numbers_without_hyphen():
    desc = "说明书有图4(a)和图5-7"
    sw = ["王总", "编撰"]
    figs = "图8"
    desc_model = m.DescriptionModel(desc, sw, figs)
    desc_fig_diff, drawings_fig_diff = desc_model.search_figure_numbers()
    assert desc_fig_diff["图4(a)"] == [(4, 9)]
    assert desc_fig_diff["图5"] == [(10, 14)]
    assert desc_fig_diff["图7"] == [(10, 14)]
    assert drawings_fig_diff["图8"] == [(0, 2)]


def test_search_figure_numbers_with_different_kinds_of_pattern():
    desc = "说明书有图4(a)、图5-7、图1或2、图4(b')至6(c)以及图3到7，还有图9b'和19(c1')"
    sw = ["王总", "编撰"]
    figs = ""
    desc_model = m.DescriptionModel(desc, sw, figs)
    desc_fig_diff, drawings_fig_diff = desc_model.search_figure_numbers()
    assert set(desc_fig_diff) == {
        "图4(a)",
        "图5",
        "图7",
        "图1",
        "图2",
        "图4(b')",
        "图6(c)",
        "图3",
        "图9b'",
        "图19(c1')",
    }
    assert desc_fig_diff['图7'] == [(10, 14), (33, 37)]


def test_search_sensitive_words(desc_model):
    words = desc_model.search_sensitive_words()
    assert words["王总"] == [(44, 46), (53, 55)]
    assert words["编撰"] == [(49, 51)]
