#!/usr/bin/env python3
"""Flag possible synthetic-prose hotspots without declaring authorship."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


RULES: tuple[tuple[str, str, str], ...] = (
    ("importance", r"\b(?:pivotal|crucial|key|vital|testament|underscores?|highlights?)\b", "Replace asserted importance with a concrete consequence."),
    ("promotion", r"\b(?:vibrant|renowned|remarkable|groundbreaking|profound|robust|intuitive|world[- ]class)\b", "Check that the evaluation is sourced, defined, evidenced, or genre-appropriate."),
    ("vague-attribution", r"\b(?:experts?|observers?|critics?|researchers?)\s+(?:believe|say|argue|note|suggest|have)|\b(?:research suggests|widely (?:regarded|considered|believed))\b", "Name and scope the source; do not imply unsupported consensus."),
    ("ceremonial-verb", r"\b(?:serves as|stands as|boasts|utili[sz]es|authored|commenced|facilitated)\b", "Test a more direct verb without changing meaning."),
    ("dense-abstraction", r"\b(?:intricate interplay|evolving landscape|tapestry|ecosystem|fostering innovation|enhancing efficiency|delves? into)\b", "Name the actors, actions, variables, rules, or measurements."),
    ("trailing-significance", r",\s+(?:highlighting|underscoring|demonstrating|reflecting|reinforcing|showcasing|solidifying|contributing to)\b", "Check whether the trailing clause adds evidence or merely restates significance."),
    ("formulaic-contrast", r"\b(?:not only\b.{0,100}\bbut also|not merely\b.{0,100}\b(?:but|it is)|more than just|not\b.{0,80}\bbut rather)\b", "Use the contrast only when it corrects a real misconception."),
    ("canned-outlook", r"\b(?:despite (?:these|ongoing) challenges|future (?:prospects|outlook).{0,40}(?:promising|bright)|full potential|continued innovation and collaboration)\b", "Replace a symmetrical outlook with a supported result or unresolved question."),
    ("assistant-artifact", r"(?:\bCertainly!|\bHere is (?:a|an|the) (?:revised|updated)\b|\bI hope this helps\b|\bLet me know if\b|\bWould you like me to\b|\bAs of my last update\b|\bBased on the information provided\b)", "Remove drafting-conversation language from the finished artifact."),
    ("placeholder", r"\[(?:Company Name|Specific Example|Insert (?:source|citation|text)[^\]]*)\]|\b202X-XX-XX\b|\b(?:TODO|TBD|PLACEHOLDER)\b", "Resolve or explicitly retain the placeholder; do not ship it accidentally."),
)


def scan(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        for rule, pattern, advice in RULES:
            matches = [match.group(0) for match in re.finditer(pattern, line, re.IGNORECASE)]
            if matches:
                findings.append(
                    {
                        "line": line_no,
                        "rule": rule,
                        "matches": matches,
                        "advice": advice,
                        "text": line.strip(),
                    }
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="UTF-8 text or Markdown file to scan")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    try:
        text = args.file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"error: cannot read {args.file}: {error}", file=sys.stderr)
        return 2

    findings = scan(text)
    if args.json:
        print(json.dumps({"file": str(args.file), "findings": findings}, indent=2))
        return 0

    if not findings:
        print(f"No lexical hotspots found in {args.file}.")
        print("A semantic and structural audit is still required.")
        return 0

    for item in findings:
        matches = ", ".join(repr(value) for value in item["matches"])
        print(f"{args.file}:{item['line']}: [{item['rule']}] {matches}")
        print(f"  {item['advice']}")
        print(f"  {item['text']}")
    print(f"\n{len(findings)} hotspot(s). Treat these as review leads, not proof of authorship.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
