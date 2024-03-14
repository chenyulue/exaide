import ttkbootstrap as ttk

class MenuBar(ttk.Menu):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.file_menu = ttk.Menu(self, tearoff=False)
        self.add(ttk.CASCADE, menu=self.file_menu, label='文件')
        self.file_menu.add("command", label='添加账号')
        self.file_menu.add("separator")
        self.file_menu.add("command", label='退出')

        self.add("command", label='设置')
        
        self.help_menu = ttk.Menu(self, tearoff=False)
        self.add(ttk.CASCADE, menu=self.help_menu, label='帮助')
        self.help_menu.add("command", label='使用手册')
        self.help_menu.add("command", label='关于')
        
        