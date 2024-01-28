import difflib
from pathlib import Path
from typing import Sequence


class TextCompareModel:
    def __init__(
        self, text_original: Sequence[str], text_modified: Sequence[str]
    ) -> None:
        self._text_original = text_original
        self._text_modified = text_modified
        self._compare_model = difflib.SequenceMatcher(
            a=self._text_original,
            b=self._text_modified,
        )

    def reset_comparing_text(self, text_original, text_modified):
        self._compare_model.set_seqs(
            a=text_original,
            b=text_modified,
        )

    def compare(self) -> list[tuple[str, int, int, int, int]]:
        cmp_result = self._compare_model.get_opcodes()
        return cmp_result

    def get_similarity_ratio(self) -> float:
        return self._compare_model.ratio()

    def get_text_from_file(self, filepath: Path):
        with open(filepath, "r", encoding="utf-8") as fh:
            text = fh.read()

        return text
