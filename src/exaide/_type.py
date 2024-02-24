from typing import TypeAlias, Iterator, NamedTuple
    
AIndex: TypeAlias = int
BIndex: TypeAlias = int
Tag: TypeAlias = str

CompareResults: TypeAlias = list[tuple[Tag, AIndex, AIndex, BIndex, BIndex]]

class SearchResult(NamedTuple):
    match: str
    start: int
    end: int