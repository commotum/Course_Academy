#!/usr/bin/env python3
"""Normalize a dated lecture folder's PRE, LEC, and composed root notes.

Every emitted Markdown file begins with exactly one empty line.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path


FOLDER_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-(M\d+-\d+)$")
QUESTION_RE = re.compile(r"^\*\*(Question\s+[^*]+)\*\*$")
QUIZ_OPEN = "```quiz"
QUIZ_CLOSE = "```"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folders", nargs="+", type=Path, help="Dated lecture folders.")
    parser.add_argument("--write", action="store_true", help="Write changes instead of printing diffs.")
    return parser.parse_args()


def strip_repeating_h1(lines: list[str], stem: str) -> list[str]:
    while lines and not lines[0].strip():
        lines = lines[1:]
    if lines and lines[0].strip() == f"# {stem}":
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    return lines


def insert_question_label(block: list[str], label: str) -> list[str]:
    if any(re.match(r"^\s+\*\*Question\s+", line) for line in block):
        return block
    for index, line in enumerate(block):
        if re.match(r"^content\s*:\s*[|>]-?\s*$", line):
            return block[: index + 1] + [f"  **{label}**", ""] + block[index + 1 :]
    raise ValueError(f"quiz block for {label} has no top-level content block scalar")


def normalize_source(text: str, stem: str) -> str:
    lines = strip_repeating_h1(text.splitlines(), stem)
    output: list[str] = []
    index = 0
    while index < len(lines):
        match = QUESTION_RE.match(lines[index].strip())
        if not match:
            output.append(lines[index])
            index += 1
            continue

        lookahead = index + 1
        while lookahead < len(lines) and not lines[lookahead].strip():
            lookahead += 1
        if lookahead >= len(lines) or lines[lookahead].strip() != QUIZ_OPEN:
            output.append(lines[index])
            index += 1
            continue

        end = lookahead + 1
        while end < len(lines) and lines[end].strip() != QUIZ_CLOSE:
            end += 1
        if end >= len(lines):
            raise ValueError(f"unclosed quiz block after {match.group(1)}")

        block = lines[lookahead : end + 1]
        output.extend(insert_question_label(block, match.group(1)))
        index = end + 1

    while output and not output[0].strip():
        output.pop(0)
    while output and not output[-1].strip():
        output.pop()
    return "\n" + "\n".join(output) + ("\n" if output else "")


def quiz_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip() == QUIZ_OPEN)


def composed_root(code: str, pre_text: str | None, lec_text: str | None) -> str:
    sections: list[str] = []
    if pre_text and quiz_count(pre_text):
        sections.extend(["## Pre-Lecture Quiz", "", f"![[Source/{code}-PRE]]"])
    if lec_text and quiz_count(lec_text):
        if sections:
            sections.append("")
        sections.extend(["## Lecture Quiz", "", f"![[Source/{code}-LEC]]"])
    return "\n" + "\n".join(sections) + ("\n" if sections else "")


def render_diff(path: Path, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=str(path),
            tofile=str(path),
        )
    )


def process_folder(folder: Path, write: bool) -> tuple[int, int]:
    folder = folder.expanduser().resolve()
    match = FOLDER_RE.match(folder.name)
    if not folder.is_dir() or not match:
        raise ValueError(f"not a dated lecture folder: {folder}")
    code = match.group(1)
    source_dir = folder / "Source"
    root_path = folder / f"{folder.name}.md"
    source_paths = {
        "pre": source_dir / f"{code}-PRE.md",
        "lec": source_dir / f"{code}-LEC.md",
    }

    changes: list[tuple[Path, str, str]] = []
    normalized: dict[str, str | None] = {"pre": None, "lec": None}
    before_counts: dict[str, int] = {}
    for kind, path in source_paths.items():
        if not path.exists():
            continue
        before = path.read_text(encoding="utf-8")
        before_counts[kind] = quiz_count(before)
        after = normalize_source(before, path.stem)
        if quiz_count(after) != before_counts[kind]:
            raise ValueError(f"quiz count changed unexpectedly in {path}")
        normalized[kind] = after
        if after != before:
            changes.append((path, before, after))

    root_before = root_path.read_text(encoding="utf-8") if root_path.exists() else ""
    root_after = composed_root(code, normalized["pre"], normalized["lec"])
    if root_after != root_before:
        changes.append((root_path, root_before, root_after))

    if write:
        for path, _, after in changes:
            path.write_text(after, encoding="utf-8")
    else:
        for path, before, after in changes:
            print(render_diff(path, before, after), end="")

    return len(changes), sum(before_counts.values())


def main() -> int:
    args = parse_args()
    total_changes = 0
    total_quizzes = 0
    try:
        for folder in args.folders:
            changes, quizzes = process_folder(folder, args.write)
            total_changes += changes
            total_quizzes += quizzes
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    action = "updated" if args.write else "would update"
    print(f"{action} {total_changes} file(s); preserved {total_quizzes} quiz block(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
