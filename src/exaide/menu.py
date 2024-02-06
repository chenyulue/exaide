import ttkbootstrap as ttk

class MenuBar(ttk.Menu):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # File menu
        file_menu = ttk.Menu(self, tearoff=False)
        file_menu.add_command(label="账号")
        file_menu.add_separator()
        file_menu.add_command(label="退出")
        self.add_cascade(label="文件", menu=file_menu)

        # Tool menu
        tool_menu = ttk.Menu(self, tearoff=False)
        
        display_menu = ttk.Menu(self, tearoff=False)
        display_menu.add_checkbutton(label="形式缺陷查找")
        display_menu.add_checkbutton(label="文本比较器")
        display_menu.add_checkbutton(label="审查周期查看")
        display_menu.add_checkbutton(label="当月结案数据")
        tool_menu.add_cascade(label="显示", menu=display_menu)
        
        tool_menu.add_command(label="设置")
        self.add_cascade(label="工具", menu=tool_menu)

        # Help menu
        help_menu = ttk.Menu(self, tearoff=False)
        help_menu.add_command(label="使用说明")
        help_menu.add_command(label="关于")
        self.add_cascade(label="帮助", menu=help_menu)
        