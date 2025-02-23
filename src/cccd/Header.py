from .DataDescription import DataDescription
from .format import f_description, f_entry
from typing import List, Callable, Dict, Any


# TODO: Generate a header as in DataSet class
# TODO: Write a function to write header to file
# TODO: Document it and test it
# TODO: An option to have scalar data in the dataset


def default_data_descriptor(name: str, desc: str) -> DataDescription:
    return DataDescription(name, desc)


class Header(DataDescription):
    def __init__(
        self,
        name: str,
        description: str,
        desc_formatter: Callable[[str], str] = f_description,
        entry_formatter: Callable[[str, str], str] = f_entry,
        data_descriptor: Callable[
            [str, str], DataDescription
        ] = default_data_descriptor,
    ):
        DataDescription.__init__(
            self, name, description, desc_formatter, entry_formatter
        )

        self.data_descriptor_ = data_descriptor
        self.data_descriptions_: List[DataDescription] = []

    def generate_header(
        self,
        header_entry_opts: Dict[str, Any] = {},
        header_desc_opts: Dict[str, Any] = {},
        entry_opts: Dict[str, Any] = {},
        desc_opts: Dict[str, Any] = {},
    ) -> str:

        data_entries_text = "".join(
            [x.to_text(entry_opts, desc_opts) for x in self.data_descriptions_]
        )

        if "append_text" in entry_opts:
            header_entry_opts["append_text"] += data_entries_text
        else:
            header_entry_opts["append_text"] = data_entries_text

        return super().to_text(header_entry_opts, header_desc_opts)

    def append(self, name: str, desc: str):
        d = self.data_descriptor_(name, desc)
        self.data_descriptions_.append(d)
