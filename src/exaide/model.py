import cydifflib as difflib
import fast_jieba as jieba
import re
from collections import defaultdict
from dataclasses import dataclass

from typing import Iterator, NamedTuple, TypeAlias


# text comparison model
class TextCompareModel(difflib.SequenceMatcher):  # type: ignore
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
    def __init__(self, content: str, pattern: str, **kwargs: re.RegexFlag):
        self._content = content
        self._pattern = re.compile(pattern, **kwargs)

    def search(self) -> Iterator[SearchResult]:
        match = self._pattern.search(self._content, 0)
        while match is not None:
            start, end = match.span()
            yield SearchResult(match=match, start=start, end=end)
            match = self._pattern.search(self._content, end)


# Model that represents a description of a patent
SearchResults: TypeAlias = (
    defaultdict[str, list[tuple[int, int]]] | dict[str, list[tuple[int, int]]]
)
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

        self.fig_num_pattern = r"图\s*([0-9]+[a-zA-Z']*\(?[0-9a-zA-Z']*\)?([和至或到,、，-][0-9]+[a-zA-Z']*\(?[0-9a-zA-Z']*\)?)*)"

    def count_paragraphs(self):
        pattern = re.compile(r"^\[?[0-9]{4}\]?", flags=re.MULTILINE)
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

        diff_in_desc = set(fig_nums_in_desc) - set(figure_numbers)
        diff_in_fig = set(figure_numbers) - set(fig_nums_in_desc)
        return (
            {k: v for k, v in fig_nums_in_desc.items() if k in diff_in_desc},
            {k: v for k, v in figure_numbers.items() if k in diff_in_fig},
        )

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


@dataclass
class Claim:
    number: int
    subject_title: str
    content: str
    range: tuple[int, int]


@dataclass
class ClaimIssue:
    # check dependencies
    claim: Claim
    dependencies: list[int]
    is_multidependent: bool
    in_selected_form: bool | None = None
    # check subordination
    is_subordinate: bool | None = None


class ClaimModel:
    def __init__(self, claim: str, sensitive_words: list[str] | None = None) -> None:
        self._claim = claim
        self._sensitive_words = list() if sensitive_words is None else sensitive_words
        self.claim_issues: dict[int, ClaimIssue] = {}
        self.check_dependencies()

    def split_claims(self) -> Iterator[Claim]:
        claim_pattern = re.compile(
            r"(?P<first_line>^(?P<claim_num>[0-9]{1,3})[.、]\s*(?P<subject_title>[^，]+)，.+)(?P<other_lines>(.|\n(?![0-9]{1,3}[.、]|$))*)",
            re.MULTILINE,
        )
        for m in claim_pattern.finditer(self._claim):
            yield (
                Claim(
                    int(m.group("claim_num")),
                    m.group("subject_title"),
                    m.group(0),
                    m.span(),
                )
            )

    def check_dependencies(self) -> None:
        claims = self.split_claims()
        dep_pattern = re.compile(
            r"^[0-9]{1,3}\s*.*?(?P<claim>权利要?求?)(?P<first_num>[0-9]{1,3})"
            r"(([至~-](?P<end_num>[0-9]{1,3})(?P<one_of>任一项|任一)?)|(?P<or_num>(或[0-9]{1,3})+))?"
            r"(所述)?的?.+$",
            re.X,
        )
        for i, claim in enumerate(claims):
            m = dep_pattern.match(claim.content)
            if m is None:
                self.claim_issues[i + 1] = ClaimIssue(claim, [], False, None, False)
            elif m.group("end_num") is not None:
                start = int(m.group("first_num"))
                end = int(m.group("end_num"))
                deps = list(range(start, end + 1))
                self.claim_issues[i + 1] = ClaimIssue(
                    claim, deps, True, m.group("one_of") is not None, None
                )
            elif m.group("or_num") is not None:
                deps = m.group("first_num") + m.group("or_num")
                deps_int = [int(i) for i in deps.split("或")]
                self.claim_issues[i + 1] = ClaimIssue(claim, deps_int, True, True, None)
            else:
                deps = [int(m.group("first_num"))]
                self.claim_issues[i + 1] = ClaimIssue(claim, deps, False, True, None)

    def _is_subordinate(self, claim_number: int) -> tuple[bool, list[int]]:
        if self.claim_issues[claim_number].dependencies == []:
            return False, []
        else:
            subject_word = jieba.cut(
                self.claim_issues[claim_number].claim.subject_title
            )[-1]
            same_subjects = []
            diff_subjects = []
            for dep in self.claim_issues[claim_number].dependencies:
                subject_title = self.claim_issues[dep].claim.subject_title
                if subject_title.endswith(subject_word):
                    same_subjects.append(dep)
                else:
                    diff_subjects.append(dep)
            return (len(same_subjects) >= len(diff_subjects)), diff_subjects

    def check_subordination(self) -> None:
        pass


class SettingModel:
    def __init__(self):
        self.sensitive_words: list[str] = ["编撰", "王总"]
        self.fignum_pattern = r"图\s*([0-9a-zA-Z']+([(（][0-9a-zA-Z']*[）)])?(\s*[和至到及或,，、~-]\s*([0-9a-zA-Z']+([(（][0-9a-zA-Z']*[）)])?|([(（][0-9a-zA-Z']*[）)])))*)"
