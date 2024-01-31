from exaide import model as m


def test_description_model(desc_model):
    result = desc_model.find_fig_numbers()
    expected = (
        [("图4", 5, 7), ("图5", 8, 10), ("图12", 13, 16)],
        [("图1", 0, 2), ("图45", 4, 7), ("图9", 9, 11)],
    )

    assert result == expected
