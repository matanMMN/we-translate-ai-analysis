from typing import Union, List,Literal

class Language:
    def __init__(
        self,
        name: str,
        native_name: str,
        direction: Literal["ltr","rtl"] = "ltr",
        charset: str = 'UTF-8',
        linguistic_family: Union[str, None] = None
    ) -> None:

        self.name = name
        self.native_name = native_name
        self.direction = direction
        self.code_2_lower = name[:2].lower()
        self.code_2_upper = name[:2].upper()
        self.code_3_lower = name[:3].lower()
        self.code_3_upper = name[:3].upper()
        self.charset = charset
        self.linguistic_family = linguistic_family


    def __str__(self) -> str:
        return self.name


    def __eq__(self, other: object) -> bool:
        if isinstance(other, Language):
            return (
                self.name == other.name and
                self.native_name == other.native_name and
                self.direction == other.direction and
                self.charset == other.charset and
                self.linguistic_family == other.linguistic_family
            )
        elif isinstance(other, str):
            return (
                other.lower() == self.name.lower() or
                other.lower() == self.native_name.lower() or
                other.lower() == self.code_2_lower or
                other.lower() == self.code_3_lower
            )
        return False

    def __hash__(self) -> int:
        return hash((
            self.name,
            self.native_name,
            self.direction,
            self.charset,
            self.linguistic_family
        ))

