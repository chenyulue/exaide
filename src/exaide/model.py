import difflib
import re

from typing import Iterator, NamedTuple


# text comparison model
class TextCompareModel(difflib.SequenceMatcher):
    def __init__(
        self,
        text_original: str,
        text_modified: str,
    ) -> None:
        super().__init__(a=text_original, b=text_modified)
        self.text_original = text_original
        self.text_modified = text_modified

    def reset_comparing_text(self, text_original: str, text_modified: str) -> None:
        self.set_seqs(
            a=text_original,
            b=text_modified,
        )
        self.text_original = text_original
        self.text_modified = text_modified

    def compare(self) -> list[tuple[str, int, int, int, int]]:
        cmp_results = self.get_opcodes()
        return cmp_results

    def get_similarity_ratio(self) -> float:
        return self.ratio()


# text search model
class SearchResult(NamedTuple):
    match: re.Match[str]
    start: int
    end: int


class SearchModel:
    def __init__(
        self,
        content: str,
        pattern: str,
        *kwargs: re._FlagsType
    ):
        self._content = content
        self._pattern = re.compile(pattern, *kwargs)

    def search(self) -> Iterator[SearchResult]:
        match = self._pattern.search(self._content, 0)
        while match is not None:
            start, end = match.span()
            yield SearchResult(match=match, start=start, end=end)
            match = self._pattern.search(self._content, end)


# Model that represents a description of a patent
class FigureNumbers(NamedTuple):
    figs: set[str]
    positions: list[tuple[str, int, int]]
    
class DescriptionModel:
    def __init__(self, description: str, figure_numbers: str | None = None):
        self.description = description
        self.figure_numbers = figure_numbers
        self.fig_num_pattern = (
            r"图([0-9]+\(?[0-9a-zA-Z']*\)?([和至或,、，-][0-9]+\(?[0-9a-zA-Z']*\)?)*)"
        )

    def count_paragraphs(self):
        pattern = re.compile(r"^\[[0-9]{4}\]", flags=re.MULTILINE)
        para_nums = pattern.findall(self.description)
        last_para_num = int(para_nums[-1][1:-1])
        assert last_para_num == len(para_nums)
        return last_para_num

    def search_figure_numbers(self):
        search_mod = SearchModel(self.description, self.fig_num_pattern)
        for fig_match, start, end in search_mod.search():
            if self._contains_multinumbers(fig_match):
                pass
            
    @staticmethod        
    def _contains_multinumbers(match: re.Match[str]) -> bool:
        if match.groups != () and match.groups()[-1] is not None:
            return True
        return False
            