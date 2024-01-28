import pytest
import ttkbootstrap as ttk

@pytest.fixture()
def root():
    return ttk.Window()