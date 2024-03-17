import difflib
import re
from collections import defaultdict

from typing import Iterator, NamedTuple, TypeAlias


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
    def __init__(self, content: str, pattern: str, *kwargs: re.RegexFlag):
        self._content = content
        self._pattern = re.compile(pattern, *kwargs)

    def search(self) -> Iterator[SearchResult]:
        match = self._pattern.search(self._content, 0)
        while match is not None:
            start, end = match.span()
            yield SearchResult(match=match, start=start, end=end)
            match = self._pattern.search(self._content, end)


# Model that represents a description of a patent
SearchResults: TypeAlias = defaultdict[str, list[tuple[int, int]]]
FigureNumbers: TypeAlias = tuple[SearchResults, SearchResults]


class DescriptionModel:
    def __init__(
        self,
        description: str,
        sensitive_words: list[str],
        figure_numbers: str | None = None,
    ):
        self.description = description
        self.figure_numbers = "" if figure_numbers is None else figure_numbers
        self.sensitive_words = sensitive_words

        self.fig_num_pattern = r"图([0-9]+[a-zA-Z']*\(?[0-9a-zA-Z']*\)?([和至或到,、，-][0-9]+[a-zA-Z']*\(?[0-9a-zA-Z']*\)?)*)"

    def count_paragraphs(self):
        pattern = re.compile(r"^\[[0-9]{4}\]", flags=re.MULTILINE)
        para_nums = pattern.findall(self.description)
        last_para_num = int(para_nums[-1][1:-1])
        assert last_para_num == len(para_nums)
        return last_para_num

    def search_figure_numbers(self) -> FigureNumbers:
        # Find figure numbers in the description
        desc_search_mod = SearchModel(self.description, self.fig_num_pattern)
        fig_nums_in_desc = defaultdict(list)

        seps_pattern = "[和至或到,、，]"
        # 如果附图中不包含诸如“图1-3”这样的图号，那么说明书中查找到的复合图号，例如图4-5则分成多个子图
        if re.search(r"图[0-9a-zA-Z'()]+-[0-9a-zA-Z'()]+", self.figure_numbers) is None:
            seps_pattern = seps_pattern[:-1] + "-]"

        for fig_match, start, end in desc_search_mod.search():
            if self._contains_multinumbers(fig_match):
                for sub_fig in re.split(seps_pattern, fig_match.group(1)):
                    fig_nums_in_desc["图" + sub_fig].append((start, end))
                continue
            fig_nums_in_desc[fig_match.group(0)].append((start, end))

        # Find figure numbers in figure number text
        figure_numbers_model = SearchModel(self.figure_numbers, self.fig_num_pattern)
        figure_numbers = defaultdict(list)
        for fig_match, start, end in figure_numbers_model.search():
            figure_numbers[fig_match.group(0)].append((start, end))

        return fig_nums_in_desc, figure_numbers

    def search_sensitive_words(self) -> SearchResults:
        search_mod = SearchModel(self.description, "|".join(self.sensitive_words))
        sensitive_words = defaultdict(list)

        for word_match, start, end in search_mod.search():
            sensitive_words[word_match.group(0)].append((start, end))

        return sensitive_words

    @staticmethod
    def _contains_multinumbers(match: re.Match[str]) -> bool:
        if match.groups() != () and match.groups()[-1] is not None:
            return True
        return False


class SettingModel:
    def __init__(self):
        self.sensitive_words: list[str] = ["编撰", "王总"]