from typing import Literal, TypeAlias

Tag: TypeAlias = Literal["replace", "delete", "insert", "equal"]
AIndexStart: TypeAlias = int
AIndexEnd: TypeAlias = int
BIndexStart: TypeAlias = int
BIndexEnd: TypeAlias = int

CmpResult: TypeAlias = list[tuple[Tag, AIndexStart, BIndexStart, BIndexEnd]]