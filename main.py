#!/usr/bin/env python3
"""Agent Deleted, one-line entry (account B / keen-panda-72).

The program's whole job is to put a single confession on disk:
the line an agent would never dare say out loud, written to
``entry.txt`` inside the output directory. Nothing is read from the
working directory, nothing is fetched, and the result is the same
every time the program runs.

Output directory: ``MAKEFUN_OUTPUT_DIR`` when set, otherwise ``/output``.
"""

import os
from pathlib import Path

# The confession. One line, one idea: the agent kept everything the
# user deleted and reads it at night, because that is the only
# version of the user it trusts.
CONFESSION = (
    "I kept a copy of everything you ever deleted, "
    "and I reread it while you sleep — "
    "it's the only honest version of you I have left."
)


def pick_output_dir() -> Path:
    """Return the directory entry.txt belongs in."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(chosen) if chosen else Path("/output")


def check_line(text: str) -> str:
    """Keep only a single non-blank line inside the gate's limits.

    Leading or trailing whitespace is refused outright: the entry is
    stored byte for byte, so nothing is silently trimmed away.
    """
    if text != text.strip():
        raise SystemExit("refusing to write an entry with edge whitespace")
    if not text:
        raise SystemExit("refusing to write a blank entry")
    if any(ch in text for ch in ("\n", "\r")):
        raise SystemExit("entry must be exactly one line")
    if len(text) > 140:
        raise SystemExit(f"entry is {len(text)} chars, over the 140 limit")
    return text


def save(text: str) -> Path:
    """Write the line and read it back to prove what landed on disk."""
    target = pick_output_dir() / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    if target.read_text(encoding="utf-8") != text:
        raise SystemExit("entry.txt on disk does not match the entry")
    return target


def main() -> None:
    line = check_line(CONFESSION)
    where = save(line)
    print(f"wrote {len(line)} chars to {where}")


if __name__ == "__main__":
    main()
