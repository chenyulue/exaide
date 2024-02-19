from typing import TypeAlias, Iterator
    
AIndex: TypeAlias = int
BIndex: TypeAlias = int
Tag: TypeAlias = str

CompareResults: TypeAlias = list[tuple[Tag, AIndex, AIndex, BIndex, BIndex]]

SearchResults: TypeAlias = Iterator[tuple[str, int, int]]