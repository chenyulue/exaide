import ttkbootstrap as ttk
from tkinter import filedialog
from ttkbootstrap.dialogs.dialogs import Messagebox

import chardet


class ApplicationCheckFrame(ttk.Frame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, padding=5, **kwargs)
        self._build_ui()
        self.pack(fill="both", expand=True)

    def _build_ui(self) -> None:
        # build ui
        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.left_frame = ttk.Frame(self, name="left_frame")
        self.left_frame.configure(height=200, width=400)
        self.application_number_label = ttk.Label(
            self.left_frame, name="application_number_label"
        )
        self.application_number_label.configure(text="案件申请号：")
        self.application_number_label.grid(
            column=0, padx=5, pady="5 0", row=0, sticky="w"
        )
        self.application_number_entry = ttk.Entry(
            self.left_frame, name="application_number_entry"
        )
        self.application_number_entry.grid(
            column=0, padx=5, pady="0 3", row=1, sticky="ew"
        )
        self.application_number_import_btn = ttk.Button(
            self.left_frame, name="application_number_import_btn"
        )
        self.application_number_import_btn.configure(text="导入")
        self.application_number_import_btn.grid(
            column=0, padx=5, pady="0 5", row=2, sticky="e"
        )
        self.utilities_frame = ttk.Labelframe(self.left_frame, name="utilities_frame")
        self.utilities_frame.configure(height=200, text="实用工具", width=200)
        self.compare_btn = ttk.Button(self.utilities_frame, name="compare_btn")
        self.compare_btn.configure(text="文本比对", command=self._show_cmp_win)
        self.compare_btn.grid(column=0, padx=5, pady="7 5", row=0, sticky="w")
        self.period_btn = ttk.Button(self.utilities_frame, name="period_btn")
        self.period_btn.configure(text="周期管理")
        self.period_btn.grid(column=0, padx=5, pady=5, row=1, sticky="w")
        self.cases_btn = ttk.Button(self.utilities_frame, name="cases_btn")
        self.cases_btn.configure(text="当月结案")
        self.cases_btn.grid(column=0, padx=5, pady=5, row=2, sticky="w")
        self.utilities_frame.grid(column=0, padx=5, pady=10, row=3, sticky="nsew")
        self.find_setting_btn = ttk.Labelframe(self.left_frame, name="find_setting_btn")
        self.find_setting_btn.configure(height=200, text="查找设置", width=200)
        self.find_range_label = ttk.Label(
            self.find_setting_btn, name="find_range_label"
        )
        self.find_range_label.configure(text="查找范围：")
        self.find_range_label.grid(column=0, padx=5, pady="5 0", row=0, sticky="w")
        self.find_range_comb = ttk.Combobox(
            self.find_setting_btn, name="find_range_comb"
        )
        self.find_range_comb.configure(values=["全部", "权利要求", "说明书"])
        self.find_range_comb.grid(column=0, padx=5, pady="0 5", row=1, sticky="w")
        self.seg_checker = ttk.Checkbutton(self.find_setting_btn, name="seg_checker")
        self.seg_checker.configure(text="权利要求自动分词")
        self.seg_checker.grid(column=0, padx=5, pady="10 0", row=2, sticky="w")
        self.seg_length_frame = ttk.Frame(
            self.find_setting_btn, name="seg_length_frame"
        )
        self.seg_length_frame.configure(height=200, width=200)
        self.seg_length_label = ttk.Label(
            self.seg_length_frame, name="seg_length_label"
        )
        self.seg_length_label.configure(text="最短截词长度")
        self.seg_length_label.grid(column=0, padx="30 5", row=0, sticky="w")
        self.seg_length_spinbox = ttk.Spinbox(
            self.seg_length_frame, name="seg_length_spinbox"
        )
        self.seg_length_spinbox.configure(width=5)
        self.seg_length_spinbox.grid(column=1, padx="5 10", row=0, sticky="w")
        self.seg_length_frame.grid(column=0, padx=5, row=3, sticky="w")
        self.find_setting_btn.grid(column=0, padx=5, pady=5, row=4, sticky="nsew")
        self.left_frame.grid(column=0, row=0, sticky="nsew")
        self.left_frame.rowconfigure(3, weight=1)
        self.left_frame.rowconfigure(4, weight=1)
        self.right_frame = ttk.Frame(self, name="right_frame")
        self.right_frame.configure(height=200, width=200)
        self.application_pane = ttk.Notebook(self.right_frame, name="application_pane")
        self.application_pane.configure(height=300, width=600)
        self.abs_text = ttk.ScrolledText(self.application_pane, name="abs_text")
        self.abs_text.configure(height=10, width=60)
        self.abs_text.grid(column=0, row=0, sticky="nsew")
        self.application_pane.add(self.abs_text, text="摘要")
        self.claim_text = ttk.ScrolledText(self.application_pane, name="claim_text")
        self.claim_text.configure(height=10, width=50)
        self.claim_text.grid(column=0, row=0, sticky="nsew")
        self.application_pane.add(self.claim_text, text="权利要求")
        self.description_text = ttk.ScrolledText(
            self.application_pane, name="description_text"
        )
        self.description_text.configure(height=10, width=50)
        self.description_text.grid(column=0, row=0, sticky="nsew")
        self.application_pane.add(self.description_text, text="说明书")
        self.figure_text = ttk.ScrolledText(self.application_pane, name="figure_text")
        self.figure_text.configure(height=10, width=50)
        self.figure_text.grid(column=0, row=0, sticky="nsew")
        self.application_pane.add(self.figure_text, text="附图图号")
        self.application_pane.grid(column=0, padx=5, pady=5, row=1, sticky="nsew")
        self.check_result_pane = ttk.Notebook(
            self.right_frame, name="check_result_pane"
        )
        self.check_result_pane.configure(height=200, width=600)
        self.claim_check_text = ttk.ScrolledText(
            self.check_result_pane, name="claim_check_text"
        )
        self.claim_check_text.configure(height=10, width=50)
        self.claim_check_text.grid(column=0, row=0, sticky="nsew")
        self.check_result_pane.add(self.claim_check_text, text="权利要求")
        self.description_check_text = ttk.ScrolledText(
            self.check_result_pane, name="description_check_text"
        )
        self.description_check_text.configure(height=10, width=50)
        self.description_check_text.grid(column=0, row=0, sticky="nsew")
        self.check_result_pane.add(self.description_check_text, text="说明书")
        self.others_check_text = ttk.ScrolledText(
            self.check_result_pane, name="others_check_text"
        )
        self.others_check_text.configure(height=10, width=50)
        self.others_check_text.grid(column=0, row=0, sticky="nsew")
        self.check_result_pane.add(self.others_check_text, text="其他问题")
        self.check_result_pane.grid(column=0, padx=5, pady="0 10", row=3, sticky="nsew")
        self.check_result_frame = ttk.Frame(self.right_frame, name="check_result_frame")
        self.check_result_frame.configure(height=200, width=200)
        self.check_result_label = ttk.Label(
            self.check_result_frame, name="check_result_label"
        )
        self.check_result_label.configure(text="检查结果：")
        self.check_result_label.grid(column=0, row=0, sticky="w")
        self.check_btn = ttk.Button(self.check_result_frame, name="check_btn")
        self.check_btn.configure(text="清    空")
        self.check_btn.grid(column=2, row=0)
        self.clear_btn = ttk.Button(self.check_result_frame, name="clear_btn")
        self.clear_btn.configure(text="查    找")
        self.clear_btn.grid(column=1, row=0, sticky="e")
        self.check_result_frame.grid(column=0, padx=5, pady="5 0", row=2, sticky="ew")
        self.check_result_frame.columnconfigure(0, weight=1)
        self.check_result_frame.columnconfigure(1, weight=1)
        self.check_result_frame.columnconfigure(2, weight=1)
        self.right_frame.grid(column=2, row=0, sticky="nsew")
        self.right_frame.rowconfigure(1, weight=3)
        self.right_frame.rowconfigure(3, weight=2)
        self.right_frame.columnconfigure(0, weight=1)
        self.separator1 = ttk.Separator(self, orient="vertical")
        self.separator1.grid(column=1, row=0, sticky="ns")

    def _show_cmp_win(self) -> None:
        cmp_win = ttk.Toplevel(title="文本比较")
        CmpFrame(cmp_win)


class CmpFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=5, **kwargs)
        self._build_ui()
        self.pack(fill="both", expand=True)

    @property
    def original_content(self) -> str:
        return self.original_text.get("1.0", "end")

    @property
    def modified_content(self) -> str:
        return self.modified_text.get("1.0", "end")

    @property
    def cmp_result_content(self) -> str:
        return self.cmp_result_text.get("1.0", "end")

    @original_content.setter
    def original_content(self, text) -> None:
        self.original_text.delete("1.0", "end")
        self.original_text.insert("1.0", text)

    @modified_content.setter
    def modified_content(self, text) -> None:
        self.modified_text.delete("1.0", "end")
        self.modified_text.insert("1.0", text)

    @cmp_result_content.setter
    def cmp_result_content(self, text) -> None:
        self.cmp_result_text.delete("1.0", "end")
        self.cmp_result_text.insert("1.0", text)

    def _clean_text(self) -> None:
        for txt_widget in [
            self.original_text,
            self.modified_text,
            self.cmp_result_text,
        ]:
            txt_widget.delete("1.0", "end")

    def set_compare_result(self, cmp_contents: list[tuple[str, int, int, int, int]]) -> None:
        pass

    def _build_ui(self) -> None:
        # build ui
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.modified_frame = ttk.Frame(self, name="modified_frame")
        self.modified_frame.configure(height=500, width=200)
        self.modified_label = ttk.Label(self.modified_frame, name="modified_label")
        self.modified_label.configure(
            text="修改文本：\n请输入或Ctrl+V粘贴或点击[导入修改]按钮导入纯文本"
        )
        self.modified_label.grid(column=0, row=0, sticky="w")
        self.modified_import_btn = ttk.Button(
            self.modified_frame, name="modified_import_btn"
        )
        self.modified_import_btn.configure(text="导入修改", width=9)
        self.modified_import_btn.grid(column=1, row=0, sticky="e")
        self.modified_text = ttk.ScrolledText(self.modified_frame, name="modified_text")
        self.modified_text.configure(height=20, width=55)
        self.modified_text.grid(column=0, columnspan=2, row=1, sticky="nsew")
        self.modified_frame.grid(column=0, padx=5, pady=5, row=0, sticky="nsew")
        self.modified_frame.rowconfigure(1, weight=1)
        self.modified_frame.columnconfigure(0, weight=1)
        self.modified_frame.columnconfigure(1, weight=1)
        self.cmp_clear_frame = ttk.Frame(self, name="cmp_clear_frame")
        self.cmp_clear_frame.configure(height=200, width=200)
        self.cmp_btn = ttk.Button(self.cmp_clear_frame, name="cmp_btn")
        self.cmp_btn.configure(text="比 较", width=5)
        self.cmp_btn.grid(column=0, pady=10, row=0)
        self.button14 = ttk.Button(self.cmp_clear_frame)
        self.button14.configure(text="清 空", width=5)
        self.button14.grid(column=0, pady=10, row=1)
        self.cmp_clear_frame.grid(column=1, padx=0, pady=5, row=0)
        self.original_frame = ttk.Frame(self, name="original_frame")
        self.original_frame.configure(height=500, width=200)
        self.original_label = ttk.Label(self.original_frame, name="original_label")
        self.original_label.configure(
            text="原始文本：\n请输入或Ctrl+V粘贴或点击[导入原始]按钮导入纯文本"
        )
        self.original_label.grid(column=0, row=0, sticky="w")
        self.original_import_btn = ttk.Button(
            self.original_frame, name="original_import_btn"
        )
        self.original_import_btn.configure(text="导入原始", width=9)
        self.original_import_btn.grid(column=1, row=0, sticky="e")
        self.original_text = ttk.ScrolledText(self.original_frame, name="original_text")
        self.original_text.configure(height=20, width=55)
        self.original_text.grid(column=0, columnspan=2, row=1, sticky="nsew")
        self.original_frame.grid(column=2, padx=5, pady=5, row=0, sticky="nsew")
        self.original_frame.rowconfigure(1, weight=1)
        self.original_frame.columnconfigure(0, weight=1)
        self.original_frame.columnconfigure(1, weight=1)
        self.cmp_result_label = ttk.Label(self, name="cmp_result_label")
        self.cmp_result_label.configure(text="修改对照：")
        self.cmp_result_label.grid(
            column=0, columnspan=3, padx=5, pady="10 3", row=1, sticky="ew"
        )
        self.cmp_result_frame = ttk.Frame(self, name="cmp_result_frame")
        self.cmp_result_frame.configure(height=200, width=200)
        self.cmp_result_text = ttk.ScrolledText(
            self.cmp_result_frame, name="cmp_result_text"
        )
        self.cmp_result_text.configure(height=15, width=50)
        self.cmp_result_text.grid(column=0, row=0, sticky="nsew")
        self.cmp_result_frame.grid(
            column=0, columnspan=3, padx=5, pady="0 5", row=2, sticky="nsew"
        )
        self.cmp_result_frame.rowconfigure(0, weight=1)
        self.cmp_result_frame.columnconfigure(0, weight=1)


if __name__ == "__main__":
    from .menu import MenuBar

    win = ttk.Window(
        title="Exaide - 审查辅助帮手",
    )
    ApplicationCheckFrame(win)
    win.configure(menu=MenuBar(win))
    win.mainloop()
