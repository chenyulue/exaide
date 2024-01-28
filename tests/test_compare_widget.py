import exaide.view as view
import exaide.model as model

def test_compare_widget(root):
    cmp = view.ComparisonFrame(root)
    m = model.TextCompareModel("你好,世界", "大家好")
    cmp_result = m.compare()
    cmp.set_comparing_text(m._text_original, m._text_modified, cmp_result)

    def comparing(*_):
        a, b = cmp.get_comparing_text()
        m._compare_model.set_seqs(a, b)
        cmp.set_comparing_text(a, b, m.compare())
    cmp.bind("<<Comparing>>", comparing)
    root.mainloop()