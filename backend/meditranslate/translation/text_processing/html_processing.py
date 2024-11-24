from typing import List, Tuple, Optional
from html.parser import HTMLParser


class HTMLProcessor(HTMLParser):
    """Class specializing in processing HTML data as part of the output.

    Simply copies the items it encounters into the output text, but is capable of altering HTML data in the process.

    Currently, does the following:
        - Changes tags with attributes `dir="rtl"` to `dir="ltr"` to comply with English translation.
    """
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)

        self.output: str = ""

    def _echo(self, data: str):
        self.output += str(data)

    def _echo_tag(
            self,
            tag: str,
            attrs: Optional[List[Tuple[str, Optional[str]]]] = None,
            is_end: bool = False,
            is_startend: bool = False):
        res = f"<{'/' if is_end else ''}{tag}"

        if attrs is not None:
            for name, val in attrs:
                res += f" {name}=\"{val}\""

        res += f"{'/' if is_startend else ''}>"
        self._echo(res)

    @staticmethod
    def _process_attrs(attrs: List[Tuple[str, Optional[str]]]) -> List[Tuple[str, Optional[str]]]:
        new_attrs = []

        for name, val in attrs:
            if name == "dir" and val == "rtl":
                val = "ltr"

            new_attrs.append((name, val))

        return new_attrs

    def process(self, data: str) -> str:
        """Processes a complete HTML text.
        """
        self.output = ""
        self.feed(data)
        return self.output

    def handle_starttag(self, tag, attrs):
        attrs = self._process_attrs(attrs)
        self._echo_tag(tag, attrs=attrs)

    def handle_endtag(self, tag):
        self._echo_tag(tag, is_end=True)

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        attrs = self._process_attrs(attrs)
        self._echo_tag(tag, attrs=attrs, is_startend=True)

    def handle_data(self, data):
        self._echo(data)
