from typing import TypeAlias, NamedTuple
from enum import Enum, auto


class Tag(Enum):
    RESERVED = auto()
    CALCULATED = auto()
    STR = auto()


AtomJSONType: TypeAlias = int | float | str | bool | None


JSONType: TypeAlias = (
    list["JSONType"] |
    dict[str, "JSONType"] |
    AtomJSONType
)


class Token(NamedTuple):
    value: AtomJSONType
    tag: Tag


class Result(NamedTuple):
    value: JSONType
    position: int
