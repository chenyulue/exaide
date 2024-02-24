import difflib
import re

from ._type import CompareResults, Iterator, SearchResult


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

    def compare(self) -> CompareResults:
        cmp_results = self.get_opcodes()
        return cmp_results

    def get_similarity_ratio(self) -> float:
        return self.ratio()


# text search model
class SearchModel:
    def __init__(
        self,
        content: str,
        pattern: str,
    ):
        self._content = content
        self._pattern = pattern

    def search(self) -> Iterator[SearchResult]:
        pattern = re.compile(self._pattern)

        match = pattern.search(self._content, 0)
        while match is not None:
            start, end = match.span()
            yield SearchResult(match=self._content[start:end], start=start, end=end)
            match = pattern.search(self._content, end)


class SearchFigureNumber(SearchModel):
    def __init__(self, content: str):
        pattern = "图[0-9]+"
        super().__init__(content, pattern)


class SearchSensitiveWords(SearchModel):
    def __init__(self, content: str, words: set[str]):
        pattern = "|".join(words)
        super().__init__(content, pattern)
