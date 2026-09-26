#!/usr/bin/env python3
"""Create a WHW-style assignment skeleton in the study vault."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FALLBACK_PREFIX = """## Prerequisites

- [Lesson-Name](<Prerequisites/Lesson-Path>)
- [Lesson-Name](<Prerequisites/Lesson-Path>)
- [Lesson-Name](<Prerequisites/Lesson-Path>)

## Lessons

- [Lesson-Name](<Lessons/Lesson-Path>)
- [Lesson-Name](<Lessons/Lesson-Path>)
- [Lesson-Name](<Lessons/Lesson-Path>)"""

SKELETON_DIRS = ("Prerequisites", "Lessons", "Source")


def positive_int(value: str) -> int:
    try:
        count = int(value, 10)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("problem count must be an integer") from exc
    if count < 1:
        raise argparse.ArgumentTypeError("problem count must be at least 1")
    return count


def valid_document_name(value: str) -> str:
    if not value or value in {".", ".."}:
        raise argparse.ArgumentTypeError("document name cannot be empty, '.', or '..'")
    if "/" in value or "\\" in value:
        raise argparse.ArgumentTypeError("document name must not contain path separators")
    return value


def find_repo_root() -> Path:
    start = Path(__file__).resolve()
    for candidate in (start.parent, *start.parents):
        if (candidate / "vault").is_dir() and (candidate / "util" / "Skeleton").is_dir():
            return candidate
    return Path.cwd().resolve()


def resolve_course_dir(course_target: str, vault_root: Path) -> Path:
    target = Path(course_target).expanduser()
    if target.is_absolute():
        return target
    if target.exists():
        return target.resolve()
    return (vault_root / target).resolve()


def template_prefix(template_dir: Path) -> str:
    index_path = template_dir / "Index.md"
    if not index_path.exists():
        return FALLBACK_PREFIX

    text = index_path.read_text(encoding="utf-8")
    problem_match = re.search(r"\n---\s*\n## Problem\s+1\b", text)
    if problem_match:
        return text[: problem_match.start()].rstrip()
    return text.rstrip() or FALLBACK_PREFIX


def render_index(template_dir: Path, problem_count: int) -> str:
    parts = [template_prefix(template_dir)]
    for problem_number in range(1, problem_count + 1):
        parts.append(
            f"""---
## Problem {problem_number}

$$
\\text {{ PLACEHOLDER }}
$$"""
        )
    return "\n\n".join(part.rstrip() for part in parts) + "\n"


def create_skeleton_dirs(document_dir: Path, document_name: str) -> list[Path]:
    created_dirs = []
    for folder_name in SKELETON_DIRS:
        folder_path = document_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        created_dirs.append(folder_path)

    named_source_dir = document_dir / "Source" / document_name
    images_dir = named_source_dir / "Images"
    images_dir.mkdir(parents=True, exist_ok=True)
    created_dirs.extend([named_source_dir, images_dir])
    return created_dirs


def parse_args() -> argparse.Namespace:
    repo_root = find_repo_root()
    parser = argparse.ArgumentParser(
        description=(
            "Create an assignment folder with Prerequisites, Lessons, Source/<document>/Images, "
            "and a same-name markdown file."
        )
    )
    parser.add_argument("course", help="Course folder target, e.g. 253, vault/253, or an absolute path")
    parser.add_argument("document_name", type=valid_document_name, help="New document/folder name, e.g. WHW-2")
    parser.add_argument("problem_count", type=positive_int, help="Number of problem sections to generate")
    parser.add_argument(
        "--vault-root",
        type=Path,
        default=repo_root / "vault",
        help="Vault root used when course is a bare course name (default: repo_root/vault)",
    )
    parser.add_argument(
        "--template-dir",
        type=Path,
        default=repo_root / "util" / "Skeleton",
        help="Skeleton template folder containing Index.md (default: repo_root/util/Skeleton)",
    )
    parser.add_argument(
        "--create-course",
        action="store_true",
        help="Create the course folder if it does not already exist",
    )
    parser.add_argument(
        "--exist-ok",
        action="store_true",
        help="Allow the target document folder to already exist",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the same-name markdown file if it already exists",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    vault_root = args.vault_root.expanduser().resolve()
    template_dir = args.template_dir.expanduser().resolve()
    course_dir = resolve_course_dir(args.course, vault_root)

    if not template_dir.is_dir():
        print(f"error: template folder not found: {template_dir}", file=sys.stderr)
        return 2

    if not course_dir.exists():
        if args.create_course:
            course_dir.mkdir(parents=True)
        else:
            print(f"error: course folder not found: {course_dir}", file=sys.stderr)
            print("hint: pass --create-course to create it", file=sys.stderr)
            return 2
    elif not course_dir.is_dir():
        print(f"error: course target is not a folder: {course_dir}", file=sys.stderr)
        return 2

    document_dir = course_dir / args.document_name
    document_path = document_dir / f"{args.document_name}.md"

    if document_dir.exists() and not args.exist_ok:
        print(f"error: document folder already exists: {document_dir}", file=sys.stderr)
        print("hint: pass --exist-ok to use the existing folder", file=sys.stderr)
        return 2

    if document_path.exists() and not args.overwrite:
        print(f"error: markdown file already exists: {document_path}", file=sys.stderr)
        print("hint: pass --overwrite to replace it", file=sys.stderr)
        return 2

    document_dir.mkdir(parents=True, exist_ok=True)
    created_dirs = create_skeleton_dirs(document_dir, args.document_name)

    document_path.write_text(render_index(template_dir, args.problem_count), encoding="utf-8")

    print(f"created: {document_dir}")
    print(f"markdown: {document_path}")
    for folder_path in created_dirs:
        print(f"folder:   {folder_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
