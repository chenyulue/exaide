import exaide.view as view
import exaide.model as model
import exaide.menu as menu

def test_compare_widget(root):
    cmp = view.ComparisonFrame(root)
    m = model.TextCompareModel("你好,世界", "大家好")
    cmp_result = m.compare()
    cmp.set_comparing_text(m.text_original, m.text_modified, cmp_result)

    def comparing(*_):
        a, b = cmp.get_comparing_text()
        m.reset_comparing_text(a, b)
        cmp.set_comparing_text(a, b, m.compare())

    def opening_file(event):
        cmp._sctext_result.insert("end", event.widget.filepath)
    cmp.bind("<<Comparing>>", comparing)
    root.mainloop()


def test_main_frame(root):
    menubar = menu.MenuBar(root)
    mframe = view.MainFrame(root)
    root.config(menu=menubar)
    root.mainloop()

def test_notebook(root):
    mframe = view.FormalDefectFrame(root)
    root.mainloop()