from . import view as v
from . import model as m

class Controller:
    def __init__(self, models, views):
        self._models = models
        self._views = views

    