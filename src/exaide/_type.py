from typing import TypeAlias
    
AIndex: TypeAlias = int
BIndex: TypeAlias = int
Tag: TypeAlias = str

CompareResults: TypeAlias = list[tuple[Tag, AIndex, AIndex, BIndex, BIndex]]