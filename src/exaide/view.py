import ttkbootstrap as ttk
from tkinter import filedialog
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.icons import Emoji
import os
import itertools

import chardet

from . import model as m
from .utilities import Color


class ApplicationCheckFrame(ttk.Frame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, padding=5, **kwargs)
        self._build_ui()
        self._config_widgets()
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
        self.compare_btn.configure(text="文本比对")
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
        self.right_frame.configure(height=200, width=800)
        self.application_pane = ttk.Notebook(self.right_frame, name="application_pane")
        self.application_pane.configure(height=300, width=600)
        self.abs_text = ttk.ScrolledText(self.application_pane, name="abs_text")
        self.abs_text.configure(height=10, width=80)
        self.abs_text.grid(column=0, row=0, sticky="nsew")
        self.application_pane.add(self.abs_text, text="摘要")
        self.claim_text = ttk.ScrolledText(self.application_pane, name="claim_text")
        self.claim_text.configure(height=10, width=80)
        self.claim_text.grid(column=0, row=0, sticky="nsew")
        self.application_pane.add(self.claim_text, text="权利要求")
        self.description_text = ttk.ScrolledText(
            self.application_pane, name="description_text"
        )
        self.description_text.configure(height=10, width=80)
        self.description_text.grid(column=0, row=0, sticky="nsew")
        self.application_pane.add(self.description_text, text="说明书")
        self.figure_text = ttk.ScrolledText(self.application_pane, name="figure_text")
        self.figure_text.configure(height=10, width=80)
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
        self.clear_btn = ttk.Button(self.check_result_frame, name="check_btn")
        self.clear_btn.configure(text="清    空")
        self.clear_btn.grid(column=2, row=0)
        self.check_btn = ttk.Button(self.check_result_frame, name="clear_btn")
        self.check_btn.configure(text="查    找")
        self.check_btn.grid(column=1, row=0, sticky="e")
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

    def _config_widgets(self) -> None:
        self.compare_btn.configure(command=self._show_cmp_win)

        self.find_range_var = ttk.StringVar(value="全部")
        self.find_range_comb.configure(
            textvariable=self.find_range_var, state="readonly"
        )

        self.seg_checker_var = ttk.BooleanVar(value=True)
        self.seg_checker_var.trace_add("write", self._toggle_seg_length_spinbox)
        self.seg_checker.configure(variable=self.seg_checker_var)

        self.seg_length_var = ttk.IntVar(value=1)
        self.seg_length_spinbox.configure(
            textvariable=self.seg_length_var,
            from_=1,
            to=20,
            increment=1,
        )
        self._toggle_seg_length_spinbox()

        self.clear_btn.configure(command=self._clear_app_data)
        self.check_btn.configure(command=self._check_defects)

    def show_description_check_results(self, **kwargs) -> None:
        for tag in self.description_text.tag_names():
            self.description_text.tag_delete(tag)
        self.description_check_text.delete("1.0", "end")
        
        if ("sensitive_words" in kwargs) and kwargs["sensitive_words"]:
            self._highlight_sensitive_words(kwargs["sensitive_words"], Color.RED)

    def _highlight_sensitive_words(
        self, results: m.SearchResults, color: Color
    ) -> None:
        emoji = Emoji.get("closed book")
        emoji = emoji.char if emoji is not None else ""
        self.description_check_text.insert(
            "end",
            emoji + " 可能的敏感词：\n",
            ("sensitive_words_title",),
        )

        for word, positions in results.items():
            self.description_check_text.insert("end", word, (word,))
            self.description_check_text.insert("end", " ")
            self.description_check_text.tag_bind(
                word,
                "<Button-1>",
                self._find_and_jump(
                    word,
                    positions,
                    self.description_text,
                ),
            )

            for start, end in positions:
                self.description_text.tag_add(
                    "sensitive_words", f"1.0+{start}c", f"1.0+{end}c"
                )
                self.description_text.tag_add(word, f"1.0+{start}c", f"1.0+{end}c")

        self.description_text.tag_configure("sensitive_words", foreground=color.value)

    def _find_and_jump(
        self, word: str, pos: list[tuple[int, int]], where: ttk.ScrolledText
    ):
        n = 0

        def _event(*_):
            nonlocal n
            count = len(pos)
            current = n % count
            where.see(f"1.0+{pos[current][1]}c")
            if n > 0:
                pre = (n - 1) % count
                where.tag_remove(
                    "current_sel", f"1.0+{pos[pre][0]}c", f"1.0+{pos[pre][1]}c"
                )
            where.tag_add(
                "current_sel", f"1.0+{pos[current][0]}c", f"1.0+{pos[current][1]}c"
            )
            where.tag_configure("current_sel", background="yellow")
            n += 1

        return _event

    def _clear_app_data(self) -> None:
        for child in itertools.chain(
            self.application_pane.winfo_children(),
            self.check_result_pane.winfo_children(),
        ):
            text_widget = [w for s, w in child.children.items() if s.endswith("_text")][
                0
            ]
            text_widget.delete("1.0", "end")  # pyright: ignore

    def _check_defects(self) -> None:
        self.event_generate("<<CheckingDefects>>")

    def _show_cmp_win(self) -> None:
        self.event_generate("<<OpenComparingWindow>>")

    def _toggle_seg_length_spinbox(self, *_):
        if self.seg_checker_var.get():
            self.seg_length_spinbox.configure(state="disabled")
        else:
            self.seg_length_spinbox.configure(state="readonly")


class CmpFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=5, **kwargs)
        self._build_ui()
        self._config_widgets()
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
    def original_content(self, text: str) -> None:
        self.original_text.delete("1.0", "end")
        self.original_text.insert("1.0", text)

    @modified_content.setter
    def modified_content(self, text: str) -> None:
        self.modified_text.delete("1.0", "end")
        self.modified_text.insert("1.0", text)

    @cmp_result_content.setter
    def cmp_result_content(self, text: str) -> None:
        self.cmp_result_text.delete("1.0", "end")
        self.cmp_result_text.insert("1.0", text)

    def _clean_text(self) -> None:
        for txt_widget in [
            self.original_text,
            self.modified_text,
            self.cmp_result_text,
        ]:
            txt_widget.delete("1.0", "end")

        self.cmp_result_label.configure(text="修改对照：")

    def set_compare_result(
        self, cmp_results: list[tuple[str, int, int, int, int]]
    ) -> None:
        # Initialize the text highlighting state for each round of comparison
        self.cmp_result_text.delete("1.0", "end")
        for tag in self.original_text.tag_names():
            self.original_text.tag_delete(tag)
        for tag in self.modified_text.tag_names():
            self.modified_text.tag_delete(tag)

        for tag, i1, i2, j1, j2 in cmp_results:
            if tag == "equal":
                self.modified_text.tag_add("equal", f"1.0+{j1}c", f"1.0+{j2}c")
                self.original_text.tag_add("equal", f"1.0+{i1}c", f"1.0+{i2}c")
                self.cmp_result_text.insert(
                    "end", self.original_content[i1:i2], "equal"
                )
            else:
                self.modified_text.tag_add("modified", f"1.0+{j1}c", f"1.0+{j2}c")
                self.original_text.tag_add("original", f"1.0+{i1}c", f"1.0+{i2}c")
                self.cmp_result_text.insert(
                    "end", self.original_content[i1:i2], (f"{tag}-original", "original")
                )
                self.cmp_result_text.insert(
                    "end", self.modified_content[j1:j2], (f"{tag}-modified", "modified")
                )

        origin_color, modify_color = "red", "blue"
        self.original_text.tag_configure("original", foreground=origin_color)
        self.modified_text.tag_configure("modified", foreground=modify_color)

        for tag in (
            "replace-original",
            "delete-original",
            "replace-modified",
            "insert-modified",
        ):
            if tag.endswith("original"):
                self.cmp_result_text.tag_configure(
                    tag, overstrike=True, foreground=origin_color
                )
            elif tag.endswith("modified"):
                self.cmp_result_text.tag_configure(
                    tag, underline=True, foreground=modify_color
                )

    def _on_cmp_btn_click(self) -> None:
        self.event_generate("<<Comparing>>")

    def show_cmp_similarity(self, ratio) -> None:
        new_label = f"修改对照 (相似度 {ratio*100:.2f}%)："
        self.cmp_result_label.configure(text=new_label)

    def _open_file(self, title: str, encode: str | None = None) -> None:
        file_path = filedialog.askopenfilename(
            title=title,
            # parent=self,
            filetypes=[("文本文档", ".txt"), ("所有文件", "*")],
            defaultextension=".txt",
            parent=self,
        )

        if not os.path.exists(file_path):
            return

        with open(file_path, "rb") as f:
            read_bytes = f.read()

            encoding = (
                chardet.detect(read_bytes)["encoding"] if encode is None else encode
            )
            if encoding is None:
                Messagebox.show_warning(
                    message='没有检测到有效的文本编码，将默认\n以"UTF-8"编码格式打开文本',
                    title="文本编码检测失效",
                )
                encoding = "utf-8"
            try:
                if title == "请选择原始文本":
                    self.original_content = read_bytes.decode(encoding)
                else:
                    self.modified_content = read_bytes.decode(encoding)
            except (UnicodeDecodeError, UnicodeError):
                Messagebox.show_error(
                    message=(
                        f"以编码格式{encoding}打开文本，请确认实际\n"
                        f"编码格式是否匹配{encoding}。若不匹配，请\n"
                        "适当增加文本文档中字符数量以提高检测准确率,\n"
                        "或者以“UTF-8无签名”编码格式重新保存文档后\n"
                        "再读取。"
                    ),
                    title="文本编码错误",
                )
                self._open_file(title, encode="utf-8")

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
        self.modified_import_btn.configure(
            text="导入修改",
            width=9,
        )
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
        self.clean_btn = ttk.Button(self.cmp_clear_frame)
        self.clean_btn.configure(text="清 空", width=5)
        self.clean_btn.grid(column=0, pady=10, row=1)
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
        self.original_import_btn.configure(
            text="导入原始",
            width=9,
        )
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

    def _config_widgets(self):
        self.modified_import_btn.configure(
            command=lambda title="请选择修改文本": self._open_file(title),
        )
        self.original_import_btn.configure(
            command=lambda title="请选择原始文本": self._open_file(title),
        )

        self.cmp_btn.configure(command=self._on_cmp_btn_click)
        self.clean_btn.configure(command=self._clean_text)


if __name__ == "__main__":
    from .menu import MenuBar

    win = ttk.Window(
        title="Exaide - 审查辅助帮手",
    )
    ApplicationCheckFrame(win)
    win.configure(menu=MenuBar(win))
    win.mainloop()
