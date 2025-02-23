from typing import Callable, Dict, Any
from .format import f_description, f_entry, format_name, format_description


# Lets format the name of the entry
# then lets format the description


class DataDescription:
    def __init__(
        self,
        name: str,
        description: str,
        desc_formatter: Callable[[str], str] = f_description,
        entry_formatter: Callable[[str, str], str] = f_entry,
    ):
        self.name_: str = name
        self.description_: str = description
        self.desc_formatter_: Callable[[str], str] = desc_formatter
        self.entry_formatter_: Callable[[str, str], str] = entry_formatter

    def __str__(self) -> str:
        return self.to_text()

    def format(
        self,
        opts: Dict[str, Any] = {},
        f_name: Callable[[str, Dict[str, Any]], str] = format_name,
        f_description: Callable[
            [str, Dict[str, Any]], str
        ] = format_description,
    ):
        return (
            f"{f_name(self.name_, opts)}"
            f"{f_description(self.description_, opts)}"
        )

    def to_text(
        self, entry_opts: Dict[str, Any] = {}, desc_opts: Dict[str, Any] = {}
    ) -> str:
        return self.entry_formatter_(
            self.name_,
            self.desc_formatter_(self.description_, **desc_opts),
            **entry_opts,
        )

    def column_name(self) -> str:
        return self.name_
