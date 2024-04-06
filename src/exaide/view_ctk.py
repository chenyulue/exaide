import customtkinter as ctk
import ctkdlib.custom_widgets as ctkdlib
import tkinter as tk


class _LabeledWidget(ctk.CTkFrame):
    def __init__(self, master, label, widget_class, orientation="vertical", **kwargs):
        super().__init__(master, fg_color="transparent")

        label = ctk.CTkLabel(self, text=label, fg_color="transparent")
        label.grid(row=0, column=0, sticky="w")

        widget = widget_class(self, **kwargs)
        if orientation == "vertical":
            widget.grid(row=1, column=0, pady=5, sticky="ew")
            self.columnconfigure(0, weight=1)
        elif orientation == "horizontal":
            widget.grid(row=0, column=1, padx=5, sticky="ew")
            self.columnconfigure(1, weight=1)
        else:
            raise ValueError(
                f'Invalid orientation: {orientation}. Only supports "vertical" or "horizontal"'
            )


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._parent = master

        # Build GUI
        ## Widgets for inputting and importing application number
        self._appnum_label = ctk.CTkLabel(
            self,
            text="案件申请号：",
            padx=0,
            pady=0,
        )

        self.appnum_var = tk.StringVar()
        self._appnum_entry = ctk.CTkEntry(
            self,
            placeholder_text="请输入申请号",
            textvariable=self.appnum_var,
            placeholder_text_color="gray",
        )

        self._import_btn = ctk.CTkButton(
            self,
            text="导入",
            command=lambda: self.event_generate("<<ImportApplication>>"),
        )

        ## Widgets for some utilities
        self._utilities_label = ctk.CTkLabel(self, text="实用工具")

        self._compare_hyperlink = ctkdlib.CTkHyperlink(
            self,
            text="文本比较工具",
            command=lambda: self.event_generate("<<OpenComparingWindow>>"),
        )
        self._deadline_hyperlink = ctkdlib.CTkHyperlink(
            self,
            text="周期管理",
            command=lambda: self.event_generate("<<OpenDeadlineWindow>>"),
        )
        self._cases_data_hyperlink = ctkdlib.CTkHyperlink(
            self,
            text="当月结案",
            command=lambda: self.event_generate("<<OpenCasesDataWindow>>"),
        )

        ## Widgets for check settings
        self._check_setting_label = ctk.CTkLabel(
            self,
            text="查找设置",
        )

        self._check_range_label = ctk.CTkLabel(self, text="查找范围：")

        self.check_range_var = tk.StringVar(value="整个申请")
        self._check_range_optionmenu = ctk.CTkOptionMenu(
            self,
            values=["整个申请", "权利要求", "说明书"],
            variable=self.check_range_var,
        )

        self.claim_seg_var = tk.BooleanVar(value=True)
        self._claim_seg_switch = ctk.CTkSwitch(
            self,
            text="权利要求自动分词",
            onvalue=True,
            offvalue=False,
            variable=self.claim_seg_var,
        )
        self._claim_seg_length_spinbox = _LabeledWidget(
            self,
            label="最短截词长度",
            widget_class=ctkdlib.CTkSpinbox,
            orientation="horizontal",
            from_=1,
            to=20,
            value=1,
        )

        ## Configure the grid position of widgets
        self._appnum_label.grid(row=0, column=0, sticky="w")
        self._appnum_entry.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="ew"
        )
        self._import_btn.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="e"
        )

        self._utilities_label.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="w"
        )
        self._compare_hyperlink.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="w"
        )
        self._deadline_hyperlink.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="w"
        )
        self._cases_data_hyperlink.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="w"
        )

        self._check_setting_label.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="w"
        )
        self._check_range_label.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="w"
        )
        self._check_range_optionmenu.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="ew"
        )
        self._claim_seg_switch.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="w"
        )
        self._claim_seg_length_spinbox.grid(
            row=self.grid_size()[1], column=self.grid_size()[0] - 1, sticky="ew"
        )

        self.columnconfigure(0, weight=1)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


if __name__ == "__main__":
    app = ctk.CTk()
    sidebar = Sidebar(app)
    sidebar.grid(sticky="ew")
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)
    app.mainloop()
