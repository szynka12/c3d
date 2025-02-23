import cccd as cdf

# TODO: The comment string part

if __name__ == "__main__":

    d = cdf.DataDescription(
        "Field",
        r"       The description of one field of a larger dataset. This"
        r" description"
        " can be quite long and it should be formatted according ot what is"
        " specified in the formatter.",
    )

    print(d.format())

    # Formatter of a description privides several options as of now. The
    # options are passed as a dictionary and later unpacked into the formatting
    # function (by default `f_description`)

    # 1. Specify the width of the wrapped comment
    print(d.format({"width": 40}))

    # 2. Change the comment text to something else
    print(d.format({"comment_text": "--"}))
    print(d.format({"comment_text": "#"}))

    # 3. You can turn off dedentation and wrapping
    print(d.format({"dedent": False, "wrap": False}))
