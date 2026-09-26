#!/usr/bin/env python3
"""Validate canonical Obsidian quiz blocks produced by quiz-block-factory."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_TYPES = {
    "radio",
    "checkbox",
    "select",
    "multi-select",
    "noodle",
    "free",
    "blank",
}

# These mirror the plugin's canonical strict root schemas in
# vault/.obsidian/plugins/quiz-blocks/main.js. The validator deliberately
# requires canonical `content` rather than the plugin's legacy root aliases
# `text` and `question`. In particular, feedback is a root field only for free
# and blank quizzes; radio/checkbox feedback belongs on individual options.
COMMON_ROOT_FIELDS = {"type", "id", "content", "gated", "shuffle"}
TYPE_ROOT_FIELDS = {
    "radio": {"options"},
    "checkbox": {"options"},
    "select": {"options", "questions"},
    "multi-select": {"questions"},
    "noodle": {"options", "questions"},
    "free": {"correct", "feedback"},
    "blank": {"input_mode", "require_exact", "feedback"},
}
OPTION_FIELDS = {"id", "content", "correct", "feedback"}
QUESTION_FIELDS = {"id", "content", "correct_option", "feedback"}
MULTI_QUESTION_FIELDS = QUESTION_FIELDS | {"options"}

TOP_KEY_CAPTURE_RE = re.compile(
    r'''^(?:"([^"]+)"|'([^']+)'|([A-Za-z_][A-Za-z0-9_.-]*))\s*:'''
)
TOP_KEY_RE = TOP_KEY_CAPTURE_RE
RAW_MCQ_RE = re.compile(r"^\s*-\s+\[[ xX]\]\s+[A-Za-z]\.\s+")
GENERIC_FEEDBACK_RE = re.compile(
    r"^(?:correct|incorrect|wrong|try again|not quite|recheck|check your work|"
    r"this is correct|this is incorrect|that is correct|that is incorrect)\.?$",
    flags=re.IGNORECASE,
)
OPAQUE_FEEDBACK_RE = re.compile(
    r"^(?:recheck|check the (?:formula|arithmetic|signs?|units?)|"
    r"this (?:value |choice )?does not (?:follow|result)|"
    r"that (?:value |choice )?does not (?:follow|result))\b",
    flags=re.IGNORECASE,
)
OPEN_FENCE = "```quiz"
CLOSE_FENCE = "```"
BLANK_ANSWER_RE = re.compile(r"==([\s\S]*?)==")
YAML_BOOLEAN_RE = re.compile(r"^(?:true|false)$", flags=re.IGNORECASE)
YAML_NULL_RE = re.compile(r"^(?:null|~)$", flags=re.IGNORECASE)
YAML_NUMBER_RE = re.compile(
    r"^[+-]?(?:0[bB][01_]+|0[oO][0-7_]+|0[xX][0-9a-fA-F_]+|"
    r"(?:(?:0|[1-9][0-9_]*)(?:\.[0-9_]*)?|\.[0-9_]+)(?:[eE][+-]?[0-9_]+)?)$"
)


@dataclass(frozen=True)
class QuizBlock:
    start_line: int
    end_line: int
    lines: list[str]


@dataclass(frozen=True)
class Issue:
    path: Path
    line: int
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.message}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown files to validate.")
    parser.add_argument(
        "--allow-no-quiz",
        action="store_true",
        help="Do not fail files that contain no quiz blocks.",
    )
    parser.add_argument(
        "--allow-raw-mcq",
        action="store_true",
        help="Allow raw '- [ ] A.' multiple-choice lists outside quiz blocks.",
    )
    parser.add_argument(
        "--require-radio-practice",
        action="store_true",
        help="Require every quiz block to use type: radio.",
    )
    parser.add_argument(
        "--require-radio-shuffle",
        action="store_true",
        help="Require every radio quiz to set shuffle: true.",
    )
    parser.add_argument(
        "--strict-ids",
        action="store_true",
        help="Require quiz block ids and option ids where applicable.",
    )
    parser.add_argument(
        "--require-feedback",
        action="store_true",
        help=(
            "Require feedback on every radio/checkbox option and select-style "
            "question, both a reference answer and root feedback on free "
            "quizzes, and root feedback on blank quizzes."
        ),
    )
    parser.add_argument(
        "--lint-feedback",
        action="store_true",
        help="Reject generic, opaque, or duplicated feedback; semantic quality still requires human review.",
    )
    return parser.parse_args()


def extract_quiz_blocks(path: Path, lines: list[str]) -> tuple[list[QuizBlock], list[Issue], set[int]]:
    blocks: list[QuizBlock] = []
    issues: list[Issue] = []
    covered: set[int] = set()
    index = 0
    while index < len(lines):
        if lines[index].strip() != OPEN_FENCE:
            index += 1
            continue

        start = index
        index += 1
        body: list[str] = []
        while index < len(lines) and lines[index].strip() != CLOSE_FENCE:
            body.append(lines[index].rstrip("\n"))
            index += 1

        if index >= len(lines):
            issues.append(Issue(path, start + 1, "unclosed ```quiz fence"))
            break

        end = index
        covered.update(range(start, end + 1))
        blocks.append(QuizBlock(start_line=start + 1, end_line=end + 1, lines=body))
        index += 1
    return blocks, issues, covered


def strip_yaml_inline_comment(value: str) -> str:
    """Remove a YAML comment while preserving hashes inside quoted scalars."""
    quote: str | None = None
    escaped = False
    for index, char in enumerate(value):
        if quote == '"' and char == "\\" and not escaped:
            escaped = True
            continue
        if char in {"'", '"'} and not escaped:
            quote = None if quote == char else char if quote is None else quote
        elif char == "#" and quote is None and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
        escaped = False
    return value.strip()


def strip_quotes(value: str) -> str:
    value = strip_yaml_inline_comment(value.strip())
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def field_key_pattern(key: str) -> str:
    """Match a YAML mapping key whether plain or explicitly quoted."""
    escaped = re.escape(key)
    return rf'(?:{escaped}|"{escaped}"|\'{escaped}\')'


def root_inline_value(lines: list[str], key: str) -> str | None:
    """Return a top-level inline value without YAML-style coercion."""
    pattern = re.compile(rf"^{field_key_pattern(key)}\s*:\s*(.*)$")
    for line in lines:
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return None


def direct_inline_value(item: list[str], key: str, indent: str = "") -> str | None:
    """Return an item's direct inline value without matching nested fields."""
    key_pattern = field_key_pattern(key)
    first_pattern = re.compile(rf"^{re.escape(indent)}-\s+{key_pattern}\s*:\s*(.*)$")
    direct_pattern = re.compile(rf"^{re.escape(indent)}  {key_pattern}\s*:\s*(.*)$")
    for index, line in enumerate(item):
        match = first_pattern.match(line) if index == 0 else direct_pattern.match(line)
        if match:
            return match.group(1).strip()
    return None


def is_nontext_yaml_scalar(raw: str | None) -> bool:
    """Identify null or collection values the runtime cannot coerce to text."""
    if raw is None or not raw:
        return False
    raw = strip_yaml_inline_comment(raw)
    if raw[0] in {"'", '"'}:
        return False
    return bool(YAML_NULL_RE.fullmatch(raw) or raw[0] in "[{")


def is_canonical_text_id(raw: str | None) -> bool:
    """Require IDs to survive YAML parsing as nonempty text."""
    if raw is None:
        return False
    raw = strip_yaml_inline_comment(raw)
    if not raw or raw in {"|-", "|", ">-", ">"}:
        return False
    if raw[0] in {"'", '"'}:
        return len(strip_quotes(raw).strip()) > 0
    return not (
        YAML_NULL_RE.fullmatch(raw)
        or YAML_BOOLEAN_RE.fullmatch(raw)
        or YAML_NUMBER_RE.fullmatch(raw)
        or raw[0] in "[{"
    )


def yaml_boolean_value(raw: str | None) -> bool | None:
    """Return a canonical YAML boolean value, ignoring an inline comment."""
    if raw is None:
        return None
    value = strip_yaml_inline_comment(raw)
    if not YAML_BOOLEAN_RE.fullmatch(value):
        return None
    return value.lower() == "true"


def item_start_line(block: QuizBlock, item: list[str]) -> int:
    """Return the one-based source line for an item's first line."""
    for index in range(len(block.lines) - len(item) + 1):
        if block.lines[index : index + len(item)] == item:
            return block.start_line + index + 1
    return block.start_line


def item_field_line(block: QuizBlock, item: list[str], line: str) -> int:
    """Return the one-based source line for a field inside an item."""
    return item_start_line(block, item) + item.index(line)


def top_block(lines: list[str], key: str) -> list[str]:
    start = None
    for index, line in enumerate(lines):
        if re.match(rf"^{field_key_pattern(key)}\s*:", line):
            start = index + 1
            break
    if start is None:
        return []

    end = len(lines)
    for index in range(start, len(lines)):
        if TOP_KEY_RE.match(lines[index]):
            end = index
            break
    return lines[start:end]


def split_list_items(lines: list[str], indent: str = "") -> list[list[str]]:
    items: list[list[str]] = []
    current: list[str] = []
    prefix = f"{indent}- "
    for line in lines:
        if line.startswith(prefix):
            if current:
                items.append(current)
            current = [line]
        elif current:
            current.append(line)
    if current:
        items.append(current)
    return items


def nested_block(item: list[str], key: str, indent: str = "  ") -> list[str]:
    start = None
    for index, line in enumerate(item):
        if re.match(rf"^{re.escape(indent)}{field_key_pattern(key)}\s*:", line):
            start = index + 1
            break
    if start is None:
        return []

    end = len(item)
    for index in range(start, len(item)):
        line = item[index]
        if line and not line.startswith(indent):
            end = index
            break
    return item[start:end]


def count_correct_true(items: list[list[str]]) -> int:
    return sum(1 for item in items if yaml_boolean_value(direct_inline_value(item, "correct")) is True)


def direct_item_fields(item: list[str], indent: str = "") -> list[tuple[str, str]]:
    """Return canonical direct fields without mistaking nested fields for siblings."""
    entries: list[tuple[str, str]] = []
    first_prefix = f"{indent}- "
    direct_prefix = f"{indent}  "
    for index, line in enumerate(item):
        candidate = None
        if index == 0 and line.startswith(first_prefix):
            candidate = line[len(first_prefix) :]
        elif line.startswith(direct_prefix):
            candidate = line[len(direct_prefix) :]
            if candidate.startswith((" ", "- ")):
                continue
        if candidate is None:
            continue
        match = TOP_KEY_CAPTURE_RE.match(candidate)
        if match:
            field = next(group for group in match.groups() if group is not None)
            entries.append((field, line))
    return entries


def direct_field_text(item: list[str], key: str, indent: str = "") -> str | None:
    """Return the normalized text of a direct item field, or None when absent."""
    key_pattern = field_key_pattern(key)
    first_pattern = re.compile(rf"^{re.escape(indent)}-\s+{key_pattern}\s*:\s*(.*)$")
    direct_pattern = re.compile(rf"^{re.escape(indent)}  {key_pattern}\s*:\s*(.*)$")
    for index, line in enumerate(item):
        match = first_pattern.match(line) if index == 0 else direct_pattern.match(line)
        if not match:
            continue
        value = match.group(1).strip()
        if value not in {"|-", "|", ">-", ">"}:
            return strip_quotes(value).strip()
        key_indent = len(line) - len(line.lstrip(" "))
        body: list[str] = []
        for following in item[index + 1 :]:
            if not following.strip():
                body.append("")
                continue
            following_indent = len(following) - len(following.lstrip(" "))
            if following_indent <= key_indent:
                break
            body.append(following.strip())
        return "\n".join(body).strip()
    return None


def direct_field_has_content(item: list[str], key: str, indent: str = "") -> bool:
    """Return whether a direct item field exists and contains nonempty text."""
    raw = direct_inline_value(item, key, indent)
    return not is_nontext_yaml_scalar(raw) and bool(direct_field_text(item, key, indent))


def root_field_text(lines: list[str], key: str) -> str | None:
    """Return the normalized text of a top-level field, or None when absent."""
    pattern = re.compile(rf"^{field_key_pattern(key)}\s*:\s*(.*)$")
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        value = match.group(1).strip()
        if value not in {"|-", "|", ">-", ">"}:
            return strip_quotes(value).strip()
        body: list[str] = []
        for following in lines[index + 1 :]:
            if not following.strip():
                body.append("")
                continue
            if not following.startswith("  "):
                break
            body.append(following.strip())
        return "\n".join(body).strip()
    return None


def root_field_has_content(lines: list[str], key: str) -> bool:
    """Return whether a top-level scalar or block-scalar field is nonempty."""
    raw = root_inline_value(lines, key)
    return not is_nontext_yaml_scalar(raw) and bool(root_field_text(lines, key))


def normalized_feedback(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def validate_feedback_quality(path: Path, block: QuizBlock, quiz_type: str) -> list[Issue]:
    """Reject deterministic anti-patterns without pretending to grade pedagogy."""
    targets: list[tuple[str, str, int]] = []
    if quiz_type in {"radio", "checkbox"}:
        for index, item in enumerate(split_list_items(top_block(block.lines, "options")), start=1):
            text = direct_field_text(item, "feedback")
            if text:
                option_id = direct_field_text(item, "id")
                label = f"option {option_id}" if option_id else f"option {index}"
                targets.append((label, text, item_start_line(block, item)))
    elif quiz_type in {"select", "noodle"}:
        for index, item in enumerate(split_list_items(top_block(block.lines, "questions")), start=1):
            text = direct_field_text(item, "feedback")
            if text:
                question_id = direct_field_text(item, "id")
                label = f"question {question_id}" if question_id else f"question {index}"
                targets.append((label, text, item_start_line(block, item)))
    elif quiz_type == "multi-select":
        for index, item in enumerate(split_list_items(top_block(block.lines, "questions")), start=1):
            text = direct_field_text(item, "feedback")
            if text:
                question_id = direct_field_text(item, "id")
                label = f"question {question_id}" if question_id else f"question {index}"
                targets.append((label, text, item_start_line(block, item)))
    elif quiz_type in {"free", "blank"}:
        text = root_field_text(block.lines, "feedback")
        if text:
            targets.append(("root feedback", text, block.start_line))

    issues: list[Issue] = []
    seen: dict[str, str] = {}
    for label, text, line in targets:
        normalized = normalized_feedback(text)
        if GENERIC_FEEDBACK_RE.fullmatch(normalized) or OPAQUE_FEEDBACK_RE.match(normalized):
            issues.append(
                Issue(
                    path,
                    line,
                    f"{label} feedback is generic or opaque; diagnose the rule or misconception",
                )
            )
        fingerprint = normalized.casefold()
        if fingerprint in seen:
            issues.append(
                Issue(
                    path,
                    line,
                    f"{label} duplicates feedback from {seen[fingerprint]}; make it option-specific",
                )
            )
        else:
            seen[fingerprint] = label
    return issues


def validate_item_fields(
    path: Path,
    block: QuizBlock,
    item: list[str],
    *,
    allowed: set[str],
    label: str,
    indent: str = "",
) -> list[Issue]:
    issues: list[Issue] = []
    seen_fields: set[str] = set()
    for field, line in direct_item_fields(item, indent):
        field_line = item_field_line(block, item, line)
        if field not in allowed:
            issues.append(
                Issue(
                    path,
                    field_line,
                    f"unknown field for {label}: {field}",
                )
            )
        elif field in seen_fields:
            issues.append(Issue(path, field_line, f"duplicate field for {label}: {field}"))
        seen_fields.add(field)
    return issues


def validate_top_level_fields(path: Path, block: QuizBlock, quiz_type: str) -> list[Issue]:
    """Reject fields that the plugin's strict schema rejects for this type."""
    allowed = COMMON_ROOT_FIELDS | TYPE_ROOT_FIELDS[quiz_type]
    issues: list[Issue] = []
    seen_fields: set[str] = set()
    for offset, line in enumerate(block.lines, start=1):
        match = TOP_KEY_CAPTURE_RE.match(line)
        if match:
            field = next(group for group in match.groups() if group is not None)
        else:
            field = None
        if field is not None and field not in allowed:
            issues.append(
                Issue(
                    path,
                    block.start_line + offset,
                    f"unknown top-level field for {quiz_type} quiz: {field}",
                )
            )
        elif field is not None and field in seen_fields:
            issues.append(
                Issue(
                    path,
                    block.start_line + offset,
                    f"duplicate top-level field for {quiz_type} quiz: {field}",
                )
            )
        if field is not None:
            seen_fields.add(field)
    return issues


def option_ids(items: list[list[str]], indent: str = "") -> list[str]:
    ids: list[str] = []
    for item in items:
        value = direct_field_text(item, "id", indent)
        if value:
            ids.append(value)
    return ids


def validate_question_id(
    path: Path,
    block: QuizBlock,
    question: list[str],
    *,
    index: int,
    quiz_type: str,
    strict_ids: bool,
    seen_ids: set[str],
) -> list[Issue]:
    line = item_start_line(block, question)
    question_id = direct_field_text(question, "id")
    raw_question_id = direct_inline_value(question, "id")
    issues: list[Issue] = []
    if strict_ids and not question_id:
        issues.append(Issue(path, line, f"{quiz_type} question {index} is missing id"))
    elif question_id and not is_canonical_text_id(raw_question_id):
        issues.append(Issue(path, line, f"{quiz_type} question {index} id must be nonempty YAML text"))
    if question_id:
        if question_id in seen_ids:
            issues.append(Issue(path, line, f"duplicate question id: {question_id}"))
        seen_ids.add(question_id)
    return issues


def validate_options(
    path: Path,
    block: QuizBlock,
    items: list[list[str]],
    *,
    strict_ids: bool,
    require_feedback: bool,
    feedback_is_rendered: bool = True,
    indent: str = "",
) -> list[Issue]:
    issues: list[Issue] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(items, start=1):
        option_line = item_start_line(block, item)
        issues.extend(
            validate_item_fields(
                path,
                block,
                item,
                allowed=OPTION_FIELDS,
                label=f"option {index}",
                indent=indent,
            )
        )
        if not direct_field_has_content(item, "content", indent):
            issues.append(Issue(path, option_line, f"option {index} is missing nonempty content"))
        if require_feedback and not direct_field_has_content(item, "feedback", indent):
            issues.append(Issue(path, option_line, f"option {index} is missing nonempty feedback"))
        if not feedback_is_rendered and direct_field_has_content(item, "feedback", indent):
            issues.append(
                Issue(
                    path,
                    option_line,
                    f"option {index} feedback is not rendered for this quiz type; move it to the question",
                )
            )
        raw_correct = direct_inline_value(item, "correct", indent)
        if raw_correct is not None and yaml_boolean_value(raw_correct) is None:
            issues.append(Issue(path, option_line, f"option {index} correct must be true or false"))
        option_id = direct_field_text(item, "id", indent)
        raw_option_id = direct_inline_value(item, "id", indent)
        if strict_ids and not option_id:
            issues.append(Issue(path, option_line, f"option {index} is missing id"))
        elif option_id and not is_canonical_text_id(raw_option_id):
            issues.append(Issue(path, option_line, f"option {index} id must be nonempty YAML text"))
        if option_id:
            if option_id in seen_ids:
                issues.append(Issue(path, option_line, f"duplicate option id: {option_id}"))
            seen_ids.add(option_id)
    return issues


def validate_radio_or_checkbox(
    path: Path,
    block: QuizBlock,
    quiz_type: str,
    *,
    strict_ids: bool,
    require_feedback: bool,
) -> list[Issue]:
    issues: list[Issue] = []
    options = split_list_items(top_block(block.lines, "options"))
    if len(options) < 2:
        return [Issue(path, block.start_line, f"{quiz_type} quiz requires at least two options")]

    issues.extend(
        validate_options(
            path,
            block,
            options,
            strict_ids=strict_ids,
            require_feedback=require_feedback,
        )
    )
    correct_count = count_correct_true(options)
    if quiz_type == "radio" and correct_count != 1:
        issues.append(Issue(path, block.start_line, "radio quiz requires exactly one correct: true option"))
    if quiz_type == "checkbox" and correct_count < 1:
        issues.append(Issue(path, block.start_line, "checkbox quiz requires at least one correct: true option"))
    return issues


def validate_select(
    path: Path,
    block: QuizBlock,
    *,
    strict_ids: bool,
    require_feedback: bool,
) -> list[Issue]:
    issues: list[Issue] = []
    options = split_list_items(top_block(block.lines, "options"))
    questions = split_list_items(top_block(block.lines, "questions"))
    if len(options) < 2:
        issues.append(Issue(path, block.start_line, "select quiz requires at least two top-level options"))
    if not questions:
        issues.append(Issue(path, block.start_line, "select quiz requires questions"))
    issues.extend(
        validate_options(
            path,
            block,
            options,
            strict_ids=True,
            require_feedback=False,
            feedback_is_rendered=False,
        )
    )
    ids = set(option_ids(options))
    seen_question_ids: set[str] = set()
    for index, question in enumerate(questions, start=1):
        line = item_start_line(block, question)
        issues.extend(
            validate_question_id(
                path,
                block,
                question,
                index=index,
                quiz_type="select",
                strict_ids=strict_ids,
                seen_ids=seen_question_ids,
            )
        )
        issues.extend(
            validate_item_fields(
                path,
                block,
                question,
                allowed=QUESTION_FIELDS,
                label=f"select question {index}",
            )
        )
        if not direct_field_has_content(question, "content"):
            issues.append(Issue(path, line, f"select question {index} is missing nonempty content"))
        if require_feedback and not direct_field_has_content(question, "feedback"):
            issues.append(Issue(path, line, f"select question {index} is missing nonempty feedback"))
        correct = direct_field_text(question, "correct_option")
        raw_correct = direct_inline_value(question, "correct_option")
        if not correct:
            issues.append(Issue(path, line, f"select question {index} is missing correct_option"))
        elif not is_canonical_text_id(raw_correct):
            issues.append(Issue(path, line, f"select question {index} correct_option must be YAML text"))
        elif correct not in ids:
            issues.append(Issue(path, line, f"select question {index} correct_option does not match an option id"))
    return issues


def validate_multi_select(
    path: Path,
    block: QuizBlock,
    *,
    strict_ids: bool,
    require_feedback: bool,
) -> list[Issue]:
    issues: list[Issue] = []
    questions = split_list_items(top_block(block.lines, "questions"))
    if not questions:
        return [Issue(path, block.start_line, "multi-select quiz requires questions")]
    seen_question_ids: set[str] = set()
    for index, question in enumerate(questions, start=1):
        line = item_start_line(block, question)
        issues.extend(
            validate_question_id(
                path,
                block,
                question,
                index=index,
                quiz_type="multi-select",
                strict_ids=strict_ids,
                seen_ids=seen_question_ids,
            )
        )
        issues.extend(
            validate_item_fields(
                path,
                block,
                question,
                allowed=MULTI_QUESTION_FIELDS,
                label=f"multi-select question {index}",
            )
        )
        if not direct_field_has_content(question, "content"):
            issues.append(Issue(path, line, f"multi-select question {index} is missing nonempty content"))
        if require_feedback and not direct_field_has_content(question, "feedback"):
            issues.append(Issue(path, line, f"multi-select question {index} is missing nonempty feedback"))
        nested_options = split_list_items(nested_block(question, "options", indent="  "), indent="  ")
        if len(nested_options) < 2:
            issues.append(Issue(path, line, f"multi-select question {index} requires at least two options"))
            continue
        issues.extend(
            validate_options(
                path,
                block,
                nested_options,
                strict_ids=True,
                require_feedback=False,
                feedback_is_rendered=False,
                indent="  ",
            )
        )
        ids = set(option_ids(nested_options, indent="  "))
        correct = direct_field_text(question, "correct_option")
        raw_correct = direct_inline_value(question, "correct_option")
        if not correct:
            issues.append(Issue(path, line, f"multi-select question {index} is missing correct_option"))
        elif not is_canonical_text_id(raw_correct):
            issues.append(Issue(path, line, f"multi-select question {index} correct_option must be YAML text"))
        elif correct not in ids:
            issues.append(Issue(path, line, f"multi-select question {index} correct_option does not match an option id"))
    return issues


def validate_noodle(
    path: Path,
    block: QuizBlock,
    *,
    strict_ids: bool,
    require_feedback: bool,
) -> list[Issue]:
    issues: list[Issue] = []
    options = split_list_items(top_block(block.lines, "options"))
    questions = split_list_items(top_block(block.lines, "questions"))
    if len(options) < 2:
        issues.append(Issue(path, block.start_line, "noodle quiz requires at least two options"))
    if len(questions) < 2:
        issues.append(Issue(path, block.start_line, "noodle quiz requires at least two questions"))
    if len(options) != len(questions):
        issues.append(
            Issue(
                path,
                block.start_line,
                "noodle quiz requires equal option and question counts for one-to-one matching",
            )
        )
    issues.extend(
        validate_options(
            path,
            block,
            options,
            strict_ids=strict_ids,
            require_feedback=False,
            feedback_is_rendered=False,
        )
    )
    ids = set(option_ids(options))
    seen_question_ids: set[str] = set()
    used_correct_options: set[str] = set()
    for index, question in enumerate(questions, start=1):
        line = item_start_line(block, question)
        issues.extend(
            validate_question_id(
                path,
                block,
                question,
                index=index,
                quiz_type="noodle",
                strict_ids=strict_ids,
                seen_ids=seen_question_ids,
            )
        )
        issues.extend(
            validate_item_fields(
                path,
                block,
                question,
                allowed=QUESTION_FIELDS,
                label=f"noodle question {index}",
            )
        )
        if not direct_field_has_content(question, "content"):
            issues.append(Issue(path, line, f"noodle question {index} is missing nonempty content"))
        correct = direct_field_text(question, "correct_option")
        raw_correct = direct_inline_value(question, "correct_option")
        if not correct:
            issues.append(Issue(path, line, f"noodle question {index} is missing correct_option"))
        elif not is_canonical_text_id(raw_correct):
            issues.append(Issue(path, line, f"noodle question {index} correct_option must be YAML text"))
        elif correct not in ids:
            issues.append(Issue(path, line, f"noodle question {index} correct_option does not match an option id"))
        elif correct in used_correct_options:
            issues.append(
                Issue(
                    path,
                    line,
                    f"noodle question {index} reuses correct_option {correct}; matching must be one-to-one",
                )
            )
        else:
            used_correct_options.add(correct)
        if require_feedback and not direct_field_has_content(question, "feedback"):
            issues.append(Issue(path, line, f"noodle question {index} is missing nonempty feedback"))
    return issues


def validate_block(
    path: Path,
    block: QuizBlock,
    *,
    require_radio_practice: bool,
    require_radio_shuffle: bool,
    strict_ids: bool,
    require_feedback: bool,
    lint_feedback: bool,
) -> list[Issue]:
    issues: list[Issue] = []
    quiz_type = root_field_text(block.lines, "type")
    if not quiz_type:
        return [Issue(path, block.start_line, "quiz block is missing type")]
    if quiz_type not in SUPPORTED_TYPES:
        return [Issue(path, block.start_line, f"unsupported quiz type: {quiz_type}")]
    issues.extend(validate_top_level_fields(path, block, quiz_type))
    if require_radio_practice and quiz_type != "radio":
        issues.append(Issue(path, block.start_line, f"expected type: radio for core-move practice, found {quiz_type}"))
    if (
        require_radio_shuffle
        and quiz_type == "radio"
        and yaml_boolean_value(root_inline_value(block.lines, "shuffle")) is not True
    ):
        issues.append(Issue(path, block.start_line, "radio quiz must set shuffle: true"))
    block_id = root_field_text(block.lines, "id")
    raw_block_id = root_inline_value(block.lines, "id")
    if strict_ids and not block_id:
        issues.append(Issue(path, block.start_line, "quiz block is missing id"))
    elif block_id and not is_canonical_text_id(raw_block_id):
        issues.append(Issue(path, block.start_line, "quiz block id must be nonempty YAML text"))
    for boolean_field in ("gated", "shuffle"):
        raw_boolean = root_inline_value(block.lines, boolean_field)
        if raw_boolean is not None and yaml_boolean_value(raw_boolean) is None:
            issues.append(Issue(path, block.start_line, f"{boolean_field} must be true or false"))
    if not root_field_has_content(block.lines, "content"):
        issues.append(Issue(path, block.start_line, "quiz block is missing nonempty content"))

    if quiz_type in {"radio", "checkbox"}:
        issues.extend(
            validate_radio_or_checkbox(
                path,
                block,
                quiz_type,
                strict_ids=strict_ids,
                require_feedback=require_feedback,
            )
        )
    elif quiz_type == "select":
        issues.extend(
            validate_select(
                path,
                block,
                strict_ids=strict_ids,
                require_feedback=require_feedback,
            )
        )
    elif quiz_type == "multi-select":
        issues.extend(
            validate_multi_select(
                path,
                block,
                strict_ids=strict_ids,
                require_feedback=require_feedback,
            )
        )
    elif quiz_type == "noodle":
        issues.extend(
            validate_noodle(
                path,
                block,
                strict_ids=strict_ids,
                require_feedback=require_feedback,
            )
        )
    elif quiz_type == "free" and require_feedback:
        if not root_field_has_content(block.lines, "correct"):
            issues.append(Issue(path, block.start_line, "free quiz is missing a nonempty reference answer in correct"))
        if not root_field_has_content(block.lines, "feedback"):
            issues.append(Issue(path, block.start_line, "free quiz is missing nonempty feedback"))
    elif quiz_type == "blank":
        input_mode = root_field_text(block.lines, "input_mode")
        if input_mode is not None and input_mode not in {"text", "math"}:
            issues.append(Issue(path, block.start_line, "input_mode must be text or math"))
        raw_require_exact = root_inline_value(block.lines, "require_exact")
        if raw_require_exact is not None and yaml_boolean_value(raw_require_exact) is None:
            issues.append(Issue(path, block.start_line, "require_exact must be true or false"))
        content = root_field_text(block.lines, "content") or ""
        answers = BLANK_ANSWER_RE.findall(content)
        if not answers:
            issues.append(Issue(path, block.start_line, "blank quiz content must contain at least one ==answer== gap"))
        elif any(not answer.strip() for answer in answers):
            issues.append(Issue(path, block.start_line, "blank quiz answers inside ==...== must not be empty"))
    if quiz_type == "blank" and require_feedback and not root_field_has_content(block.lines, "feedback"):
        issues.append(Issue(path, block.start_line, "blank quiz is missing nonempty feedback"))
    if lint_feedback:
        issues.extend(validate_feedback_quality(path, block, quiz_type))
    return issues


def validate_file(path: Path, args: argparse.Namespace) -> tuple[list[Issue], int]:
    if not path.exists():
        return [Issue(path, 1, "file not found")], 0
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks, issues, covered = extract_quiz_blocks(path, lines)
    if not blocks and not args.allow_no_quiz:
        issues.append(Issue(path, 1, "file contains no quiz blocks"))
    if not args.allow_raw_mcq:
        for index, line in enumerate(lines, start=1):
            if index - 1 not in covered and RAW_MCQ_RE.match(line):
                issues.append(Issue(path, index, "raw checklist MCQ found outside a quiz block"))
    seen_block_ids: set[str] = set()
    for block in blocks:
        block_id = root_field_text(block.lines, "id")
        if block_id:
            if block_id in seen_block_ids:
                issues.append(Issue(path, block.start_line, f"duplicate quiz block id: {block_id}"))
            seen_block_ids.add(block_id)
        issues.extend(
            validate_block(
                path,
                block,
                require_radio_practice=args.require_radio_practice,
                require_radio_shuffle=getattr(args, "require_radio_shuffle", False),
                strict_ids=args.strict_ids,
                require_feedback=getattr(args, "require_feedback", False),
                lint_feedback=getattr(args, "lint_feedback", False),
            )
        )
    return issues, len(blocks)


def main() -> int:
    args = parse_args()
    all_issues: list[Issue] = []
    block_count = 0
    for raw_path in args.paths:
        path = raw_path.expanduser()
        issues, count = validate_file(path, args)
        all_issues.extend(issues)
        block_count += count

    for issue in all_issues:
        print(issue.render(), file=sys.stderr)

    if all_issues:
        print(f"quiz block validation failed: {len(all_issues)} issue(s), {block_count} block(s) checked", file=sys.stderr)
        return 1

    print(f"quiz block validation passed: {block_count} block(s) checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
