import ttkbootstrap as ttk
import ttkbootstrap.constants as tc
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog
from ttkbootstrap.dialogs.dialogs import Messagebox

import chardet


class ComparisonFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=10, **kwargs)
        self.pack(fill=tc.BOTH, expand=tc.YES)

        self._build_widgets()

    def _build_widgets(self):
        self.rowconfigure(1, weight=3)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

        label = "{}:\n请输入或[Ctrl+V]粘贴或点击[导入]按钮导入纯文本"
        label_left = ttk.Label(self, text=label.format("原始文本"))
        label_left.grid(
            row=0,
            column=0,
            sticky=tc.W,
        )
        label_right = ttk.Label(self, text=label.format("修改文本"))
        label_right.grid(row=0, column=3, sticky=tc.W)

        self._btn_left = ttk.Button(
            self,
            text="导入",
            command=lambda title="请选择原始文本": self._open_file(title),
        )
        self._btn_left.grid(row=0, column=1, sticky=tc.E)
        self._btn_right = ttk.Button(
            self,
            text="导入",
            command=lambda title="请选择修改文本": self._open_file(title),
        )
        self._btn_right.grid(row=0, column=4, sticky=tc.E)

        self._sctext_left = ScrolledText(self, autohide=True, wrap="word")
        self._sctext_left.grid(row=1, column=0, columnspan=2, sticky=tc.NSEW)
        self._sctext_right = ScrolledText(self, autohide=True, wrap="word")
        self._sctext_right.grid(row=1, column=3, columnspan=2, sticky=tc.NSEW)
        self._btn_cmp = ttk.Button(
            self,
            text="比较",
            bootstyle=(tc.PRIMARY, tc.OUTLINE),
            command=self._on_compare,
        )
        self._btn_cmp.grid(row=1, column=2, padx=3, sticky=tc.EW)

        label_result = ttk.Label(self, text="修改对照:")
        label_result.grid(row=2, column=0, sticky=tc.W)
        self._sctext_result = ScrolledText(self, autohide=True, height=10, wrap="word")
        self._sctext_result.grid(row=3, column=0, columnspan=5, sticky=tc.NSEW)

    @property
    def original_text(self):
        return self._sctext_left.get("1.0", "end")

    @property
    def modified_text(self):
        return self._sctext_right.get("1.0", "end")

    @property
    def comparison_result(self):
        return self._sctext_result.get("1.0", "end")

    @original_text.setter
    def original_text(self, text):
        self._sctext_left.delete("1.0", "end")
        self._sctext_left.insert("1.0", text)

    @modified_text.setter
    def modified_text(self, text):
        self._sctext_right.delete("1.0", "end")
        self._sctext_right.insert("1.0", text)

    @comparison_result.setter
    def comparison_result(self, text):
        self._sctext_result.delete("1.0", "end")
        self._sctext_result.insert("1.0", text)

    def _clean_text(self):
        self._sctext_left.delete("1.0", "end")
        self._sctext_right.delete("1.0", "end")
        self._sctext_result.delete("1.0", "end")

    def set_comparing_text(
        self,
        text_original,
        text_modified,
        cmp_contents: list[tuple[str, int, int, int, int]],
    ):
        self._clean_text()

        for tag, i1, i2, j1, j2 in cmp_contents:
            match tag:
                case "equal":
                    self._sctext_left.insert(
                        "end",
                        text_original[i1:i2],
                        ("equal",),
                    )
                    self._sctext_right.insert(
                        "end",
                        text_modified[j1:j2],
                        ("equal",),
                    )
                    self._sctext_result.insert(
                        "end",
                        text_original[i1:i2],
                        ("equal",),
                    )
                case _:
                    self._sctext_left.insert("end", text_original[i1:i2], ("original",))
                    self._sctext_right.insert(
                        "end", text_modified[j1:j2], ("modified",)
                    )
                    self._sctext_result.insert(
                        "end", text_original[i1:i2], (f"{tag}-original", "original")
                    )
                    self._sctext_result.insert(
                        "end", text_modified[j1:j2], (f"{tag}-modified", "modified")
                    )

        origin_color, modify_color = "red", "blue"
        self._sctext_left.tag_configure("original", foreground=origin_color)
        self._sctext_right.tag_configure("modified", foreground=modify_color)

        for tag in (
            "replace-original",
            "delete-original",
            "replace-modified",
            "insert-modified",
        ):
            if tag.endswith("original"):
                self._sctext_result.tag_configure(
                    tag, overstrike=True, foreground=origin_color
                )
            elif tag.endswith("modified"):
                self._sctext_result.tag_configure(
                    tag, underline=True, foreground=modify_color
                )

    def get_comparing_text(self):
        return self.original_text, self.modified_text

    def _on_compare(self):
        self.event_generate("<<Comparing>>")

    def _open_file(self, title):
        file_path = filedialog.askopenfilename(
            title=title,
            # parent=self,
            filetypes=[("文本文档", ".txt"), ("所有文件", "*")],
            defaultextension=".txt",
        )

        with open(file_path, "rb") as f:
            read_bytes = f.read()
            encoding = chardet.detect(read_bytes)["encoding"]
            try:
                if title == "请选择原始文本":
                    self.original_text = read_bytes.decode(encoding)
                else:
                    self.modified_text = read_bytes.decode(encoding)
            except (UnicodeDecodeError, UnicodeError):
                Messagebox.show_error(
                    message=(
                        f"检测到文本文档的编码格式为{encoding}，请确认\n"
                        f"实际编码格式是否匹配{encoding}。若不匹配，请\n"
                        "适当增加文本文档中字符数量以提高检测准确率。"
                    ),
                    title="文本编码错误",
                )
