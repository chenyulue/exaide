import pytest
import ttkbootstrap as ttk

from exaide import model as m

@pytest.fixture()
def root():
    return ttk.Window()

@pytest.fixture()
def desc_model():
    description = "说明书中有图4和图5，其中图12在后面。"
    figures = "图1\n\n图45\n\n图9"
    pattern = "图[0-9]+"
    phrases = ["中共", "党国"]
    model = m.DescriptionModel(description, figures, pattern, phrases)
    return model