import pytest
import ttkbootstrap as ttk

from exaide import model as m

@pytest.fixture()
def root():
    return ttk.Window()