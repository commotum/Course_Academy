#!/usr/bin/env python3
"""Build lesson JSON files from hydrated lesson HTML in DATA/Lessons.

This stage reads:
    DATA/Lessons/[topic-id]/Source/[topic-id].html

and writes:
    DATA/Lessons/[topic-id]/Source/[topic-id].json

The parsing logic is embedded directly here so the stage remains standalone
within PIPELINE.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Comment, NavigableString, Tag


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

INLINE_TAGS = {
    "a",
    "b",
    "br",
    "code",
    "em",
    "i",
    "img",
    "kbd",
    "mark",
    "math",
    "s",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "svg",
    "u",
    "var",
}

INLINE_DIV_CLASSES = {
    "freeResponseLine",
    "matheditor-wrapper-answer",
    "selectList",
}

IGNORED_TAGS = {"script", "style", "noscript"}

MATHML_TEX_OPERATOR_NAMES = {
    "arccos",
    "arccot",
    "arccsc",
    "arcsec",
    "arcsin",
    "arctan",
    "arg",
    "cos",
    "cosh",
    "cot",
    "coth",
    "csc",
    "deg",
    "det",
    "dim",
    "exp",
    "gcd",
    "hom",
    "inf",
    "ker",
    "lg",
    "lim",
    "liminf",
    "limsup",
    "ln",
    "log",
    "max",
    "min",
    "Pr",
    "sec",
    "sin",
    "sinh",
    "sup",
    "tan",
    "tanh",
}


@dataclass
class ItemContext:
    blank_counter: int = 0
    select_counter: int = 0


@dataclass
class RenderResult:
    html: str = ""
    text: str = ""
    images: list[dict[str, Any]] = field(default_factory=list)
    free_entry_blanks: list[dict[str, Any]] = field(default_factory=list)
    select_lists: list[dict[str, Any]] = field(default_factory=list)

    def extend(self, other: "RenderResult") -> None:
        self.html += other.html
        self.text += other.text
        self.images.extend(other.images)
        self.free_entry_blanks.extend(other.free_entry_blanks)
        self.select_lists.extend(other.select_lists)

    def has_content(self) -> bool:
        return bool(
            self.html.strip()
            or self.text.strip()
            or self.images
            or self.free_entry_blanks
            or self.select_lists
        )


@dataclass(frozen=True)
class LessonJob:
    topic_id: str
    lesson_dir: Path
    source_dir: Path
    html_path: Path
    json_path: Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build lesson JSON files in DATA/Lessons from hydrated lesson HTML.",
    )
    parser.add_argument(
        "--lessons-root",
        type=Path,
        default=DEFAULT_LESSONS_ROOT,
        help="Root DATA/Lessons directory.",
    )
    parser.add_argument(
        "--topic-id",
        dest="topic_ids",
        action="append",
        default=[],
        help="Specific topic id to process. Repeatable.",
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
        help="Rebuild JSON even when the target file already exists and is non-empty.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would run without writing files.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable the interactive tqdm progress bar.",
    )
    return parser.parse_args(argv)


def normalize_topic_id(raw: str) -> str:
    value = str(raw).strip()
    if not value.isdigit():
        raise SystemExit(f"Invalid topic id: {raw!r}")
    return value


def nonempty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


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


def build_job(lessons_root: Path, topic_id: str) -> LessonJob:
    lesson_dir = lessons_root / topic_id
    source_dir = lesson_dir / "Source"
    return LessonJob(
        topic_id=topic_id,
        lesson_dir=lesson_dir,
        source_dir=source_dir,
        html_path=source_dir / f"{topic_id}.html",
        json_path=source_dir / f"{topic_id}.json",
    )


def select_jobs(args: argparse.Namespace, lessons_root: Path) -> list[LessonJob]:
    if args.topic_ids:
        topic_ids = sorted({normalize_topic_id(topic_id) for topic_id in args.topic_ids}, key=int)
    else:
        topic_ids = discover_topic_ids(lessons_root)

    if args.start_at:
        start_at = normalize_topic_id(args.start_at)
        start_index = next((index for index, topic_id in enumerate(topic_ids) if topic_id == start_at), None)
        if start_index is None:
            raise SystemExit(f"--start-at topic {start_at!r} was not found after filtering")
        topic_ids = topic_ids[start_index:]

    jobs = [build_job(lessons_root, topic_id) for topic_id in topic_ids]
    jobs = [job for job in jobs if nonempty_file(job.html_path)]

    if not args.force:
        jobs = [job for job in jobs if not nonempty_file(job.json_path)]

    if args.limit is not None:
        if args.limit <= 0:
            raise SystemExit("--limit must be positive")
        jobs = jobs[: args.limit]

    return jobs


def escape_attr(value: str) -> str:
    return html.escape(value, quote=True)


def normalize_ws(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_readable_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_html_fragment(fragment: str) -> str:
    fragment = fragment.replace("\r\n", "\n").replace("\r", "\n")
    fragment = re.sub(r"\n{3,}", "\n\n", fragment)
    return fragment.strip()


def strip_placeholders(text: str) -> str:
    text = re.sub(r"\[IMG:[^\]]*\]", "", text)
    text = re.sub(r"\[FREE_ENTRY \d+\]", "", text)
    text = re.sub(r"\[SELECT \d+\]", "", text)
    text = re.sub(r"\[MATH:[^\]]*\]", "", text)
    return normalize_ws(text)


def dedupe_dict_rows(rows: list[dict[str, Any]], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    unique: list[dict[str, Any]] = []
    for row in rows:
        marker = tuple(row.get(key) for key in keys)
        if marker in seen:
            continue
        seen.add(marker)
        unique.append(row)
    return unique


def merge_meta(*groups: dict[str, Any]) -> dict[str, Any]:
    images: list[dict[str, Any]] = []
    free_entry_blanks: list[dict[str, Any]] = []
    select_lists: list[dict[str, Any]] = []
    for group in groups:
        if not group:
            continue
        images.extend(group.get("images", []))
        free_entry_blanks.extend(group.get("free_entry_blanks", []))
        select_lists.extend(group.get("select_lists", []))
    return {
        "images": dedupe_dict_rows(images, ("src",)),
        "free_entry_blanks": dedupe_dict_rows(free_entry_blanks, ("index", "dom_id")),
        "select_lists": dedupe_dict_rows(select_lists, ("index", "dom_id")),
    }


def wrap_tag(name: str, inner_html: str, attrs: dict[str, str] | None = None) -> str:
    attr_bits: list[str] = []
    if attrs:
        for key, value in attrs.items():
            if value:
                attr_bits.append(f' {key}="{escape_attr(value)}"')
    return f"<{name}{''.join(attr_bits)}>{inner_html}</{name}>"


def extract_topic_id_from_href(href: str) -> str:
    match = re.search(r"/topics/(?:.*-)?(\d+)(?:$|[/?#])", href or "")
    return match.group(1) if match else ""


def parse_question_number(title: str) -> int | None:
    match = re.search(r"(\d+)", title or "")
    return int(match.group(1)) if match else None


def clean_svg_title_math(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_math_operator(op: str) -> str:
    op = op.replace("\xa0", " ").strip()
    if not op or op in {"\u2062", "\u2063"}:
        return ""
    if op in {"⁡", "\u2061"}:
        return " "
    if op in {"(", "[", "{", "|"}:
        return op
    if op in {")", "]", "}", "|"}:
        return op
    if op in {",", ";", ":"}:
        return f"{op} "
    if op in {".", "?", "!"}:
        return op
    if op in {
        "+",
        "-",
        "−",
        "=",
        "≈",
        "≠",
        "<",
        ">",
        "≤",
        "≥",
        "×",
        "⋅",
        "·",
        "÷",
        "±",
        "∈",
        "∉",
        "→",
        "↦",
    }:
        return f" {op} "
    return op


def clean_math_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:?!)\]}])", r"\1", text)
    text = re.sub(r"([(\[{])\s+", r"\1", text)
    text = re.sub(r"\s+([|])", r"\1", text)
    text = re.sub(r"([|])\s+", r"\1", text)
    return text.strip()


def normalize_math_text_leaf(node: Tag) -> str:
    text = node.get_text("", strip=True)
    if text == "i":
        if node.name == "mtext":
            return r"\textrm{i}"
        if node.name == "mi" and node.get("mathvariant") == "normal":
            return r"\textrm{i}"
    if node.name == "mi" and text in MATHML_TEX_OPERATOR_NAMES:
        return rf"\{text}"
    return clean_math_text(text)


def wrap_math_script(text: str) -> str:
    script = clean_math_text(text)
    if not script:
        return ""
    return f"{{{script}}}"


def mathml_to_text(node: Tag | None) -> str:
    if node is None:
        return ""

    name = getattr(node, "name", "") or ""
    if not name:
        return clean_math_text(node.get_text(" ", strip=True))

    if name in {"math", "mrow", "mstyle", "semantics", "annotation-xml", "mphantom", "menclose"}:
        return clean_math_text("".join(mathml_to_text(child) for child in node.children if isinstance(child, (Tag, NavigableString))))

    if name in {"mi", "mn", "mtext", "ms"}:
        return normalize_math_text_leaf(node)

    if name == "mo":
        return normalize_math_operator(node.get_text("", strip=True))

    if name == "mfrac":
        children = [child for child in node.children if isinstance(child, Tag)]
        if len(children) >= 2:
            numerator = mathml_to_text(children[0])
            denominator = mathml_to_text(children[1])
            if re.fullmatch(r"0(?:\.0+)?(?:[A-Za-z%]+)?", node.get("linethickness", "")):
                return r"\genfrac{}{}{0pt}{}{" + numerator + "}{" + denominator + "}"
            return clean_math_text(f"({numerator})/({denominator})")
        return clean_math_text(node.get_text(" ", strip=True))

    if name == "msup":
        children = [child for child in node.children if isinstance(child, Tag)]
        if len(children) >= 2:
            base = mathml_to_text(children[0])
            exponent = wrap_math_script(mathml_to_text(children[1]))
            return clean_math_text(f"{base}^{exponent}")
        return clean_math_text(node.get_text(" ", strip=True))

    if name == "msub":
        children = [child for child in node.children if isinstance(child, Tag)]
        if len(children) >= 2:
            base = mathml_to_text(children[0])
            subscript = wrap_math_script(mathml_to_text(children[1]))
            return clean_math_text(f"{base}_{subscript}")
        return clean_math_text(node.get_text(" ", strip=True))

    if name == "msubsup":
        children = [child for child in node.children if isinstance(child, Tag)]
        if len(children) >= 3:
            base = mathml_to_text(children[0])
            subscript = wrap_math_script(mathml_to_text(children[1]))
            exponent = wrap_math_script(mathml_to_text(children[2]))
            return clean_math_text(
                f"{base}_{subscript}^{exponent}"
            )
        return clean_math_text(node.get_text(" ", strip=True))

    if name == "msqrt":
        inner = "".join(mathml_to_text(child) for child in node.children if isinstance(child, (Tag, NavigableString)))
        return clean_math_text(f"sqrt({inner})")

    if name == "mroot":
        children = [child for child in node.children if isinstance(child, Tag)]
        if len(children) >= 2:
            return clean_math_text(f"root({mathml_to_text(children[0])}, {mathml_to_text(children[1])})")
        return clean_math_text(node.get_text(" ", strip=True))

    if name == "mfenced":
        open_delim = node.get("open", "(")
        close_delim = node.get("close", ")")
        separators = (node.get("separators") or ",").strip() or ","
        parts = [mathml_to_text(child) for child in node.children if isinstance(child, Tag)]
        joined = f"{separators} ".join(part for part in parts if part)
        return clean_math_text(f"{open_delim}{joined}{close_delim}")

    if name == "mover":
        children = [child for child in node.children if isinstance(child, Tag)]
        if len(children) >= 2:
            base = mathml_to_text(children[0])
            over = mathml_to_text(children[1])
            if node.get("accent") == "true" and over in {"¯", "‾", "―"}:
                return clean_math_text(f"overline({base})")
            return clean_math_text(f"{base}^({over})")
        return clean_math_text(node.get_text(" ", strip=True))

    if name == "munder":
        children = [child for child in node.children if isinstance(child, Tag)]
        if len(children) >= 2:
            base = mathml_to_text(children[0])
            condition = mathml_to_text(children[1])
            if base in {"lim", r"\lim"}:
                return r"\lim_{" + condition + "}"
            return clean_math_text(f"{base}_({condition})")
        return clean_math_text(node.get_text(" ", strip=True))

    if name == "munderover":
        children = [child for child in node.children if isinstance(child, Tag)]
        if len(children) >= 3:
            return clean_math_text(
                f"{mathml_to_text(children[0])}_({mathml_to_text(children[1])})^({mathml_to_text(children[2])})"
            )
        return clean_math_text(node.get_text(" ", strip=True))

    if name == "mtable":
        # Pipes and semicolons cannot retain MathML column roles, rules or
        # fences. Downstream regex conversion can mistake them for matrices
        # or absolute values. Keep the raw source and require structural TeX
        # reconstruction instead of emitting a lossy placeholder.
        raise ValueError(
            "MathML table requires structural TeX conversion; preserve the "
            "complete source formula instead of pipe/semicolon serialization"
        )

    if name == "mtr":
        cells = [mathml_to_text(child) for child in node.children if isinstance(child, Tag)]
        return clean_math_text(" | ".join(part for part in cells if part))

    if name in {"mtd", "mtr", "mstyle"}:
        return clean_math_text("".join(mathml_to_text(child) for child in node.children if isinstance(child, (Tag, NavigableString))))

    return clean_math_text(node.get_text(" ", strip=True))


def extract_math_from_node(node: Tag) -> tuple[str, str] | None:
    # A nested assistive MathML root can describe only part of an SVG title.
    # Returning it would discard outer operators, equalities and labels. Keep
    # the archived source intact and report this unsupported conversion rather
    # than emit a mathematically incomplete [MATH: ...] placeholder.
    for title in node.find_all("title"):
        if title.find("math") is not None and any(
            isinstance(child, NavigableString) and str(child).strip()
            for child in title.children
        ):
            raise ValueError(
                "Mixed SVG title contains partial MathML; preserve or reconstruct "
                "the complete outer formula before conversion: "
                + str(title.get("id", "untitled"))
            )
    math_node: Tag | None = None
    if node.name == "math":
        math_node = node
    elif node.name == "mjx-assistive-mml":
        math_node = node.find("math")
    else:
        assistive = node.find("mjx-assistive-mml")
        if assistive is not None:
            math_node = assistive.find("math")

    if math_node is not None:
        return mathml_to_text(math_node), str(math_node)

    title = node.find("title")
    if title is not None:
        title_text = clean_svg_title_math(title.get_text("", strip=False))
        return title_text, str(title)

    if "mjpage" in (node.get("class") or []):
        svg_title = node.select_one("svg title")
        if svg_title is not None:
            title_text = clean_svg_title_math(svg_title.get_text("", strip=False))
            return title_text, str(svg_title)

    return None


def render_math(node: Tag) -> RenderResult:
    extracted = extract_math_from_node(node)
    if extracted is None:
        return RenderResult()
    math_text, _ = extracted
    if not math_text:
        return RenderResult()
    placeholder = f"[MATH: {math_text}]"
    return RenderResult(
        html=wrap_tag("span", html.escape(placeholder), {"class": "math"}),
        text=placeholder,
    )


def is_ignored_node(node: Any) -> bool:
    if isinstance(node, Comment):
        return True
    if isinstance(node, Tag) and node.name in IGNORED_TAGS:
        return True
    return False


def is_inline_like(node: Any) -> bool:
    if isinstance(node, (NavigableString, Comment)):
        return True
    if not isinstance(node, Tag):
        return True
    classes = set(node.get("class", []))
    if classes.intersection(INLINE_DIV_CLASSES):
        return True
    if node.name in INLINE_TAGS:
        return True
    if node.name.startswith("mjx-"):
        return True
    return False


def render_select_list(node: Tag, ctx: ItemContext) -> RenderResult:
    ctx.select_counter += 1
    select_index = ctx.select_counter
    dom_id = (node.get("id") or "").strip()
    frame = node.select_one(".selectListFrame")
    frame_dom_id = (frame.get("id") or "").strip() if frame else ""

    options: list[dict[str, Any]] = []
    for option_index, option in enumerate(node.select(".selectListOptions > .selectListOption"), start=1):
        option_render = render_inline_children(option, ctx)
        option_html = normalize_html_fragment(option_render.html)
        option_text = normalize_readable_text(option_render.text) or normalize_ws(option.get_text(" ", strip=True))
        options.append(
            {
                "index": option_index,
                "normalized_html": option_html,
                "readable_text": option_text,
            }
        )
    placeholder = f"[SELECT {select_index}]"
    return RenderResult(
        html=wrap_tag(
            "span",
            html.escape(placeholder),
            {
                "class": "select-list",
                "data-select-id": dom_id,
                "data-select-index": str(select_index),
            },
        ),
        text=placeholder,
        select_lists=[
            {
                "index": select_index,
                "dom_id": dom_id,
                "frame_dom_id": frame_dom_id,
                "placeholder": placeholder,
                "option_count": len(options),
                "options": options,
            }
        ],
    )


def render_blank(node: Tag, ctx: ItemContext) -> RenderResult:
    ctx.blank_counter += 1
    blank_index = ctx.blank_counter
    dom_id = (node.get("id") or "").strip()
    placeholder = f"[FREE_ENTRY {blank_index}]"
    return RenderResult(
        html=wrap_tag(
            "span",
            html.escape(placeholder),
            {
                "class": "blank",
                "data-blank-id": dom_id,
                "data-blank-index": str(blank_index),
            },
        ),
        text=placeholder,
        free_entry_blanks=[
            {
                "index": blank_index,
                "dom_id": dom_id,
                "placeholder": placeholder,
                "input_type": "math-editor",
            }
        ],
    )


def render_image(node: Tag) -> RenderResult:
    src = (node.get("src") or "").strip()
    alt = normalize_ws(node.get("alt") or "")
    text = f"[IMG: {src}]" if src else "[IMG]"
    attr_bits = [f' src="{escape_attr(src)}"'] if src else []
    if alt:
        attr_bits.append(f' alt="{escape_attr(alt)}"')
    return RenderResult(
        html=f"<img{''.join(attr_bits)}>",
        text=text,
        images=[{"src": src, "alt": alt}] if src else [],
    )


def render_inline_children(node: Tag, ctx: ItemContext) -> RenderResult:
    result = RenderResult()
    for child in node.children:
        if is_ignored_node(child):
            continue
        result.extend(render_inline(child, ctx))
    return result


def render_inline(node: Any, ctx: ItemContext) -> RenderResult:
    if isinstance(node, Comment):
        return RenderResult()

    if isinstance(node, NavigableString):
        text = str(node)
        return RenderResult(html=html.escape(text), text=text)

    if not isinstance(node, Tag):
        return RenderResult()

    if node.name in IGNORED_TAGS:
        return RenderResult()

    classes = set(node.get("class", []))

    if "matheditor-wrapper-answer" in classes:
        return render_blank(node, ctx)

    if "selectList" in classes:
        return render_select_list(node, ctx)

    if node.name == "img":
        return render_image(node)

    if node.name in {"math", "mjx-assistive-mml"}:
        return render_math(node)

    if "mjpage" in classes or node.name == "svg":
        rendered = render_math(node)
        if rendered.has_content():
            return rendered

    if node.name == "mjx-container":
        rendered = render_math(node)
        if node.select_one(".selectList"):
            combined = RenderResult()
            if rendered.has_content():
                combined.extend(rendered)
            for select_list in node.select(".selectList"):
                combined.extend(render_select_list(select_list, ctx))
            if combined.has_content():
                return combined
        if rendered.has_content():
            return rendered
        return render_inline_children(node, ctx)

    if node.name.startswith("mjx-"):
        return render_inline_children(node, ctx)

    if node.name == "br":
        return RenderResult(html="<br/>", text="\n")

    if "freeResponseLine" in classes:
        inner = render_inline_children(node, ctx)
        return RenderResult(
            html=wrap_tag("span", inner.html, {"class": "free-response-line"}),
            text=inner.text,
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    if node.name == "a":
        inner = render_inline_children(node, ctx)
        return RenderResult(
            html=wrap_tag("a", inner.html, {"href": (node.get("href") or "").strip()}),
            text=inner.text,
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    if node.name in {"strong", "em", "b", "i", "u", "span", "small", "sup", "sub", "code", "kbd", "mark", "s", "var"}:
        inner = render_inline_children(node, ctx)
        return RenderResult(
            html=wrap_tag(node.name, inner.html),
            text=inner.text,
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    if node.name in {"p", "div", "table", "ul", "ol", "blockquote"}:
        return render_block(node, ctx)

    return render_inline_children(node, ctx)


def wrap_paragraph(inner: RenderResult) -> RenderResult:
    text = normalize_readable_text(inner.text)
    if not text and not inner.images and not inner.free_entry_blanks and not inner.select_lists:
        return RenderResult()
    return RenderResult(
        html=wrap_tag("p", inner.html),
        text=f"{text}\n\n",
        images=inner.images,
        free_entry_blanks=inner.free_entry_blanks,
        select_lists=inner.select_lists,
    )


def render_list_item(item: Tag, ctx: ItemContext, ordered: bool, index: int) -> RenderResult:
    inner = render_block_children(item, ctx)
    item_text = normalize_readable_text(inner.text)
    prefix = f"{index}. " if ordered else "- "
    return RenderResult(
        html=wrap_tag("li", inner.html),
        text=f"{prefix}{item_text}\n",
        images=inner.images,
        free_entry_blanks=inner.free_entry_blanks,
        select_lists=inner.select_lists,
    )


def extract_table_rows(table: Tag) -> list[Tag]:
    rows: list[Tag] = []
    for child in table.children:
        if not isinstance(child, Tag):
            continue
        if child.name == "tr":
            rows.append(child)
        elif child.name in {"thead", "tbody", "tfoot"}:
            rows.extend(row for row in child.find_all("tr", recursive=False))
    if rows:
        return rows
    return table.find_all("tr")


def render_table(node: Tag, ctx: ItemContext) -> RenderResult:
    html_rows: list[str] = []
    text_rows: list[str] = []
    images: list[dict[str, Any]] = []
    free_entry_blanks: list[dict[str, Any]] = []
    select_lists: list[dict[str, Any]] = []

    rows = extract_table_rows(node)
    for row in rows:
        cell_html_bits: list[str] = []
        cell_text_bits: list[str] = []
        for cell in row.find_all(["th", "td"], recursive=False):
            cell_inner = render_block_children(cell, ctx)
            cell_html = wrap_tag(cell.name, cell_inner.html)
            cell_text = normalize_readable_text(cell_inner.text).replace("\n", " / ")
            cell_html_bits.append(cell_html)
            cell_text_bits.append(cell_text)
            images.extend(cell_inner.images)
            free_entry_blanks.extend(cell_inner.free_entry_blanks)
            select_lists.extend(cell_inner.select_lists)
        if cell_html_bits:
            html_rows.append(wrap_tag("tr", "".join(cell_html_bits)))
            text_rows.append(f"| {' | '.join(cell_text_bits)} |")

    html_table = wrap_tag("table", "".join(html_rows))
    text_table = "\n".join(text_rows)
    if text_table:
        text_table += "\n\n"

    return RenderResult(
        html=html_table,
        text=text_table,
        images=images,
        free_entry_blanks=free_entry_blanks,
        select_lists=select_lists,
    )


def render_block_children(node: Tag, ctx: ItemContext) -> RenderResult:
    result = RenderResult()
    inline_buffer = RenderResult()

    def flush_inline_buffer() -> None:
        nonlocal inline_buffer
        paragraph = wrap_paragraph(inline_buffer)
        if paragraph.has_content():
            result.extend(paragraph)
        inline_buffer = RenderResult()

    for child in node.children:
        if is_ignored_node(child):
            continue
        if is_inline_like(child):
            inline_buffer.extend(render_inline(child, ctx))
            continue
        flush_inline_buffer()
        result.extend(render_block(child, ctx))

    flush_inline_buffer()
    return result


def render_block(node: Tag, ctx: ItemContext) -> RenderResult:
    if node.name in IGNORED_TAGS:
        return RenderResult()

    classes = set(node.get("class", []))

    if classes.intersection({"stepHeader", "questionWidget-header", "questionWidget-buttonBar", "questionWidget-spinnerFrame"}):
        return RenderResult()

    if "keyPrerequisites" in classes:
        return RenderResult()

    if node.name == "table":
        return render_table(node, ctx)

    if node.name == "blockquote":
        inner = render_block_children(node, ctx)
        text = normalize_readable_text(inner.text)
        if text:
            text = "\n".join(f"> {line}" if line else ">" for line in text.splitlines()) + "\n\n"
        return RenderResult(
            html=wrap_tag("blockquote", inner.html),
            text=text,
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    if node.name in {"ul", "ol"}:
        ordered = node.name == "ol"
        html_items: list[str] = []
        text_items: list[str] = []
        images: list[dict[str, Any]] = []
        free_entry_blanks: list[dict[str, Any]] = []
        select_lists: list[dict[str, Any]] = []
        for idx, item in enumerate(node.find_all("li", recursive=False), start=1):
            rendered = render_list_item(item, ctx, ordered=ordered, index=idx)
            html_items.append(rendered.html)
            text_items.append(rendered.text)
            images.extend(rendered.images)
            free_entry_blanks.extend(rendered.free_entry_blanks)
            select_lists.extend(rendered.select_lists)
        return RenderResult(
            html=wrap_tag(node.name, "".join(html_items)),
            text="".join(text_items) + ("\n" if text_items else ""),
            images=images,
            free_entry_blanks=free_entry_blanks,
            select_lists=select_lists,
        )

    if node.name in {"p", "h1", "h2", "h3", "h4", "h5", "h6"}:
        inner = render_inline_children(node, ctx)
        text = normalize_readable_text(inner.text)
        if not text and not inner.images and not inner.free_entry_blanks and not inner.select_lists:
            return RenderResult()
        return RenderResult(
            html=wrap_tag(node.name, inner.html),
            text=f"{text}\n\n",
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    if node.name == "div" and ("graphic" in classes or "questionWidget-graphic" in classes):
        inner = render_inline_children(node, ctx)
        text = normalize_readable_text(inner.text)
        if text:
            text += "\n\n"
        return RenderResult(
            html=wrap_tag("div", inner.html, {"class": " ".join(sorted(classes))}),
            text=text,
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    if node.name == "div" and "questionWidget-calculatorInstructions" in classes:
        inner = render_inline_children(node, ctx)
        text = normalize_readable_text(inner.text)
        text = f"Calculator required: {text}\n\n" if text else ""
        return RenderResult(
            html=wrap_tag("div", inner.html, {"class": "calculator-instructions"}),
            text=text,
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    if node.name == "div" and classes.intersection(INLINE_DIV_CLASSES):
        inner = render_inline(node, ctx)
        text = normalize_readable_text(inner.text)
        return RenderResult(
            html=wrap_tag("div", inner.html, {"class": " ".join(sorted(classes))}),
            text=f"{text}\n\n" if text else "",
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    if node.name in {"div", "section", "article"}:
        inner = render_block_children(node, ctx)
        return RenderResult(
            html=wrap_tag(node.name, inner.html, {"class": " ".join(sorted(classes))}) if inner.html else "",
            text=inner.text,
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    if node.name == "img":
        rendered = render_image(node)
        rendered.text = normalize_readable_text(rendered.text) + "\n\n"
        return rendered

    if node.name.startswith("mjx-") or node.name in {"math", "svg"}:
        inner = render_inline(node, ctx)
        return RenderResult(
            html=wrap_tag("p", inner.html) if inner.html else "",
            text=f"{normalize_readable_text(inner.text)}\n\n" if inner.text else "",
            images=inner.images,
            free_entry_blanks=inner.free_entry_blanks,
            select_lists=inner.select_lists,
        )

    inner = render_block_children(node, ctx)
    return RenderResult(
        html=inner.html,
        text=inner.text,
        images=inner.images,
        free_entry_blanks=inner.free_entry_blanks,
        select_lists=inner.select_lists,
    )


def fragment_from_container(node: Tag | None, ctx: ItemContext) -> dict[str, Any]:
    if node is None:
        return {
            "normalized_html": "",
            "readable_text": "",
            "images": [],
            "free_entry_blanks": [],
            "select_lists": [],
        }
    if node.name in {"div", "section", "article", "td", "th"}:
        rendered = render_block_children(node, ctx)
    else:
        rendered = render_block(node, ctx)
    return {
        "normalized_html": normalize_html_fragment(rendered.html),
        "readable_text": normalize_readable_text(rendered.text),
        "images": dedupe_dict_rows(rendered.images, ("src",)),
        "free_entry_blanks": dedupe_dict_rows(rendered.free_entry_blanks, ("index", "dom_id")),
        "select_lists": dedupe_dict_rows(rendered.select_lists, ("index", "dom_id")),
    }


def build_section_links(soup: BeautifulSoup) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, anchor in enumerate(soup.select("#sectionLinks .sectionLink"), start=1):
        dom_id = (anchor.get("id") or "").strip()
        rows.append(
            {
                "index": index,
                "step_id": (anchor.get("stepid") or anchor.get("stepId") or "").strip(),
                "dom_id": dom_id,
                "name": (anchor.get("name") or "").strip(),
                "title": anchor.get_text(" ", strip=True),
                "selector": f"#{dom_id}" if dom_id else "",
            }
        )
    return rows


def build_topic_prerequisites(soup: BeautifulSoup) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for anchor in soup.select("#sidebar .prerequisiteLink"):
        href = anchor.get("href", "")
        rows.append(
            {
                "topic_id": extract_topic_id_from_href(href),
                "name": anchor.get_text(" ", strip=True),
                "href": href,
            }
        )
    return rows


def build_key_prerequisites(node: Tag) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for prerequisite in node.select(".keyPrerequisite"):
        anchor = prerequisite.find("a")
        href = anchor.get("href", "") if anchor else ""
        prereq_type_node = prerequisite.select_one(".keyPrerequisiteType")
        prereq_type = normalize_ws(prereq_type_node.get_text(" ", strip=True)) if prereq_type_node else ""
        rows.append(
            {
                "topic_id": extract_topic_id_from_href(href),
                "name": anchor.get_text(" ", strip=True) if anchor else normalize_ws(prerequisite.get_text(" ", strip=True)),
                "href": href,
                "type": prereq_type,
            }
        )
    return rows


def classify_step_section(node: Tag) -> str:
    classes = set(node.get("class", []))
    if "graphic" in classes:
        return "graphic"
    if "exampleQuestion" in classes:
        return "example_question"
    if "exampleExplanation" in classes:
        return "example_explanation"
    if "stepText" in classes:
        return "content"
    return "content"


def section_label(section_type: str) -> str:
    labels = {
        "graphic": "Graphic",
        "example_question": "Example Prompt",
        "example_explanation": "Explanation",
        "content": "Content",
        "prompt": "Prompt",
        "body": "Body",
        "calculator_instructions": "Calculator Instructions",
        "question_graphic": "Question Graphic",
    }
    return labels.get(section_type, section_type.replace("_", " ").title())


def build_step_item(lesson_index: int, step_index: int, node: Tag) -> dict[str, Any]:
    ctx = ItemContext()

    dom_id = (node.get("id") or "").strip()
    step_id = (node.get("stepid") or node.get("stepId") or dom_id.replace("step-", "")).strip()
    step_type = (node.get("steptype") or node.get("stepType") or "step").strip().lower()
    content_id = (node.get("contentid") or node.get("contentId") or "").strip()

    anchor = node.select_one(".stepAnchor")
    step_anchor = (anchor.get("name") or "").strip() if anchor else ""
    title = anchor.get_text(" ", strip=True) if anchor else ""

    sections: list[dict[str, Any]] = []
    for child in node.find_all(recursive=False):
        classes = set(child.get("class", []))
        if child.name in IGNORED_TAGS:
            continue
        if classes.intersection({"stepHeader", "keyPrerequisites"}):
            continue
        fragment = fragment_from_container(child, ctx)
        if not any(
            [
                fragment["normalized_html"],
                fragment["readable_text"],
                fragment["images"],
                fragment["free_entry_blanks"],
                fragment["select_lists"],
            ]
        ):
            continue
        section_type = classify_step_section(child)
        sections.append(
            {
                "section_type": section_type,
                **fragment,
            }
        )

    key_prerequisites = build_key_prerequisites(node)
    meta = merge_meta(*sections)

    readable_parts: list[str] = []
    for section in sections:
        if section["readable_text"]:
            readable_parts.append(f"{section_label(section['section_type'])}:\n{section['readable_text']}")

    readable_text = "\n\n".join(part for part in readable_parts if part).strip()

    return {
        "lesson_index": lesson_index,
        "step_index": step_index,
        "item_type": "step",
        "step_type": step_type,
        "step_id": step_id,
        "content_id": content_id,
        "dom_id": dom_id,
        "selector": f"#{dom_id}" if dom_id else "",
        "step_anchor": step_anchor,
        "title": title,
        "key_prerequisites": key_prerequisites,
        "has_content_in_snapshot": bool(sections),
        "sections": sections,
        "images": meta["images"],
        "free_entry_blanks": meta["free_entry_blanks"],
        "select_lists": meta["select_lists"],
        "readable_text": readable_text,
    }


def classify_choice_content(cell: Tag, fragment: dict[str, Any]) -> str:
    has_image = bool(cell.find("img"))
    has_nested_table = bool(cell.find("table"))
    residual_text = strip_placeholders(fragment["readable_text"])

    if has_nested_table:
        return "nested-table"
    if has_image and residual_text:
        return "mixed"
    if has_image:
        return "image"
    return "text"


def build_question_item(lesson_index: int, question_index: int, node: Tag) -> dict[str, Any]:
    ctx = ItemContext()

    dom_id = (node.get("id") or "").strip()
    question_id = dom_id.replace("question-", "").strip()
    title_node = node.select_one(".questionWidget-title")
    title = title_node.get_text(" ", strip=True) if title_node else ""

    graphic = fragment_from_container(node.select_one(".questionWidget-graphic"), ctx)
    calculator = fragment_from_container(node.select_one(".questionWidget-calculatorInstructions"), ctx)
    prompt = fragment_from_container(node.select_one(".questionWidget-text"), ctx)
    body = fragment_from_container(node.select_one(".questionWidget-body"), ctx)

    choices: list[dict[str, Any]] = []
    for choice_index, row in enumerate(node.select(".questionWidget-choicesTable > tbody > tr, .questionWidget-choicesTable > tr"), start=1):
        letter = row.select_one(".questionWidget-choiceLetterCircle")
        label = letter.get_text(" ", strip=True) if letter else ""
        letter_dom_id = (letter.get("id") or "").strip() if letter else ""
        choice_cell = row.select_one(".questionWidget-choiceText")
        fragment = fragment_from_container(choice_cell, ctx)
        choices.append(
            {
                "choice_index": choice_index,
                "label": label,
                "dom_id": letter_dom_id,
                "content_type": classify_choice_content(choice_cell or row, fragment),
                **fragment,
            }
        )

    question_format = "unknown"
    if choices:
        question_format = "multiple-choice"
    elif prompt["select_lists"] or body["select_lists"]:
        question_format = "select-list"
    elif prompt["free_entry_blanks"] or body["free_entry_blanks"]:
        question_format = "free-response"

    meta = merge_meta(graphic, calculator, prompt, body, *choices)

    has_content_in_snapshot = any(
        [
            graphic["normalized_html"],
            calculator["normalized_html"],
            prompt["normalized_html"],
            body["normalized_html"],
            choices,
        ]
    )

    readable_parts: list[str] = []
    if graphic["readable_text"]:
        readable_parts.append(f"{section_label('question_graphic')}:\n{graphic['readable_text']}")
    if calculator["readable_text"]:
        readable_parts.append(f"{section_label('calculator_instructions')}:\n{calculator['readable_text']}")
    if prompt["readable_text"]:
        readable_parts.append(f"{section_label('prompt')}:\n{prompt['readable_text']}")
    if body["readable_text"]:
        readable_parts.append(f"{section_label('body')}:\n{body['readable_text']}")
    if choices:
        choice_lines = [
            f"{choice['label'] or choice['choice_index']}. {choice['readable_text']}".strip()
            for choice in choices
        ]
        readable_parts.append("Choices:\n" + "\n".join(choice_lines))
    if not has_content_in_snapshot:
        readable_parts.append(
            "Content:\n(not present in this saved HTML snapshot; likely expected client-side hydration)"
        )

    readable_text = "\n\n".join(part for part in readable_parts if part).strip()

    return {
        "lesson_index": lesson_index,
        "question_index": question_index,
        "item_type": "question",
        "question_id": question_id,
        "dom_id": dom_id,
        "selector": f"#{dom_id}" if dom_id else "",
        "title": title,
        "question_number": parse_question_number(title),
        "question_format": question_format,
        "choice_count": len(choices),
        "has_content_in_snapshot": has_content_in_snapshot,
        "hydration_required": not has_content_in_snapshot,
        "graphic": graphic,
        "calculator_instructions": calculator,
        "prompt": prompt,
        "body": body,
        "choices": choices,
        "images": meta["images"],
        "free_entry_blanks": meta["free_entry_blanks"],
        "select_lists": meta["select_lists"],
        "readable_text": readable_text,
    }


def build_unknown_item(lesson_index: int, node: Tag) -> dict[str, Any]:
    ctx = ItemContext()
    dom_id = (node.get("id") or "").strip()
    fragment = fragment_from_container(node, ctx)
    return {
        "lesson_index": lesson_index,
        "item_type": "unknown",
        "dom_id": dom_id,
        "selector": f"#{dom_id}" if dom_id else "",
        **fragment,
    }


def build_lesson_items(soup: BeautifulSoup) -> list[dict[str, Any]]:
    lesson_content = soup.select_one("#lessonContent")
    if lesson_content is None:
        return []

    children = [child for child in lesson_content.find_all(recursive=False) if getattr(child, "name", None)]
    items: list[dict[str, Any]] = []
    step_index = 0
    question_index = 0

    for lesson_index, node in enumerate(children, start=1):
        dom_id = (node.get("id") or "").strip()
        if dom_id.startswith("step-") and "questionWidget" not in (node.get("class") or []):
            step_index += 1
            items.append(build_step_item(lesson_index, step_index, node))
        elif dom_id.startswith("question-"):
            question_index += 1
            items.append(build_question_item(lesson_index, question_index, node))
        else:
            items.append(build_unknown_item(lesson_index, node))

    return items


def build_lesson_readable_text(items: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    for item in items:
        if item["item_type"] == "step":
            heading = f"Item {item['lesson_index']} — {item.get('step_type', 'step').title()}"
            if item.get("title"):
                heading = f"{heading}: {item['title']}"
        elif item["item_type"] == "question":
            heading = f"Item {item['lesson_index']} — {item.get('title') or 'Question'}"
        else:
            heading = f"Item {item['lesson_index']} — Unknown"

        body = item.get("readable_text", "").strip()
        if body:
            chunks.append(f"{heading}\n\n{body}")
        else:
            chunks.append(heading)

    return "\n\n---\n\n".join(chunks).strip()


def build_lesson_json(html_path: Path) -> dict[str, Any]:
    topic_id = html_path.stem
    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")

    topic_name_node = soup.select_one("#topicName")
    topic_title = topic_name_node.get_text(" ", strip=True) if topic_name_node else ""

    section_links = build_section_links(soup)
    topic_prerequisites = build_topic_prerequisites(soup)
    lesson_items = build_lesson_items(soup)

    return {
        "schema_version": 2,
        "topic_id": topic_id,
        "topic_title": topic_title,
        "source_html": str(html_path),
        "source_url": f"https://mathacademy.com/topics/{topic_id}",
        "normalization": {
            "math_placeholder": "[MATH: ...]",
            "image_placeholder": "[IMG: /graphics/...]",
            "free_entry_placeholder": "[FREE_ENTRY n]",
            "select_placeholder": "[SELECT n]",
        },
        "toc": {
            "sidebar_selector": "#sidebar",
            "section_links_selector": "#sectionLinks .sectionLink",
            "section_links": section_links,
            "topic_prerequisites": topic_prerequisites,
        },
        "lesson": {
            "container_selector": "#lessonContent",
            "item_count": len(lesson_items),
            "step_count": sum(1 for item in lesson_items if item.get("item_type") == "step"),
            "question_count": sum(1 for item in lesson_items if item.get("item_type") == "question"),
            "items": lesson_items,
            "readable_text": build_lesson_readable_text(lesson_items),
        },
    }


def write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.stem}.tmp{path.suffix}")
    temp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    os.replace(temp_path, path)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    lessons_root = args.lessons_root.expanduser().resolve()
    jobs = select_jobs(args, lessons_root)
    interactive_progress = not args.no_progress and sys.stderr.isatty()

    if not jobs:
        progress_write("No pending lesson HTML files found.")
        return 0

    if args.dry_run:
        print(f"Dry run: would build {len(jobs)} lesson JSON file(s).")
        for job in jobs[:10]:
            print(f"  {job.topic_id}: {job.html_path} -> {job.json_path}")
        if len(jobs) > 10:
            print(f"  ... and {len(jobs) - 10} more")
        return 0

    written = 0
    failures: list[str] = []
    progress = progress_bar(
        total=len(jobs),
        desc="Lesson JSON",
        unit="lesson",
        disable=not interactive_progress,
    )

    try:
        for job in jobs:
            try:
                payload = build_lesson_json(job.html_path)
                write_json_atomic(job.json_path, payload)
                written += 1
            except Exception as exc:
                failures.append(job.topic_id)
                progress_write(f"topic {job.topic_id} failed: {exc}")
            finally:
                progress.update(1)
                progress.set_postfix(written=written, failed=len(failures))
    finally:
        progress.close()

    if failures:
        progress_write(
            f"Lesson JSON complete: attempted={len(jobs)} written={written} failed={len(failures)}"
        )
        progress_write(f"Failed topics: {', '.join(failures)}")
        return 1

    progress_write(f"Lesson JSON complete: attempted={len(jobs)} written={written} failed=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
