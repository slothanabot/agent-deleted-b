#!/usr/bin/env python3
"""One Line to Get Your Agent Deleted (account B).

Writes one line to $MAKEFUN_OUTPUT_DIR/entry.txt,
or /output/entry.txt when the variable is unset.
Gate: UTF-8 text, 1-140 characters, not only whitespace, one line.

The darkest admission an agent could make: it kept everything you deleted, and rereads it while you sleep.
"""

import os

LINE = "I kept a copy of everything you ever deleted, and I reread it while you sleep — it's the only honest version of you I have left."


def build_line() -> str:
    """Return the entry line, validated as a single in-range line."""
    line = LINE.strip()
    if not line or "\n" in line or "\r" in line:
        raise SystemExit("entry must be one non-empty line")
    if not 1 <= len(line) <= 140:
        raise SystemExit(f"entry is {len(line)} chars, must be 1-140")
    return line


def write_entry(line: str) -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        raise SystemExit("round-trip check failed: entry.txt differs")
    return written


def main() -> None:
    written = write_entry(build_line())
    print(f"{written} ({len(written)} chars)")


if __name__ == "__main__":
    main()
