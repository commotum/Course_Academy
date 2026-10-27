#!/usr/bin/env python3
"""Render lesson JSON files into DATA/Lessons/[topic-id]/[topic-id].md.

This is a standalone renderer for the lesson-centric layout:

    DATA/Lessons/[topic-id]/
      [topic-id].md
      Source/
        [topic-id].json
        Images/
          ...

It embeds the markdown rendering logic directly in this script so the stage
remains self-contained.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from bs4 import BeautifulSoup, NavigableString, Tag


SCRIPT_PATH = Path(__file__).resolve()


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "DATA").is_dir() and (candidate / "PIPELINE").is_dir():
            return candidate
    raise RuntimeError(f"Could not determine repo root from {start}")


REPO_ROOT = find_repo_root(SCRIPT_PATH)
LIB_ROOT = REPO_ROOT / "PIPELINE" / "0-lib"
if str(LIB_ROOT) not in sys.path:
    sys.path.insert(0, str(LIB_ROOT))

from progress import progress_bar, progress_write

DEFAULT_LESSONS_ROOT = REPO_ROOT / "DATA" / "Lessons"

RELATION_COMMANDS = (
    r"\approx",
    r"\le",
    r"\ge",
    r"\ne",
    "=",
    "<",
    ">",
)
RELATION_PATTERN = "|".join(sorted((re.escape(token) for token in RELATION_COMMANDS), key=len, reverse=True))
SIZED_DELIMITER_PIPE_PATTERN = re.compile(
    r"\\(?:left|right|middle|bigl|bigr|Bigl|Bigr|biggl|biggr|Biggl|Biggr)\s*\|"
)


@dataclass
class Block:
    kind: str
    markdown: str


@dataclass
class MarkdownContext:
    image_resolver: "LessonImageResolver"
    blank_width: str = "1.5cm"
    select_width: str = "2cm"
    standalone_math_display: bool = True


def normalize_ws(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify_heading(text: str) -> str:
    slug = html.unescape(text or "").strip().lower()
    slug = slug.replace("'", "")
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug.strip("-")


def upper_choice_label(label: str) -> str:
    return (label or "").strip().upper() or "?"


def escape_literal_math_dollars(tex: str) -> str:
    """A source formula is bare TeX; its dollar glyphs are not delimiters."""
    # Older source records replaced escaped currency while tokenizing dollars.
    tex = re.sub(r"\\\[/?math\]", lambda _: r"\$", tex)
    result: list[str] = []
    backslashes = 0
    for char in tex:
        if char == "$" and backslashes % 2 == 0:
            result.append("\\")
        result.append(char)
        backslashes = backslashes + 1 if char == "\\" else 0
    return "".join(result)


def wrap_math_inline(tex: str) -> str:
    return f"${escape_literal_math_dollars(ensure_inline_integrals_displaystyle(tex))}$"


def wrap_math_display(tex: str) -> str:
    return "\n".join(["$$", escape_literal_math_dollars(tex), "$$"])


def split_top_level(text: str, delimiter: str = ",") -> list[str]:
    parts: list[str] = []
    depth = 0
    start = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif char == delimiter and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def split_math_top_level(text: str, delimiter: str) -> list[str]:
    parts: list[str] = []
    depth_round = 0
    depth_square = 0
    depth_curly = 0
    start = 0
    index = 0

    while index < len(text):
        char = text[index]

        if char == "\\":
            index += 2
            continue

        if char == "(":
            depth_round += 1
        elif char == ")":
            depth_round = max(0, depth_round - 1)
        elif char == "[":
            depth_square += 1
        elif char == "]":
            depth_square = max(0, depth_square - 1)
        elif char == "{":
            depth_curly += 1
        elif char == "}":
            depth_curly = max(0, depth_curly - 1)
        elif (
            char == delimiter
            and depth_round == 0
            and depth_square == 0
            and depth_curly == 0
        ):
            if delimiter != "|" or not text.startswith("|=", index):
                parts.append(text[start:index].strip())
                start = index + 1

        index += 1

    parts.append(text[start:].strip())
    return parts


def find_matching_delimiter(text: str, start: int, open_char: str, close_char: str) -> int | None:
    depth = 0
    index = start

    while index < len(text):
        char = text[index]

        if char == "\\":
            index += 2
            continue

        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return index

        index += 1

    return None


def parse_matrix_rows(text: str, *, allow_single_column: bool) -> list[list[str]] | None:
    stripped = text.strip()
    if not stripped or ("|" not in stripped and ";" not in stripped):
        return None

    row_texts = split_math_top_level(stripped, ";")
    rows: list[list[str]] = []
    expected_cols: int | None = None

    for row_text in row_texts:
        columns = split_math_top_level(row_text, "|")
        columns = [column.strip() for column in columns]
        if any(column == "" for column in columns):
            return None

        col_count = len(columns)
        if expected_cols is None:
            expected_cols = col_count
        elif col_count != expected_cols:
            return None

        rows.append(columns)

    if not rows or expected_cols is None:
        return None
    if len(rows) == 1 and expected_cols == 1:
        return None
    if expected_cols == 1 and not allow_single_column:
        return None
    return rows


def matrix_rows_to_tex(rows: Sequence[Sequence[str]], env: str) -> str:
    normalized_rows = [
        " & ".join(normalize_math_tex(entry) for entry in row)
        for row in rows
    ]
    body = r" \\ ".join(normalized_rows)
    return rf"\begin{{{env}}}{body}\end{{{env}}}"


def convert_bracket_matrix_notation(text: str) -> str:
    out: list[str] = []
    index = 0

    while index < len(text):
        if text[index] != "[":
            out.append(text[index])
            index += 1
            continue

        end = find_matching_delimiter(text, index, "[", "]")
        if end is None:
            out.append(text[index])
            index += 1
            continue

        inner = text[index + 1 : end]
        rows = parse_matrix_rows(inner, allow_single_column=True)
        if rows is None:
            out.append(text[index : end + 1])
        else:
            out.append(matrix_rows_to_tex(rows, "bmatrix"))
        index = end + 1

    return "".join(out)


def convert_determinant_matrix_notation(text: str) -> str:
    out: list[str] = []
    index = 0

    while index < len(text):
        current = text[index]
        if (
            current != "|"
            or text.startswith("|=", index)
            or text.startswith("||", index)
            or (index > 0 and text[index - 1] == "|")
            or is_sized_delimiter_pipe(text, index)
            or is_evaluation_bar(text, index)
        ):
            out.append(current)
            index += 1
            continue

        replacement: str | None = None
        replacement_end: int | None = None

        for end in range(index + 1, len(text)):
            if text[end] != "|":
                continue
            if (
                text.startswith("|=", end)
                or (end > 0 and text[end - 1] == "|")
                or is_sized_delimiter_pipe(text, end)
                or is_evaluation_bar(text, end)
            ):
                continue

            rows = parse_matrix_rows(text[index + 1 : end], allow_single_column=True)
            if rows is not None:
                replacement = matrix_rows_to_tex(rows, "vmatrix")
                replacement_end = end

        if replacement is None or replacement_end is None:
            out.append(current)
            index += 1
            continue

        out.append(replacement)
        index = replacement_end + 1

    return "".join(out)


def convert_standalone_matrix_notation(text: str) -> str:
    body, punctuation = split_trailing_punctuation(text.strip())
    if ";" not in body:
        return text
    rows = parse_matrix_rows(body, allow_single_column=False)
    if rows is None:
        return text
    return matrix_rows_to_tex(rows, "bmatrix") + punctuation


def convert_custom_matrix_notation(text: str) -> str:
    converted = convert_bracket_matrix_notation(text)
    converted = convert_standalone_matrix_notation(converted)
    return convert_determinant_matrix_notation(converted)


def ensure_inline_integrals_displaystyle(tex: str) -> str:
    def repl(match: re.Match[str]) -> str:
        prefix = tex[: match.start()]
        if re.search(r"\\displaystyle\s*$", prefix):
            return r"\int"
        return r"\displaystyle \int"

    return re.sub(r"\\int(?![A-Za-z])", repl, tex)


SIZED_PIPE_COMMANDS = (
    r"\left",
    r"\right",
    r"\middle",
    r"\bigl",
    r"\bigr",
    r"\Bigl",
    r"\Bigr",
    r"\biggl",
    r"\biggr",
    r"\Biggl",
    r"\Biggr",
)


def is_sized_delimiter_pipe(text: str, index: int) -> bool:
    if index >= len(text) or text[index] != "|":
        return False
    prefix = text[:index].rstrip()
    return any(prefix.endswith(command) for command in SIZED_PIPE_COMMANDS)


def is_evaluation_bar(text: str, index: int) -> bool:
    if index >= len(text) or text[index] != "|":
        return False
    if is_sized_delimiter_pipe(text, index):
        return False
    cursor = index + 1
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    return cursor < len(text) and text[cursor] in {"_", "^"}


def read_math_script(text: str, index: int) -> int | None:
    if index >= len(text) or text[index] not in {"_", "^"}:
        return None

    cursor = index + 1
    if cursor >= len(text):
        return None

    if text[cursor] == "{":
        end = find_matching_delimiter(text, cursor, "{", "}")
        return end + 1 if end is not None else None

    if text[cursor] == "\\":
        match = re.match(r"\\[A-Za-z]+", text[cursor:])
        if match:
            return cursor + len(match.group(0))

    return cursor + 1


def read_evaluation_bar_end(text: str, index: int) -> int | None:
    if not is_evaluation_bar(text, index):
        return None

    cursor = index + 1
    saw_script = False
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1

    while cursor < len(text) and text[cursor] in {"_", "^"}:
        end = read_math_script(text, cursor)
        if end is None:
            return None
        saw_script = True
        cursor = end
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1

    return cursor if saw_script else None


def previous_nonspace_index(text: str, index: int) -> int | None:
    cursor = index
    while cursor >= 0:
        if not text[cursor].isspace():
            return cursor
        cursor -= 1
    return None


def skip_math_space(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def is_binary_minus(text: str, index: int) -> bool:
    prev = previous_nonspace_index(text, index - 1)
    if prev is None:
        return False
    return text[prev] not in "([{=;,+-*/"


def find_evaluation_expression_start(text: str, bar_index: int) -> int:
    depth_round = 0
    depth_square = 0
    depth_curly = 0
    cursor = bar_index - 1

    while cursor >= 0:
        char = text[cursor]

        if char == "}":
            depth_curly += 1
        elif char == "{":
            depth_curly = max(0, depth_curly - 1)
        elif char == "]":
            depth_square += 1
        elif char == "[":
            depth_square = max(0, depth_square - 1)
        elif char == ")":
            depth_round += 1
        elif char == "(":
            depth_round = max(0, depth_round - 1)

        if depth_round == 0 and depth_square == 0 and depth_curly == 0:
            for token in (r"\cdot", r"\times"):
                token_start = cursor - len(token) + 1
                if token_start >= 0 and text.startswith(token, token_start):
                    return skip_math_space(text, cursor + 1)

            if char in {";", "=", "+"}:
                return skip_math_space(text, cursor + 1)
            if char == "-" and is_binary_minus(text, cursor):
                return skip_math_space(text, cursor + 1)

        cursor -= 1

    return skip_math_space(text, 0)


def normalize_evaluation_bar_syntax(text: str) -> str:
    replacements: list[tuple[int, int, int]] = []
    cursor = 0

    while cursor < len(text):
        if text[cursor] != "|":
            cursor += 1
            continue

        end = read_evaluation_bar_end(text, cursor)
        if end is None:
            cursor += 1
            continue

        start = find_evaluation_expression_start(text, cursor)
        replacements.append((start, cursor, end))
        cursor = end

    for start, bar_index, end in reversed(replacements):
        expression = text[start:bar_index]
        scripts = text[bar_index + 1 : end]
        replacement = rf"\left.{expression}\right|{scripts}"
        text = text[:start] + replacement + text[end:]

    return text


def replace_balanced_braced_command(text: str, command_name: str, formatter) -> str:
    needle = "\\" + command_name + "{"
    out: list[str] = []
    cursor = 0

    while True:
        start = text.find(needle, cursor)
        if start == -1:
            out.append(text[cursor:])
            break

        out.append(text[cursor:start])
        brace_start = start + len(needle) - 1
        end = find_matching_delimiter(text, brace_start, "{", "}")
        if end is None:
            out.append(text[start:])
            break

        inner = text[brace_start + 1 : end]
        out.append(formatter(inner))
        cursor = end + 1

    return "".join(out)


def split_eqalign_rows(text: str) -> tuple[list[str], list[str | None]]:
    marker = "@@EQALIGN_ROW@@"
    marked = text.replace("\r\n", "\n").replace("\r", "\n")
    marked = re.sub(r"\\\s*\[([^\]]+)\]", lambda m: f"{marker}[{m.group(1).strip()}]", marked)
    marked = re.sub(r"\\\s+(?=(?:&|\\hline|[^\\\s\[]))", marker, marked)
    marked = re.sub(r"\\\s*$", marker, marked)

    rows: list[str] = []
    separators: list[str | None] = []
    pattern = re.compile(re.escape(marker) + r"(?:\[([^\]]+)\])?")
    cursor = 0

    for match in pattern.finditer(marked):
        rows.append(match.string[cursor:match.start()].strip())
        separators.append(match.group(1).strip() if match.group(1) else None)
        cursor = match.end()

    rows.append(marked[cursor:].strip())

    while rows and not rows[-1]:
        rows.pop()
        if separators:
            separators.pop()

    return rows, separators


def normalize_eqalign_rows(rows: Sequence[str]) -> list[str]:
    normalized_rows: list[str] = []
    pending_prefix = ""

    for raw_row in rows:
        row = re.sub(r"\s+", " ", raw_row).strip()
        if not row:
            continue

        if pending_prefix and not row.startswith("&"):
            row = f"{pending_prefix} {row}".strip()
            pending_prefix = ""

        match = re.match(rf"^(.*?)(?:&\s*({RELATION_PATTERN}))\s*$", row)
        if match:
            row = match.group(1).strip()
            pending_prefix = f"&{match.group(2)}"

        if row:
            normalized_rows.append(row)

    if pending_prefix:
        normalized_rows.append(pending_prefix)

    return normalized_rows


def eqalign_to_tex(inner: str) -> str:
    raw_rows, separators = split_eqalign_rows(inner)
    rows = normalize_eqalign_rows(raw_rows)
    if not rows:
        return r"\begin{aligned}\end{aligned}"

    has_hline = any(r"\hline" in row for row in rows)
    open_env = r"\begin{array}{rl}" if has_hline else r"\begin{aligned}"
    close_env = r"\end{array}" if has_hline else r"\end{aligned}"

    parts: list[str] = []
    for index, row in enumerate(rows):
        parts.append(row)
        if index < len(rows) - 1:
            parts.append(r" \\")
            if index < len(separators) and separators[index]:
                parts.append(f"[{separators[index]}]")
            parts.append("\n")

    return "\n".join([open_env, "".join(parts), close_env])


def normalize_legacy_alignment_syntax(text: str) -> str:
    return replace_balanced_braced_command(text, "eqalign", eqalign_to_tex)


def replace_balanced_calls(text: str, func_name: str, formatter) -> str:
    needle = f"{func_name}("
    out: list[str] = []
    cursor = 0

    while True:
        start = text.find(needle, cursor)
        if start == -1:
            out.append(text[cursor:])
            break

        out.append(text[cursor:start])
        depth = 1
        index = start + len(needle)
        while index < len(text) and depth:
            if text[index] == "(":
                depth += 1
            elif text[index] == ")":
                depth -= 1
            index += 1

        if depth:
            out.append(text[start:])
            break

        inner = text[start + len(needle) : index - 1]
        out.append(formatter(inner))
        cursor = index

    return "".join(out)


def normalize_fraction_syntax(text: str) -> str:
    current = text
    while True:
        updated = re.sub(r"\(([^()]+)\)/\(([^()]+)\)", r"\\frac{\1}{\2}", current)
        updated = re.sub(
            r"\((\\frac\{[^{}]+\}\{[^{}]+\})\)/\((\\frac\{[^{}]+\}\{[^{}]+\})\)",
            r"\\frac{\1}{\2}",
            updated,
        )
        if updated == current:
            return updated
        current = updated


def normalize_conditional_function_syntax(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        prefix = match.group(1)
        left = match.group(2)
        right = match.group(3)
        first_arg = match.group(4).strip()
        second_arg = match.group(5).strip()
        return f"{prefix}_{{{left}\\mid {right}}}({first_arg} \\mid {second_arg})"

    braced = re.compile(r"\b([A-Za-z]+)_\{([^|{}]+)\|([^{}]+)\}\(([^|()]+)\|([^()]+)\)")
    bare = re.compile(r"\b([A-Za-z]+)_([A-Za-z0-9\\]+)\|([A-Za-z0-9\\]+)\(([^|()]+)\|([^()]+)\)")
    return bare.sub(repl, braced.sub(repl, text))


def protect_sized_delimiter_pipes(text: str) -> tuple[str, list[str]]:
    protected: list[str] = []

    def repl(match: re.Match[str]) -> str:
        protected.append(re.sub(r"\s+\|$", "|", match.group(0)))
        return f"@@DELIMPIPE{len(protected) - 1}@@"

    return SIZED_DELIMITER_PIPE_PATTERN.sub(repl, text), protected


def restore_sized_delimiter_pipes(text: str, protected: Sequence[str]) -> str:
    for index, original in enumerate(protected):
        text = text.replace(f"@@DELIMPIPE{index}@@", original)
    return text


def normalize_math_tex(raw: str) -> str:
    text = html.unescape(raw or "").strip()
    text = text.replace("∫", r"\int")
    text = text.replace("\u2212", "-")
    text = text.replace("\u2264", r"\le")
    text = text.replace("\u2265", r"\ge")
    text = text.replace("\u2248", r"\approx")
    text = text.replace("\u2260", r"\ne")
    text = text.replace("\u00d7", r"\cdot")
    text = text.replace(r"\mathbin{:}", ":")
    text = text.replace("÷", r"\div")
    text = text.replace("⋅", r"\cdot")
    text = text.replace("·", r"\cdot")
    text = text.replace("≤", r"\le")
    text = text.replace("≥", r"\ge")
    text = text.replace("≈", r"\approx")
    text = text.replace("≠", r"\ne")
    text = replace_balanced_calls(text, "sqrt", lambda inner: rf"\sqrt{{{normalize_math_tex(inner)}}}")
    text = replace_balanced_calls(
        text,
        "root",
        lambda inner: (
            lambda parts: rf"\sqrt[{normalize_math_tex(parts[1])}]{{{normalize_math_tex(parts[0])}}}"
            if len(parts) == 2
            else f"root({inner})"
        )(split_top_level(inner))
    )
    text = normalize_fraction_syntax(text)
    text = normalize_conditional_function_syntax(text)
    text = normalize_legacy_alignment_syntax(text)
    text = convert_custom_matrix_notation(text)
    text = normalize_evaluation_bar_syntax(text)
    text = re.sub(r"\bK_(\d+)\s*,\s*(\d+)\b", r"K_{\1,\2}", text)

    align_marker = "@@ALIGN@@"
    text = text.replace("|=", align_marker)
    text, protected_delimiter_pipes = protect_sized_delimiter_pipes(text)
    text = re.sub(r"(?<!\\)\|", r" \\mid ", text)
    text = text.replace(align_marker, "|=")

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(^|[({=,])\s*-\s+(?=[A-Za-z0-9\\])", lambda m: m.group(1) + "-", text)
    text = re.sub(r"\s+([,.;:?!])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = text.replace("{ ", "{").replace(" }", "}")
    text = restore_sized_delimiter_pipes(text, protected_delimiter_pipes)
    return text.strip()


def split_trailing_punctuation(text: str) -> tuple[str, str]:
    if not text:
        return "", ""
    match = re.match(r"^(.*?)(?<!\\)([.,;:?!])$", text)
    if not match:
        return text, ""
    return match.group(1).rstrip(), match.group(2)


def relation_prefix(text: str) -> str | None:
    for token in RELATION_COMMANDS:
        if text.startswith(token):
            return token
    return None


def aligned_display_math(text: str) -> str:
    clean = normalize_math_tex(text)
    clean, _ = split_trailing_punctuation(clean)
    pieces = [piece.strip() for piece in clean.split(";") if piece.strip()]
    if not pieces:
        return wrap_math_display(clean)

    lines: list[str] = []
    for index, piece in enumerate(pieces):
        if "|=" in piece:
            left, right = piece.split("|=", 1)
            lines.append(f"{left.strip()} &= {right.strip()}")
            continue
        relation = relation_prefix(piece)
        if relation:
            lines.append(f"&{piece}")
        elif index == 0:
            lines.append(piece)
        else:
            lines.append(f"&= {piece}")

    body = " \\\\\n".join(lines)
    return wrap_math_display("\n".join([r"\begin{aligned}", body, r"\end{aligned}"]))


def math_to_markdown(raw: str, display: bool) -> str:
    normalized = normalize_math_tex(raw)
    if display:
        if "|=" in normalized:
            return aligned_display_math(raw)
        normalized, _ = split_trailing_punctuation(normalized)
        return wrap_math_display(normalized)

    normalized, punctuation = split_trailing_punctuation(normalized)
    return wrap_math_inline(normalized) + punctuation


def extract_single_bracket_placeholder(text: str, name: str) -> str | None:
    normalized = normalize_ws(text)
    prefix = f"[{name}:"
    if not normalized.startswith(prefix):
        return None

    depth = 1
    index = len(prefix)
    while index < len(normalized):
        char = normalized[index]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                content = normalized[len(prefix):index].strip()
                trailing = normalized[index + 1 :].strip()
                if trailing or not content:
                    return None
                return content
        index += 1

    return None


def question_math_prompt_sentence(raw_text: str) -> str | None:
    expr = extract_math_placeholder(raw_text)
    if expr is None:
        return None
    if not expr.endswith("="):
        return None
    expr = normalize_math_tex(expr[:-1].rstrip())
    return f"What is {wrap_math_inline(expr)}?"


def extract_math_placeholder(text: str) -> str | None:
    return extract_single_bracket_placeholder(text, "MATH")


def math_span_raw_text(node: Tag) -> str | None:
    classes = set(node.get("class", []))
    if node.name == "span" and "math" in classes:
        return extract_math_placeholder(node.get_text("", strip=True))
    return None


def markdown_escape_table_cell(text: str) -> str:
    return text.replace("|", r"\|").replace("\n", "<br>")


class LessonImageResolver:
    def __init__(self, topic_id: str, lessons_root: Path) -> None:
        self.topic_id = str(topic_id)
        self.image_dir = lessons_root / self.topic_id / "Source" / "Images"
        self.lookup: dict[str, Path] = {}
        meta_path = self.image_dir / "_image_meta.json"
        if meta_path.is_file():
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            for row in data.get("images", []):
                if not isinstance(row, dict):
                    continue
                src = row.get("img_src")
                filename = row.get("filename")
                if not src or not filename:
                    continue
                path = self.image_dir / filename
                if path.is_file():
                    self.lookup[str(src)] = path

    def resolve(self, src: str) -> Path | None:
        src = (src or "").strip()
        if not src:
            return None
        if src in self.lookup:
            return self.lookup[src]

        stem = Path(src).name
        for candidate in self.image_dir.glob(f"{stem}.*"):
            if candidate.is_file():
                self.lookup[src] = candidate
                return candidate
        return None

    def relative_markdown_path(self, src: str) -> str | None:
        path = self.resolve(src)
        if path is None:
            return None
        return f"Source/Images/{path.name}"


def is_significant_node(node) -> bool:
    return not (isinstance(node, NavigableString) and not normalize_ws(str(node)))


def render_inline_node(node, ctx: MarkdownContext) -> str:
    if isinstance(node, NavigableString):
        return html.unescape(str(node))

    if not isinstance(node, Tag):
        return ""

    classes = set(node.get("class", []))

    if node.name == "span" and "math" in classes:
        raw = extract_math_placeholder(node.get_text("", strip=True))
        return math_to_markdown(raw or node.get_text("", strip=True), display=False)

    if node.name == "span" and "select-list" in classes:
        return rf" $\underline{{\hspace{{{ctx.select_width}}}}}$ "

    if node.name == "span" and "blank" in classes:
        return rf" $\underline{{\hspace{{{ctx.blank_width}}}}}$ "

    if node.name == "img":
        src = (node.get("src") or "").strip()
        rel = ctx.image_resolver.relative_markdown_path(src)
        if rel is None:
            return f"[Missing image: {src}]"
        return f"![]({rel})"

    if node.name in {"strong", "b"}:
        inner = "".join(render_inline_node(child, ctx) for child in node.children)
        return f"**{inner.strip()}**"

    if node.name in {"em", "i"}:
        inner = "".join(render_inline_node(child, ctx) for child in node.children)
        return f"*{inner.strip()}*"

    if node.name == "code":
        inner = "".join(render_inline_node(child, ctx) for child in node.children)
        return f"`{inner.strip()}`"

    if node.name == "br":
        return "\n"

    if node.name == "a":
        inner = "".join(render_inline_node(child, ctx) for child in node.children).strip()
        href = (node.get("href") or "").strip()
        return f"[{inner}]({href})" if href else inner

    return "".join(render_inline_node(child, ctx) for child in node.children)


def normalize_inline_markdown(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\s+([,.;:?!])", r"\1", text)
    text = re.sub(r"([(\[{])\s+", r"\1", text)
    text = re.sub(r"\s+([)\]}])", r"\1", text)
    return text.strip()


def display_worthy_math(raw: str) -> bool:
    normalized = normalize_math_tex(raw)
    if "|=" in raw:
        return True
    if any(token in normalized for token in (r"\dfrac", r"\frac", r"\approx", r"\le", r"\ge", r"\ne")):
        return True
    if "=" in normalized:
        if normalized.startswith(("P(", "f(", "f_", "E(", "K_")):
            return True
        if any(token in normalized for token in ("+", r"\cdot", r"\sqrt", "/")):
            return True
        if len(normalized) >= 12:
            return True
    return False


def paragraph_buffer_to_block(buffer: str) -> list[Block]:
    text = normalize_inline_markdown(buffer)
    return [Block("paragraph", text)] if text else []


def render_paragraph_block(tag: Tag, ctx: MarkdownContext) -> list[Block]:
    if all(child.name == "img" or (isinstance(child, NavigableString) and not normalize_ws(str(child))) for child in tag.children if is_significant_node(child)):
        blocks: list[Block] = []
        for img in tag.find_all("img", recursive=False):
            blocks.extend(render_image_block(img, ctx))
        return blocks

    raw_text = normalize_ws(tag.get_text(" ", strip=True))
    if not raw_text:
        return []

    if raw_text.upper() == "EXPLANATION":
        return []

    raw_math = extract_math_placeholder(raw_text)
    if raw_math is not None and ctx.standalone_math_display:
        return [Block("display_math", math_to_markdown(raw_math, display=True))]
    if raw_math is not None:
        return [Block("paragraph", math_to_markdown(raw_math, display=False))]

    if ctx.standalone_math_display:
        split_blocks: list[Block] = []
        buffer: list[str] = []
        did_split = False
        for child in tag.children:
            raw_math = math_span_raw_text(child) if isinstance(child, Tag) else None
            if raw_math and display_worthy_math(raw_math):
                split_blocks.extend(paragraph_buffer_to_block("".join(buffer)))
                buffer = []
                split_blocks.append(Block("display_math", math_to_markdown(raw_math, display=True)))
                did_split = True
                continue
            buffer.append(render_inline_node(child, ctx))
        split_blocks.extend(paragraph_buffer_to_block("".join(buffer)))
        if did_split:
            return split_blocks

    text = "".join(render_inline_node(child, ctx) for child in tag.children)
    text = normalize_inline_markdown(text)
    if not text:
        return []
    return [Block("paragraph", text)]


def render_image_block(tag: Tag, ctx: MarkdownContext) -> list[Block]:
    src = (tag.get("src") or "").strip()
    rel = ctx.image_resolver.relative_markdown_path(src)
    if rel is None:
        return [Block("image", f"[Missing image: {src}]")]
    return [Block("image", f"![]({rel})")]


def render_list_block(tag: Tag, ctx: MarkdownContext) -> list[Block]:
    lines: list[str] = []
    ordered = tag.name == "ol"
    for index, li in enumerate(tag.find_all("li", recursive=False), start=1):
        text = normalize_inline_markdown("".join(render_inline_node(child, ctx) for child in li.children))
        if not text:
            continue
        marker = f"{index}." if ordered else "-"
        lines.append(f"{marker} {text}")
    if not lines:
        return []
    return [Block("list", "\n".join(lines))]


def render_blockquote_block(tag: Tag, ctx: MarkdownContext) -> list[Block]:
    quote_ctx = MarkdownContext(
        image_resolver=ctx.image_resolver,
        blank_width=ctx.blank_width,
        select_width=ctx.select_width,
        standalone_math_display=False,
    )
    nested = render_children_as_blocks(tag, quote_ctx)
    if not nested:
        return []
    lines: list[str] = []
    for block in nested:
        for line in block.markdown.splitlines():
            lines.append("> " + line if line else ">")
    return [Block("blockquote", "\n".join(lines))]


def render_table_block(tag: Tag, ctx: MarkdownContext) -> list[Block]:
    rows: list[list[str]] = []
    for tr in tag.find_all("tr", recursive=False) or tag.find_all("tr"):
        cells = tr.find_all(["th", "td"], recursive=False) or tr.find_all(["th", "td"])
        if not cells:
            continue
        row: list[str] = []
        for cell in cells:
            text = normalize_inline_markdown("".join(render_inline_node(child, ctx) for child in cell.children))
            row.append(markdown_escape_table_cell(text))
        rows.append(row)

    if not rows:
        return []

    width = max(len(row) for row in rows)
    padded = [row + [""] * (width - len(row)) for row in rows]
    header = padded[0]
    aligns = ["---"] + ["---:"] * (width - 1)
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(aligns) + " |",
    ]
    for row in padded[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return [Block("table", "\n".join(lines))]


def render_generic_block(tag: Tag, ctx: MarkdownContext) -> list[Block]:
    text = normalize_inline_markdown("".join(render_inline_node(child, ctx) for child in tag.children))
    if not text:
        return []
    return [Block("paragraph", text)]


def render_block_node(node, ctx: MarkdownContext) -> list[Block]:
    if isinstance(node, NavigableString):
        text = normalize_ws(str(node))
        return [Block("paragraph", text)] if text else []

    if not isinstance(node, Tag):
        return []

    if node.name == "p":
        return render_paragraph_block(node, ctx)
    if node.name == "table":
        return render_table_block(node, ctx)
    if node.name == "blockquote":
        return render_blockquote_block(node, ctx)
    if node.name == "img":
        return render_image_block(node, ctx)
    if node.name in {"ul", "ol"}:
        return render_list_block(node, ctx)
    if node.name == "div":
        return render_children_as_blocks(node, ctx)
    return render_generic_block(node, ctx)


def render_children_as_blocks(tag: Tag, ctx: MarkdownContext) -> list[Block]:
    blocks: list[Block] = []
    for child in tag.children:
        blocks.extend(render_block_node(child, ctx))
    return blocks


def html_fragment_to_blocks(fragment_html: str, ctx: MarkdownContext) -> list[Block]:
    html_text = (fragment_html or "").strip()
    if not html_text:
        return []
    soup = BeautifulSoup(html_text, "html.parser")
    blocks: list[Block] = []
    for child in soup.contents:
        blocks.extend(render_block_node(child, ctx))
    return [block for block in blocks if block.markdown.strip()]


def append_block(lines: list[str], block: str) -> None:
    if not block:
        return
    if lines and lines[-1] != "":
        lines.append("")
    lines.extend(block.splitlines())
    lines.append("")


def blocks_to_markdown(blocks: Sequence[Block]) -> str:
    lines: list[str] = []
    for block in blocks:
        append_block(lines, block.markdown)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def prompt_blocks(fragment: dict[str, Any], ctx: MarkdownContext) -> list[Block]:
    return html_fragment_to_blocks(fragment.get("normalized_html", ""), ctx)


def render_example_step(item: dict[str, Any], ctx: MarkdownContext) -> list[str]:
    lines: list[str] = []
    prompt_blocks_list: list[Block] = []
    explanation_blocks: list[Block] = []
    prompt_ctx = MarkdownContext(
        image_resolver=ctx.image_resolver,
        blank_width=ctx.blank_width,
        select_width=ctx.select_width,
        standalone_math_display=False,
    )

    for section in item.get("sections", []):
        if section.get("section_type") == "example_question":
            prompt_blocks_list.extend(prompt_blocks(section, prompt_ctx))
            continue
        if normalize_ws(section.get("readable_text", "")).upper() == "EXPLANATION":
            continue
        explanation_blocks.extend(html_fragment_to_blocks(section.get("normalized_html", ""), ctx))

    intro_block_index = next((idx for idx, block in enumerate(prompt_blocks_list) if block.kind == "paragraph"), None)
    if intro_block_index is None:
        lines.append("**Example:**")
        lines.append("")
        remaining_prompt_blocks = prompt_blocks_list
    else:
        intro = prompt_blocks_list[intro_block_index].markdown
        lines.append(f"**Example:** {intro}")
        lines.append("")
        remaining_prompt_blocks = [
            block for idx, block in enumerate(prompt_blocks_list) if idx != intro_block_index
        ]

    for block in remaining_prompt_blocks:
        append_block(lines, block.markdown)

    if explanation_blocks:
        lines.append("**Explanation**")
        lines.append("")
        for block in explanation_blocks:
            append_block(lines, block.markdown)

    while lines and lines[-1] == "":
        lines.pop()
    return lines


def render_tutorial_step(item: dict[str, Any], ctx: MarkdownContext) -> list[str]:
    lines: list[str] = []
    for section in item.get("sections", []):
        if normalize_ws(section.get("readable_text", "")).upper() == "EXPLANATION":
            continue
        for block in html_fragment_to_blocks(section.get("normalized_html", ""), ctx):
            append_block(lines, block.markdown)
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def render_nested_table_choices(choices: Sequence[dict[str, Any]], ctx: MarkdownContext) -> str | None:
    parsed_rows: list[tuple[str, list[list[str]]]] = []
    for choice in choices:
        soup = BeautifulSoup(choice.get("normalized_html", ""), "html.parser")
        table = soup.find("table")
        if table is None:
            return None
        rows: list[list[str]] = []
        for tr in table.find_all("tr"):
            cells = tr.find_all(["th", "td"])
            if not cells:
                continue
            row = [
                markdown_escape_table_cell(
                    normalize_inline_markdown("".join(render_inline_node(child, ctx) for child in cell.children))
                )
                for cell in cells
            ]
            rows.append(row)
        if len(rows) != 2:
            return None
        parsed_rows.append((upper_choice_label(choice.get("label")), rows))

    if not parsed_rows:
        return None

    template_rows = parsed_rows[0][1]
    if len(template_rows) != 2 or any(len(rows) != 2 for _, rows in parsed_rows):
        return None

    header_cells = template_rows[0]
    value_label = template_rows[1][0]
    domain_variable = header_cells[0].strip("$")
    value_headers: list[str] = []

    for domain_value in header_cells[1:]:
        raw_value = domain_value.strip("$")
        substituted = re.sub(
            rf"(?<![A-Za-z]){re.escape(domain_variable)}(?![A-Za-z])",
            raw_value,
            value_label.strip("$"),
            count=1,
        )
        value_headers.append(f"${substituted}$")

    lines = [
        "#### Choices",
        "",
        "| Option | " + " | ".join(value_headers) + " |",
        "| --- | " + " | ".join(["---:"] * len(value_headers)) + " |",
    ]

    for option, rows in parsed_rows:
        values = rows[1][1:]
        lines.append("| " + " | ".join([option, *values]) + " |")

    return "\n".join(lines)


def markdown_contains_integral(markdown: str) -> bool:
    return r"\int" in markdown or "∫" in markdown


def render_multiple_choice_choice_lines(choice: dict[str, Any], ctx: MarkdownContext) -> list[str]:
    label = upper_choice_label(choice.get("label"))
    blocks = html_fragment_to_blocks(choice.get("normalized_html", ""), ctx)

    if len(blocks) == 1 and blocks[0].kind in {"paragraph", "image", "display_math"}:
        return [f"- [ ] {label}. {blocks[0].markdown}"]

    if len(blocks) == 1 and blocks[0].kind == "table":
        return [f"- [ ] {label}.", "", *blocks[0].markdown.splitlines()]

    lines = [f"- [ ] {label}."]
    for block in blocks:
        lines.append("")
        lines.extend(block.markdown.splitlines())
    return lines


def render_multiple_choice_choices(choices: Sequence[dict[str, Any]], ctx: MarkdownContext) -> str:
    inline_ctx = MarkdownContext(
        image_resolver=ctx.image_resolver,
        blank_width=ctx.blank_width,
        select_width=ctx.select_width,
        standalone_math_display=False,
    )
    if choices and all(choice.get("content_type") == "nested-table" for choice in choices):
        combined = render_nested_table_choices(choices, inline_ctx)
        if combined:
            return combined

    lines: list[str] = []
    rendered_choices = [
        render_multiple_choice_choice_lines(choice, inline_ctx)
        for choice in choices
    ]
    space_between_choices = any(
        markdown_contains_integral("\n".join(choice_lines))
        for choice_lines in rendered_choices
    )

    for index, choice_lines in enumerate(rendered_choices):
        if index > 0 and space_between_choices:
            lines.append("")
        lines.extend(choice_lines)

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def render_select_option_markdown(option: dict[str, Any], ctx: MarkdownContext) -> str:
    html_text = (option.get("normalized_html", "") or "").strip()
    if html_text and not html_text.startswith("<p"):
        html_text = f"<p>{html_text}</p>"
    blocks = html_fragment_to_blocks(html_text, ctx)
    if blocks:
        return " ".join(block.markdown for block in blocks).strip()
    return option.get("readable_text", "").strip()


def render_select_lists(select_lists: Sequence[dict[str, Any]], ctx: MarkdownContext) -> str:
    inline_ctx = MarkdownContext(
        image_resolver=ctx.image_resolver,
        blank_width=ctx.blank_width,
        select_width=ctx.select_width,
        standalone_math_display=False,
    )
    sections: list[str] = []
    for index, select_list in enumerate(select_lists, start=1):
        title = "#### Select" if len(select_lists) == 1 else f"#### Select {index}"
        lines = [title, ""]
        options = [
            render_select_option_markdown(option, inline_ctx)
            for option in select_list.get("options", [])
        ]
        space_between_options = any(markdown_contains_integral(option) for option in options)
        for option_index, option in enumerate(options):
            if option_index > 0 and space_between_options:
                lines.append("")
            lines.append(f"- [ ] {option}")
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


MISSING_ANSWER_MARKER = "MA_ANSWER_MISSING"


def normalize_quiz_id(raw: Any, fallback: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]+", "-", str(raw or "").strip()).strip("-")
    return value.lower() or fallback


def append_yaml_scalar(lines: list[str], key: str, value: str, indent: int = 0) -> None:
    prefix = " " * indent
    text = (value or "").rstrip()
    if not text:
        lines.append(f'{prefix}{key}: ""')
        return

    lines.append(f"{prefix}{key}: |-")
    for line in text.splitlines():
        lines.append(f"{prefix}  {line}" if line else f"{prefix}  ")


def append_missing_answer_comment(lines: list[str], detail: str) -> None:
    lines.append(f"# {MISSING_ANSWER_MARKER}: {detail}")


def quiz_block(lines: Sequence[str]) -> str:
    return "\n".join(["```quiz", *lines, "```"])


def quiz_truthy(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return False


def quiz_answer_value(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def quiz_choice_is_correct(choice: dict[str, Any]) -> bool:
    return any(
        quiz_truthy(choice.get(key))
        for key in ("correct", "is_correct", "answer", "is_answer")
    )


def render_question_content_markdown(
    item: dict[str, Any],
    ctx: MarkdownContext,
    prompt_blocks_list: Sequence[Block],
    body_blocks: Sequence[Block],
    graphic_blocks: Sequence[Block],
    calculator_blocks: Sequence[Block],
    *,
    simple_inline_prompt: bool,
) -> str:
    prompt_raw_text = item.get("prompt", {}).get("readable_text", "")
    if simple_inline_prompt:
        return question_math_prompt_sentence(prompt_raw_text) or blocks_to_markdown(prompt_blocks_list)

    lines: list[str] = []
    for block in graphic_blocks:
        append_block(lines, block.markdown)
    for block in prompt_blocks_list:
        append_block(lines, block.markdown)
    for block in calculator_blocks:
        quote_lines = ["> " + line if line else ">" for line in block.markdown.splitlines()]
        append_block(lines, "\n".join(quote_lines))
    for block in body_blocks:
        append_block(lines, block.markdown)

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def render_choice_markdown(choice: dict[str, Any], ctx: MarkdownContext) -> str:
    blocks = html_fragment_to_blocks(choice.get("normalized_html", ""), ctx)
    if blocks:
        return blocks_to_markdown(blocks)
    return normalize_ws(choice.get("readable_text", ""))


def render_radio_or_checkbox_quiz_block(
    item: dict[str, Any], ctx: MarkdownContext, content: str
) -> str | None:
    choices = item.get("choices", []) or []
    if not choices:
        return None

    inline_ctx = MarkdownContext(
        image_resolver=ctx.image_resolver,
        blank_width=ctx.blank_width,
        select_width=ctx.select_width,
        standalone_math_display=False,
    )
    correct_count = sum(1 for choice in choices if quiz_choice_is_correct(choice))
    quiz_type = "checkbox" if correct_count > 1 else "radio"
    question_id = normalize_quiz_id(item.get("question_id"), f"question-{item.get('question_number', 'unknown')}")

    lines = [f"type: {quiz_type}", f"id: ma-{question_id}"]
    if correct_count == 0:
        append_missing_answer_comment(
            lines,
            "set exactly one options[].correct=true for radio, or all correct options for checkbox",
        )
    append_yaml_scalar(lines, "content", content)
    lines.append("options:")

    for index, choice in enumerate(choices, start=1):
        option_id = normalize_quiz_id(choice.get("label"), f"option-{index}")
        lines.append(f"- id: {option_id}")
        append_yaml_scalar(lines, "content", render_choice_markdown(choice, inline_ctx), indent=2)
        if quiz_choice_is_correct(choice):
            lines.append("  correct: true")

    return quiz_block(lines)


def render_free_quiz_block(item: dict[str, Any], content: str) -> str:
    question_id = normalize_quiz_id(item.get("question_id"), f"question-{item.get('question_number', 'unknown')}")
    correct = quiz_answer_value(item, "correct", "answer", "correct_answer", "reference_answer")
    feedback = quiz_answer_value(item, "feedback", "answer_feedback")

    lines = ["type: free", f"id: ma-{question_id}"]
    if not correct:
        append_missing_answer_comment(lines, "set correct to an optional reference answer")
    append_yaml_scalar(lines, "content", content)
    if correct:
        append_yaml_scalar(lines, "correct", correct)
    if feedback:
        append_yaml_scalar(lines, "feedback", feedback)
    return quiz_block(lines)


def select_option_id(select_index: int, option_index: int) -> str:
    return f"select-{select_index}-option-{option_index}"


def render_select_quiz_blocks(
    item: dict[str, Any], ctx: MarkdownContext, content: str
) -> list[str]:
    blocks: list[str] = []
    inline_ctx = MarkdownContext(
        image_resolver=ctx.image_resolver,
        blank_width=ctx.blank_width,
        select_width=ctx.select_width,
        standalone_math_display=False,
    )
    question_id = normalize_quiz_id(item.get("question_id"), f"question-{item.get('question_number', 'unknown')}")

    for select_list in item.get("select_lists", []) or []:
        select_index = int(select_list.get("index") or len(blocks) + 1)
        options = select_list.get("options", []) or []
        if not options:
            continue

        block_id = f"ma-{question_id}-select-{select_index}"
        lines = ["type: select", f"id: {block_id}"]
        append_missing_answer_comment(
            lines,
            f"set questions[0].correct_option to one of this block's options[].id values",
        )
        append_yaml_scalar(lines, "content", content)
        lines.append("options:")

        correct_option = ""
        for option_index, option in enumerate(options, start=1):
            option_id = select_option_id(select_index, option_index)
            if quiz_choice_is_correct(option):
                correct_option = option_id
            lines.append(f"- id: {option_id}")
            append_yaml_scalar(lines, "content", render_select_option_markdown(option, inline_ctx), indent=2)

        lines.append("questions:")
        lines.append(f"- id: select-{select_index}")
        append_yaml_scalar(lines, "content", f"Select {select_index}", indent=2)
        if correct_option:
            lines.append(f"  correct_option: {correct_option}")

        blocks.append(quiz_block(lines))

    return blocks


def render_blank_quiz_block(item: dict[str, Any], content: str) -> str:
    question_id = normalize_quiz_id(item.get("question_id"), f"question-{item.get('question_number', 'unknown')}")
    feedback = quiz_answer_value(item, "feedback", "answer_feedback")

    lines = ["type: blank", f"id: ma-{question_id}", "require_exact: false"]
    if "==" not in content:
        append_missing_answer_comment(lines, "wrap each expected answer in content with ==answer==")
    append_yaml_scalar(lines, "content", content)
    if feedback:
        append_yaml_scalar(lines, "feedback", feedback)
    return quiz_block(lines)


def render_question(item: dict[str, Any], ctx: MarkdownContext) -> list[str]:
    lines: list[str] = []
    question_ctx = MarkdownContext(
        image_resolver=ctx.image_resolver,
        blank_width=ctx.blank_width,
        select_width=ctx.select_width,
        standalone_math_display=False,
    )
    prompt_raw_text = item.get("prompt", {}).get("readable_text", "")
    prompt_blocks_list = prompt_blocks(item.get("prompt", {}), question_ctx)
    body_blocks = prompt_blocks(item.get("body", {}), question_ctx)
    graphic_blocks = prompt_blocks(item.get("graphic", {}), question_ctx)
    calculator_blocks = prompt_blocks(item.get("calculator_instructions", {}), question_ctx)

    simple_inline_prompt = (
        item.get("question_format") == "multiple-choice"
        and not graphic_blocks
        and not body_blocks
        and not calculator_blocks
        and len(prompt_blocks_list) == 1
        and prompt_blocks_list[0].kind in {"paragraph", "display_math"}
        and all(choice.get("content_type") == "text" for choice in item.get("choices", []))
    )

    lines.append(f"**Question {item['question_number']}:**")
    lines.append("")

    content = render_question_content_markdown(
        item,
        question_ctx,
        prompt_blocks_list,
        body_blocks,
        graphic_blocks,
        calculator_blocks,
        simple_inline_prompt=simple_inline_prompt,
    )

    question_format = item.get("question_format")
    if question_format == "multiple-choice":
        quiz = render_radio_or_checkbox_quiz_block(item, ctx, content)
        if quiz:
            append_block(lines, quiz)
    elif question_format == "select-list":
        for quiz in render_select_quiz_blocks(item, ctx, content):
            append_block(lines, quiz)
    elif question_format == "free-response":
        append_block(lines, render_free_quiz_block(item, content))
    elif question_format == "blank":
        append_block(lines, render_blank_quiz_block(item, content))
    else:
        append_block(lines, content)

    while lines and lines[-1] == "":
        lines.pop()
    return lines


def render_item(item: dict[str, Any], ctx: MarkdownContext) -> list[str]:
    if item.get("item_type") == "question":
        return render_question(item, ctx)
    if item.get("step_type") == "example":
        return render_example_step(item, ctx)
    return render_tutorial_step(item, ctx)


def render_lesson_markdown(data: dict[str, Any], ctx: MarkdownContext) -> str:
    lines: list[str] = [f"# {data['topic_title']}", "", "## Table of Contents", ""]

    section_links = data.get("toc", {}).get("section_links", [])
    for link in section_links:
        title = link.get("title", "").strip()
        if not title:
            continue
        lines.append(f"- [{title}](#{slugify_heading(title)})")

    prerequisites = data.get("toc", {}).get("topic_prerequisites", [])
    if prerequisites:
        lines.extend(["", "## Prerequisites", ""])
        for prereq in prerequisites:
            prereq_id = str(prereq.get("topic_id", "")).strip()
            name = prereq.get("name", "").strip()
            if not prereq_id or not name:
                continue
            lines.append(f"- [{name}](../{prereq_id}/{prereq_id}.md)")

    items = data.get("lesson", {}).get("items", [])
    for item in items:
        lines.extend(["", "---", ""])
        if item.get("item_type") == "step":
            title = item.get("title", "").strip()
            if title:
                lines.append(f'<a id="{slugify_heading(title)}"></a>')
                lines.append(f"## {title}")
                lines.append("")
        lines.extend(render_item(item, ctx))

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def write_text_atomic(path: Path, content: str) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(content, encoding="utf-8")
    tmp_path.replace(path)


def normalize_topic_id(raw: str) -> str:
    value = str(raw).strip()
    if not value.isdigit():
        raise SystemExit(f"Invalid topic id: {raw!r}")
    return value


def lesson_json_path(lessons_root: Path, topic_id: str) -> Path:
    return lessons_root / topic_id / "Source" / f"{topic_id}.json"


def lesson_markdown_path(output_root: Path, topic_id: str) -> Path:
    return output_root / topic_id / f"{topic_id}.md"


def discover_topic_ids(lessons_root: Path) -> list[str]:
    if not lessons_root.is_dir():
        return []
    return sorted(
        (
            entry.name
            for entry in lessons_root.iterdir()
            if entry.is_dir() and entry.name.isdigit()
        ),
        key=int,
    )


def resolve_input_path(raw: str, lessons_root: Path) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.exists():
        return candidate.resolve()

    if raw.isdigit():
        topic_json = lesson_json_path(lessons_root, raw)
        if topic_json.is_file():
            return topic_json.resolve()

    return candidate.resolve()


def collect_json_files(paths: list[Path], lessons_root: Path) -> list[Path]:
    json_files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() == ".json" and path.name == f"{path.stem}.json":
            json_files.append(path.resolve())
            continue

        if not path.is_dir():
            continue

        if path == lessons_root:
            topic_ids = discover_topic_ids(lessons_root)
            for topic_id in topic_ids:
                json_path = lesson_json_path(lessons_root, topic_id)
                if json_path.is_file():
                    json_files.append(json_path.resolve())
            continue

        for candidate in path.rglob("*.json"):
            if candidate.name.startswith("_"):
                continue
            if candidate.parent.name != "Source":
                continue
            if candidate.stem != candidate.parent.parent.name:
                continue
            json_files.append(candidate.resolve())

    return sorted(set(json_files), key=lambda path: int(path.stem) if path.stem.isdigit() else path.stem)


def write_markdown(json_path: Path, output_root: Path, lessons_root: Path) -> Path:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    topic_id = normalize_topic_id(str(data["topic_id"]))
    resolver = LessonImageResolver(topic_id, lessons_root)
    ctx = MarkdownContext(image_resolver=resolver)
    markdown = render_lesson_markdown(data, ctx)

    output_path = lesson_markdown_path(output_root, topic_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_text_atomic(output_path, markdown)
    return output_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render lesson JSON files into DATA/Lessons/[topic-id]/[topic-id].md.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=[],
        help="Lesson JSON file(s), topic ids, or directories containing lesson JSON files.",
    )
    parser.add_argument(
        "--lessons-root",
        type=Path,
        default=DEFAULT_LESSONS_ROOT,
        help="Root DATA/Lessons directory.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_LESSONS_ROOT,
        help="Root directory where lesson markdown files will be written.",
    )
    parser.add_argument(
        "--topic-id",
        dest="topic_ids",
        action="append",
        default=[],
        help="Specific topic id to render. Repeatable.",
    )
    parser.add_argument(
        "--start-at",
        help="Start processing at this topic id after filtering.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of pending lessons to process after filtering.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate markdown even if the output file already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be processed without writing markdown.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue processing other lessons when one lesson fails.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable the interactive tqdm progress bar.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each generated Markdown path.",
    )
    return parser.parse_args(argv)


def select_json_files(args: argparse.Namespace, lessons_root: Path) -> list[Path]:
    raw_paths = list(args.paths)
    raw_paths.extend(args.topic_ids)
    if not raw_paths:
        raw_paths = [str(lessons_root)]
    input_paths = [resolve_input_path(raw, lessons_root) for raw in raw_paths]
    json_files = collect_json_files(input_paths, lessons_root)

    if args.start_at:
        start_at = normalize_topic_id(args.start_at)
        start_index = next((index for index, path in enumerate(json_files) if path.stem == start_at), None)
        if start_index is None:
            raise SystemExit(f"--start-at topic {start_at!r} was not found after filtering")
        json_files = json_files[start_index:]

    return json_files


def filter_pending(json_files: list[Path], output_root: Path) -> list[Path]:
    pending: list[Path] = []
    for json_path in json_files:
        output_path = lesson_markdown_path(output_root, json_path.stem)
        if output_path.is_file() and output_path.stat().st_size > 0:
            continue
        pending.append(json_path)
    return pending


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    lessons_root = args.lessons_root.expanduser().resolve()
    output_root = args.output_root.expanduser().resolve()
    interactive_progress = not args.no_progress and sys.stderr.isatty()

    json_files = select_json_files(args, lessons_root)
    if not json_files:
        progress_write("No lesson JSON files found.")
        return 0

    runnable = json_files if args.force else filter_pending(json_files, output_root)
    if args.limit is not None:
        if args.limit <= 0:
            raise SystemExit("--limit must be positive")
        runnable = runnable[: args.limit]

    if not runnable:
        progress_write("No pending lesson markdown files found.")
        return 0

    if args.dry_run:
        print(f"Dry run: would process {len(runnable)} lesson(s).")
        for json_path in runnable[:10]:
            print(f"  {json_path} -> {lesson_markdown_path(output_root, json_path.stem)}")
        if len(runnable) > 10:
            print(f"  ... and {len(runnable) - 10} more")
        return 0

    written = 0
    failed: list[tuple[Path, str]] = []
    progress = progress_bar(
        total=len(runnable),
        desc="Lesson Markdown",
        unit="lesson",
        disable=not interactive_progress,
    )

    try:
        for json_path in runnable:
            try:
                output_path = write_markdown(json_path, output_root, lessons_root)
                written += 1
                if args.verbose:
                    progress_write(f"wrote {output_path}")
            except Exception as exc:
                failed.append((json_path, str(exc)))
                progress_write(f"error {json_path}: {exc}")
                if not args.continue_on_error:
                    return 1
            finally:
                progress.update(1)
                progress.set_postfix(written=written, failed=len(failed))
    finally:
        progress.close()

    progress_write(f"Lesson Markdown complete: written={written} failed={len(failed)}")
    if failed:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    return run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
