#!/usr/bin/env python3
"""Print problem blocks from a study-vault assignment markdown file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PROBLEM_RE = re.compile(r"^##\s+Problem\s+(\d+)\b.*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List ## Problem N blocks from an assignment markdown file."
    )
    parser.add_argument("markdown_file", type=Path)
    parser.add_argument(
        "--problem",
        type=int,
        help="Print only one problem number.",
    )
    return parser.parse_args()


def find_problem_blocks(lines: list[str]) -> list[tuple[int, int, int]]:
    starts: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        match = PROBLEM_RE.match(line)
        if match:
            starts.append((int(match.group(1)), index))

    blocks: list[tuple[int, int, int]] = []
    for position, (number, start) in enumerate(starts):
        end = starts[position + 1][1] if position + 1 < len(starts) else len(lines)
        blocks.append((number, start, end))
    return blocks


def main() -> int:
    args = parse_args()
    path = args.markdown_file.expanduser()
    if not path.exists():
        print(f"error: markdown file not found: {path}", file=sys.stderr)
        return 2

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    blocks = find_problem_blocks(lines)
    if args.problem is not None:
        blocks = [block for block in blocks if block[0] == args.problem]

    if not blocks:
        target = f"Problem {args.problem}" if args.problem is not None else "problem blocks"
        print(f"error: no {target} found in {path}", file=sys.stderr)
        return 1

    for offset, (number, start, end) in enumerate(blocks):
        if offset:
            print()
        print(f"<!-- Problem {number}: lines {start + 1}-{end} -->")
        print("".join(lines[start:end]).rstrip())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
