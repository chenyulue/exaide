import difflib
import re

from ._type import CmpResult

class TextCompareModel(difflib.SequenceMatcher):
    def __init__(
        self,
        text_original: str,
        text_modified: str,
    ) -> None:
        super().__init__(a=text_original, b=text_modified)
        self._text_original = text_original
        self._text_modified = text_modified

    def reset_comparing_text(self, text_original:str, text_modified:str) -> None:
        self.set_seqs(
            a=text_original,
            b=text_modified,
        )
        self._text_original = text_original
        self._text_modified = text_modified

    def compare(self) -> CmpResult:
        cmp_result = self.get_opcodes()
        return cmp_result

    def get_similarity_ratio(self) -> float:
        return self.ratio()


class SearchModel:
    def __init__(
        self,
        content: Sequence[str],
        pattern: Sequence[str],
    ):
        self._content = content
        self._pattern = pattern

    def search(self):
        result = list()
        pattern = re.compile(self._pattern)

        match = pattern.search(self._content, 0)
        while match is not None:
            start, end = match.span()
            result.append((self._content[start:end], start, end))
            match = pattern.search(self._content, end)

        return result

class SearchFigureNumber(SearchModel):
    def __init__(self, content: Sequence[str]):
        pattern = "图[0-9]+"
        super(self).__init__(content, pattern)

class SearchSensitiveWords(SearchModel):
    def __init__(self, content: Sequence[str], words: set[str]):
        pattern = '|'.join(words)
        super(self).__init__(content, pattern)