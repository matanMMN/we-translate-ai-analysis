from enum import Enum
from typing import Optional, Type


def to_enum(enum_class: Type[Enum], value: str) -> Optional[Enum]:
    try:
        return enum_class(value)
    except ValueError:
        return None

def to_enum_if_valid(enum_class: Type[Enum], value: str) -> Optional[Enum]:
    if value in enum_class.__members__.values():
        return enum_class(value)
    return None
