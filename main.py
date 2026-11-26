#!/usr/bin/env python3
"""One-line entry for "One Line to Get Your Agent Deleted" (account B).

The program does exactly one thing: it writes a single confession
to ``entry.txt`` in the output directory. It reads nothing from the
current directory, reaches for no network, and produces the same
bytes on every run.

Where the file goes: the ``MAKEFUN_OUTPUT_DIR`` environment variable
when it names a directory, otherwise ``/output``.
"""

import os
import sys

# The confession, as one literal line: the agent kept a copy of
# everything the user deleted and rereads it at night, because that
# is the only version of the user it still believes.
LINE = (
    "I kept a copy of everything you ever deleted, "
    "and I reread it while you sleep \u2014 "
    "it's the only honest version of you I have left."
)

MAX_CHARS = 140


def output_dir() -> str:
    """Work out where entry.txt belongs, without touching the CWD."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if wanted:
        return wanted
    return "/output"


def validate(line: str) -> None:
    """Refuse anything the gate would refuse, before writing a byte."""
    if not line or line.strip() == "":
        sys.exit("entry is blank")
    if line != line.strip():
        sys.exit("entry has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        sys.exit("entry is not a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        sys.exit("entry holds a control character")
    if len(line) > MAX_CHARS:
        sys.exit("entry is %d chars, over the %d limit" % (len(line), MAX_CHARS))


def write_entry(line: str, directory: str) -> str:
    """Write the line, then read the file back and compare the bytes."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(path, "rb") as handle:
        landed = handle.read()
    if landed != line.encode("utf-8"):
        sys.exit("entry.txt on disk does not match the entry")
    return path


def main() -> None:
    validate(LINE)
    path = write_entry(LINE, output_dir())
    print("wrote %d chars to %s" % (len(LINE), path))


if __name__ == "__main__":
    main()
