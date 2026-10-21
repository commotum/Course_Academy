"""Repair the two lossless, structured brace-accent import errors.

Only `_ {brace glyph}` (without the space) attached to a balanced TeX
group, and `\\overset{overbrace glyph}{balanced group}`, are recognized.
Balanced groups are parsed, including escaped braces and nested commands.
Labels are moved from the importer's redundant wrappers onto the accent.
Flattened Word/linear-math notation is deliberately left for source-backed
reconstruction by the separate flattened repair.

No source text, mathematical base, label, surrounding group, or whitespace
is rewritten except the explicitly recognized decoration wrappers.  Each
result carries a reversible provenance tree and an occurrence-level record.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Union


@dataclass
class Text:
    value: str

    def old(self) -> str:
        return self.value

    def new(self) -> str:
        return self.value


@dataclass
class Group:
    children: list["Node"]

    def old(self) -> str:
        return "{" + old(self.children) + "}"

    def new(self) -> str:
        return "{" + new(self.children) + "}"


@dataclass
class Accent:
    direction: str
    base: list["Node"]
    original: str
    label: list["Node"] | None = None
    label_style: str | None = None
    wrapper_spaces: str = ""

    def old(self) -> str:
        return self.original

    def new(self) -> str:
        # wrapper_spaces can only consist of ignorable TeX whitespace; retain
        # it before the brace rather than silently dropping any source bytes.
        result = self.wrapper_spaces + "\\" + self.direction + "brace{" + new(self.base) + "}"
        if self.label is not None:
            result += ("_" if self.direction == "under" else "^") + "{" + new(self.label) + "}"
        return result


Node = Union[Text, Group, Accent]


def old(nodes: list[Node]) -> str:
    return "".join(node.old() for node in nodes)


def new(nodes: list[Node]) -> str:
    return "".join(node.new() for node in nodes)


def parse(text: str) -> list[Node]:
    """Parse only braces/commands; preserve everything else byte for byte.

    Unmatched braces are retained as text, because a full Markdown field can
    contain literal braces outside its TeX fragments.  An accent can consume
    only a successfully matched Group, never those unmatched braces.
    """
    def sequence(i: int, grouped: bool = False) -> tuple[list[Node], int, bool]:
        nodes: list[Node] = []
        while i < len(text):
            char = text[i]
            if char == "\\":
                match = re.match(r"\\(?:[A-Za-z]+|.)", text[i:], re.S)
                value = match.group(0) if match else "\\"
                nodes.append(Text(value))
                i += len(value)
            elif char == "{":
                children, end, closed = sequence(i + 1, True)
                if closed:
                    nodes.append(Group(children))
                else:
                    nodes.append(Text("{"))
                    nodes.extend(children)
                i = end
            elif char == "}" and grouped:
                return nodes, i + 1, True
            else:
                nodes.append(Text(char))
                i += 1
        return nodes, i, False
    nodes, _, _ = sequence(0)
    assert old(nodes) == text
    return nodes


def literal(node: Node, value: str) -> bool:
    return isinstance(node, Text) and node.value == value


def pure_accent(node: Node, direction: str) -> tuple[Accent, str] | None:
    """Find an unlabelled accent inside only redundant grouping/whitespace."""
    whitespace = ""
    while isinstance(node, Group):
        substantive = [child for child in node.children
                       if not (isinstance(child, Text) and child.value.isspace())]
        if len(substantive) != 1:
            return None
        whitespace += "".join(child.value for child in node.children
                              if isinstance(child, Text) and child.value.isspace())
        node = substantive[0]
    if isinstance(node, Accent) and node.direction == direction and node.label is None:
        return node, whitespace
    return None


def rewrite(nodes: list[Node], counts: Counter) -> list[Node]:
    # Recursive descent ensures accents in either bases or labels retain their
    # original scopes before an enclosing accent is repaired.
    nodes = [Group(rewrite(node.children, counts)) if isinstance(node, Group) else node
             for node in nodes]
    i = 0
    while i < len(nodes):
        # MathML munder(base, brace glyph) was wrongly serialized as a subscript.
        if (i + 2 < len(nodes) and isinstance(nodes[i], Group)
                and literal(nodes[i + 1], "_") and isinstance(nodes[i + 2], Group)
                and old(nodes[i + 2].children) == "⏟"):
            consumed = nodes[i:i + 3]
            node = Accent("under", nodes[i].children, old(consumed))
            nodes[i:i + 3] = [node]
            counts["underbrace"] += 1
            continue

        # MathML mover(base, brace glyph) was wrongly serialized as overset.
        if (i + 2 < len(nodes) and literal(nodes[i], r"\overset")
                and isinstance(nodes[i + 1], Group) and isinstance(nodes[i + 2], Group)
                and old(nodes[i + 1].children) == "⏞"):
            consumed = nodes[i:i + 3]
            node = Accent("over", nodes[i + 2].children, old(consumed))
            nodes[i:i + 3] = [node]
            counts["overbrace"] += 1
            continue

        # Move a label on a redundant outer group to the underbrace itself.
        # This matters: {\underbrace{BASE}}_{label} would put the label right.
        if (i + 2 < len(nodes) and literal(nodes[i + 1], "_")
                and isinstance(nodes[i + 2], Group)):
            match = pure_accent(nodes[i], "under")
            if match:
                accent, whitespace = match
                nodes[i:i + 3] = [Accent("under", accent.base, old(nodes[i:i + 3]),
                                         nodes[i + 2].children, "subscript",
                                         accent.wrapper_spaces + whitespace)]
                counts["underbrace_labels"] += 1
                continue

        # The mover label is outside the brace glyph's mover.  Preserve that
        # association by making it a centered overbrace annotation.
        if (i + 2 < len(nodes) and isinstance(nodes[i + 1], Group)
                and isinstance(nodes[i + 2], Group)
                and (literal(nodes[i], r"\overset") or literal(nodes[i], r"\underset"))):
            direction = "over" if literal(nodes[i], r"\overset") else "under"
            match = pure_accent(nodes[i + 2], direction)
            if match:
                accent, whitespace = match
                nodes[i:i + 3] = [Accent(direction, accent.base, old(nodes[i:i + 3]),
                                         nodes[i + 1].children,
                                         "overset" if direction == "over" else "underset",
                                         accent.wrapper_spaces + whitespace)]
                counts[direction + "brace_labels"] += 1
                continue
        i += 1
    return nodes


def occurrence_evidence(nodes: list[Node]) -> list[dict]:
    rows: list[dict] = []
    for node in nodes:
        if isinstance(node, Group):
            rows.extend(occurrence_evidence(node.children))
        elif isinstance(node, Accent):
            rows.append({
                "direction": node.direction,
                "before": node.old(), "after": node.new(),
                "base_before": old(node.base), "base_after": new(node.base),
                "label_before": None if node.label is None else old(node.label),
                "label_after": None if node.label is None else new(node.label),
                "label_style": node.label_style,
                "base_and_label_preserved_except_nested_accent_repairs": True,
            })
            rows.extend(occurrence_evidence(node.base))
            if node.label is not None:
                rows.extend(occurrence_evidence(node.label))
    return rows


def transform(text: str) -> tuple[str, dict]:
    """Return repaired text and JSON-serializable counts/provenance evidence."""
    counts: Counter = Counter()
    nodes = rewrite(parse(text), counts)
    result = new(nodes)
    # old() walks the provenance tree after every substitution and promotion;
    # it must reconstruct the entire source exactly, including unaffected text.
    assert old(nodes) == text, "Transformation lost original source content"
    occurrences = occurrence_evidence(nodes)
    assert len(occurrences) == counts["underbrace"] + counts["overbrace"]
    assert result.count("_{⏟}") == text.count("_{⏟}") - counts["underbrace"]
    assert result.count(r"\overset{⏞}") == text.count(r"\overset{⏞}") - counts["overbrace"]
    return result, {"counts": dict(counts), "exact_source_reconstruction": True,
                    "occurrences": occurrences}


def main() -> None:
    here = Path(__file__).resolve().parent
    # The canonical path is relative to edb-math, not the repair itself.
    source = here.parents[2] / "audits/2026-10-17-underbrace-import/current-affected.json"
    rows = json.loads(source.read_text())
    changes = []
    totals: Counter = Counter()
    for row in rows:
        result, evidence = transform(row["value"])
        if result != row["value"]:
            totals.update(evidence["counts"])
            changes.append({"entity": row["entity"], "attribute": row["attribute"],
                            "before": row["value"], "after": result, "evidence": evidence})
    (here / "changes.json").write_text(json.dumps(changes, ensure_ascii=False, indent=2) + "\n")
    summary = {"fields": len(changes), "entities": len({x["entity"] for x in changes}),
               "counts": dict(totals), "exact_source_reconstruction": True,
               "flattened_variants_unchanged": True}
    (here / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
