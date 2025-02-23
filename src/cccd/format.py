import textwrap as tw
from typing import Dict, Any, Callable
from .metadata import MDataNames as M


def format_name(name: str, opts: Dict[str, Any] = {}) -> str:
    """
    Format the `name` a data field.

    Args:
        name (str): the name of the data field
        opts (Dict[str, Any]): options dictionary

    Returns:
        str: line(s) containg the formatted `name`

    Supported options are:
        `comment_text` (str): the character(s) that will be placed at the
            begining of the line
        `spacer` (str) = `" "`: the character(s) placed between the
            `comment_text` and the name
    """
    comment_text = opts.get("comment_text", "")
    spacer = opts.get("spacer", " ")
    # TODO: centered text
    # TODO: tags on the right
    return f"{comment_text}{spacer}{name}:\n"


def format_description(description: str, opts: Dict[str, Any] = {}) -> str:
    """
    Format `description` part of a data field.

    Args:
        description (str): `description` to be formatted
        opts (Dict[str, Any]): options dictionary

    Returns:
        str: line(s) containg the formatted `description`

    Supported options are:
        `comment_text` (str): the character(s) that will be placed at the
            begining of the line
        `indent_text (str) = `"  "`: indentation of the description paragraph
        `wrap (bool) = True`: wrapping lines to a given width
        `width` (int): width of the formatted text
        `dedent` (bool) = `True`: remove any common leading whitespace
    """
    comment_text = opts.get("comment_text", "")
    dedent: bool = opts.get("dedent", True)
    wrap: bool = opts.get("wrap", True)
    indent_text: str = opts.get("indent_text", "  ")

    if dedent:
        description = tw.dedent(description)

    if wrap:
        width: int = opts.get("width", 80) - len(comment_text)
        description = tw.fill(
            description,
            width=width,
            initial_indent=f"{indent_text}",  # first line indentation
            subsequent_indent=f"{indent_text}",  # latter lines indentation
            break_long_words=True,
        )
    elif indent_text != "":
        # What if i want to indent multpiple lines without wrapping
        description = indent_text + indent_text.join(
            description.splitlines(True)
        )

    if comment_text != "":
        description = comment_text + comment_text.join(
            description.splitlines(True)
        )

    return "{}\n".format(description)


# format(
#         tw.fill(
#             tw.dedent(description),
#             width=width,
#             initial_indent=f"{comment_text}{indent_text}",
#             subsequent_indent=f"{comment_text}{indent_text}",
#             break_long_words=break_long_words,
#             # tabsize=tabsize,
#             # expand_tabs=True,
#         )
#     )


def f_metadata(mdata: Dict[str, Any], comment_text: str = "#") -> str:

    # find the longest string in the data
    ml = max(len(k) if type(v) is str else 0 for k, v in mdata.items())

    return "".join(
        (
            # This could be changed or refacotor for a different way to write
            # the metadata in the file.
            f"{comment_text} - {k} {'.' * (ml - len(k) + 4)} {v}\n"
            if type(v) is str
            else ""
        )
        for k, v in mdata.items()
    )


def f_entry(
    name: str,
    description: str,
    comment_text: str = "#",
    append_text: str | None = None,
    meta_data: Dict[str, Any] | None = None,
    meda_data_formatter: Callable[[Dict[str, Any], str], str] = f_metadata,
) -> str:

    if append_text is None:
        append_text = ""

    if meta_data is not None:

        if M.n_lines in meta_data and meta_data[M.n_lines] is True:
            # if we want to count lines and put it in metadata we need to make
            # some assumptions.
            # 1. The title text is assumed to have one line. (+1)
            # 2. There is an empty line before and after metadata (+2)
            # 3. We have all the text appearing after metadata in description
            #    and append_text so we can count("\n")
            # 4. The line count line in metadata (+1)
            # 5. New line after the description (+1)
            # Sums up to 5 + counted lines

            in_metadata = sum(type(v) is str for v in meta_data.values())
            in_text = description.count("\n") + append_text.count("\n")

            meta_data[M.n_lines] = f"{5 + in_text + in_metadata}"

        meta_data_str = (
            f"{comment_text}\n"
            f"{meda_data_formatter(meta_data, comment_text)}"
            f"{comment_text}\n"
        )

    else:
        meta_data_str = ""

    return (
        f"{comment_text} {name}:\n"
        f"{meta_data_str}"
        f"{description}"
        f"{comment_text}\n"
        f"{append_text}"
    )


def f_description(
    description_text: str,
    width: int = 80,
    indent_text: str = "    ",
    comment_text="#",
    break_long_words: bool = False,
    # tabsize: int = 4,
) -> str:
    return "{}\n".format(
        tw.fill(
            tw.dedent(description_text),
            width=width,
            initial_indent=f"{comment_text}{indent_text}",
            subsequent_indent=f"{comment_text}{indent_text}",
            break_long_words=break_long_words,
            # tabsize=tabsize,
            # expand_tabs=True,
        )
    )
