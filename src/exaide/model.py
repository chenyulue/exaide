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

        start = 0
        match = pattern.search(self._content, start)
        while match is not None:
            a, b = match.span()
            result.append((self._content[a:b], a, b))
            start = b

        return result

class SearchFigureNumber(SearchModel):
    def __init__(self, content: Sequence[str]):
        pattern = "图[0-9]+"
        super(self).__init__(content, pattern)

class SearchSensitiveWords(SearchModel):
    def __init__(self, content: Sequence[str], words: set[str]):
        pattern = '|'.join(words)
        super(self).__init__(content, pattern)