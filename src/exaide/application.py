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
        self._bind_events()

        self.place_window_center()

    def run(self) -> None:
        self.mainloop()

    def _bind_events(self) -> None:
        self.mainwindow.bind("<<OpenComparingWindow>>", self._open_comparing_window)
        self.mainwindow.bind("<<CheckingDefects>>", self._check_defects)

    def _check_defects(self, *_) -> None:
        find_range = self.mainwindow.find_range_var.get()
        if find_range == "说明书" or find_range == "全部":
            self._check_description_defects()
        if find_range == "权利要求" or find_range == "全部":
            self._check_claim_defects()
        if find_range == "全部":
            self._check_other_defects()

    def _check_description_defects(self) -> None:
        desc_text = self.mainwindow.description_text.get("1.0", "end")
        fig_text = self.mainwindow.figure_text.get("1.0", "end")
        sensitive_words = m.SettingModel().sensitive_words
        desc_model = self.description_model(desc_text, sensitive_words, fig_text)

        for tag in self.mainwindow.description_text.tag_names():
            self.mainwindow.description_text.tag_delete(tag)

        # Search sensitive words
        sensitive_words_result = desc_model.search_sensitive_words()
        self.mainwindow.show_description_check_results(
            sensitive_words=sensitive_words_result,
        )

    def _check_claim_defects(self):
        print("Claim defects")

    def _check_other_defects(self):
        print("Other defects")

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
