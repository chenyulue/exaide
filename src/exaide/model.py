import difflib
import re
from typing import Sequence


class TextCompareModel(difflib.SequenceMatcher):
    def __init__(
        self,
        text_original: Sequence[str],
        text_modified: Sequence[str],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(a=text_original, b=text_modified, *args, **kwargs)
        self._text_original = text_original
        self._text_modified = text_modified

    def reset_comparing_text(self, text_original, text_modified):
        self.set_seqs(
            a=text_original,
            b=text_modified,
        )
        self._text_original = text_original
        self._text_modified = text_modified

    def compare(self) -> list[tuple[str, int, int, int, int]]:
        cmp_result = self.get_opcodes()
        return cmp_result

    def get_similarity_ratio(self) -> float:
        return self.ratio()


class DescriptionModel:
    def __init__(
        self,
        description: Sequence[str],
        figures: Sequence[str],
        pattern: Sequence[str],
        phrases: list[str],
    ):
        self._description = description
        self._figures = figures
        self._phrases = phrases
        self._pattern = pattern

    def find_fig_numbers(self):
        fig_nums_in_description = list()
        fig_nums_in_figures = list()
        pattern = re.compile(self._pattern)

        start = 0
        while start < len(self._description):
            match = pattern.search(self._description, start)
            if match is None:
                break
            a, b = match.span()
            fig_nums_in_description.append((self._description[a:b], a, b))
            start = b

        start = 0
        while start < len(self._figures):
            match = pattern.search(self._figures, start)
            if match is None:
                break
            a, b = match.span()
            fig_nums_in_figures.append((self._figures[a:b], a, b))
            start = b

        return fig_nums_in_description, fig_nums_in_figures
