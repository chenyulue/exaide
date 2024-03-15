import ttkbootstrap as ttk


from . import view as v
from . import model as m
from . import menu
from . import assets


class Application(ttk.Window):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            title="Exaide - 审查辅助帮手",
            iconphoto=str(assets.CMP_ICON),
            minsize=(800, 600),
            size=(1024, 768),
            *args,
            **kwargs,
        )
        self.configure(menu=menu.MenuBar(self))

        self.description_model = m.DescriptionModel
        self.compare_model = m.TextCompareModel

        self.mainwindow = v.ApplicationCheckFrame(self)
        self.mainwindow.bind("<<OpenComparingWindow>>", self._open_comparing_window)

        self.place_window_center()

    def run(self):
        self.mainloop()

    def _open_comparing_window(self, *_):
        cmp_win = ttk.Toplevel(
            title="文本比对",
            iconphoto=str(assets.CMP_ICON),
            minsize=(800, 600),
        )
        self.compare_window = v.CmpFrame(cmp_win)

        self.compare_window.bind("<<Comparing>>", self._comparing)

        cmp_win.place_window_center()

    def _comparing(self, *_):
        a, b = (
            self.compare_window.original_content.rstrip(),
            self.compare_window.modified_content.rstrip(),
        )
        cmp_model = self.compare_model(a, b)
        cmp_result = cmp_model.compare()
        self.compare_window.set_compare_result(cmp_result)
        self.compare_window.show_cmp_similarity(cmp_model.get_similarity_ratio())


if __name__ == "__main__":
    Application().run()
