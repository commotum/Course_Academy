"""Classify malformed hat accents and preserve exact structured base scopes.

No database calls or mutations. Width selection must come from saved source
evidence. Flattened bases require separate source-backed recovery: this module
does not guess where those lost scopes start.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import loads

HERE = Path(__file__).resolve().parent
ATTRIBUTES = {1064: ":tutorial/content", 1071: ":question/problem",
              1074: ":question/worked-solution", 1080: ":answer/value",
              1081: ":answer/feedback", 1085: ":multistep/context"}
FLATTENED = re.compile(r"\^\(\s*[\^ˆ]\s*\)")


def group(text, start):
    """Return (inner text, exclusive end), respecting escaped TeX braces."""
    if start >= len(text) or text[start] != "{":
        return None
    depth = 1
    i = start + 1
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return None


def skip_space(text, i):
    while i < len(text) and text[i].isspace():
        i += 1
    return i


def bare_caret(mark):
    """Permit only whitespace and transparent balanced group wrappers."""
    mark = mark.strip()
    while mark.startswith("{"):
        value = group(mark, 0)
        if value is None or value[1] != len(mark):
            break
        mark = value[0].strip()
    return mark in ("^", "ˆ")


def structured_occurrences(text):
    r"""Find source spans; token scanning distinguishes \\ from \command."""
    result = []
    i = 0
    while i < len(text):
        if text[i] != "\\":
            i += 1
            continue
        match = re.match(r"\\(?:[A-Za-z]+|.)", text[i:], re.S)
        if not match:
            break
        command = match.group(0)
        command_end = i + match.end()
        if command not in (r"\overset", r"\stackrel"):
            i = command_end
            continue
        mark_start = skip_space(text, command_end)
        mark = group(text, mark_start)
        if mark is None or not bare_caret(mark[0]):
            i = command_end
            continue
        base_start = skip_space(text, mark[1])
        base = group(text, base_start)
        if base is None:
            raise ValueError("Bare-caret accent has no balanced base: " + text[i:i + 100])
        result.append({"start": i, "end": base[1], "before": text[i:base[1]],
                       "base": base[0], "base_start": base_start + 1,
                       "base_end": base[1] - 1, "marker": mark[0],
                       "imported_command": command})
        # Scan inside the base too so nested malformed accents are counted.
        i = base_start + 1
    return result


def transform_structured(text, select_width):
    """select_width(occurrence) must return source evidence and command name."""
    proofs = []
    occurrences = structured_occurrences(text)

    def render(start, end):
        output = []
        cursor = start
        for occurrence in occurrences:
            if not (cursor <= occurrence["start"] < end):
                continue
            assert occurrence["end"] <= end
            evidence = select_width(occurrence)
            command = evidence["command"].lstrip("\\")
            assert command in ("hat", "widehat"), command
            output.append(text[cursor:occurrence["start"]])
            base = render(occurrence["base_start"], occurrence["base_end"])
            after = "\\" + command + "{" + base + "}"
            output.append(after)
            proofs.append({**occurrence, "after": after, "base_after": base,
                           "width_source": evidence,
                           "base_preserved_except_nested_hat_repairs": True})
            cursor = occurrence["end"]
        output.append(text[cursor:end])
        return "".join(output)

    after = render(0, len(text))
    assert len(proofs) == len(occurrences)
    assert not structured_occurrences(after)
    # Top-level replacement replay checks all surrounding source bytes.
    cursor = 0
    replay = []
    for proof in sorted(proofs, key=lambda value: value["start"]):
        if proof["start"] < cursor:
            continue
        replay.append(text[cursor:proof["start"]])
        assert text[proof["start"]:proof["end"]] == proof["before"]
        replay.append(proof["after"])
        cursor = proof["end"]
    replay.append(text[cursor:])
    assert "".join(replay) == after
    assert FLATTENED.findall(text) == FLATTENED.findall(after)
    return after, proofs


def inventory():
    rows = []
    seen = set()
    bases = defaultdict(lambda: {"occurrences": 0, "fields": []})
    totals = Counter()
    for path in sorted((HERE / "evidence").glob("current-*.edn")):
        for entity, attribute, value, tx, source, added in loads(path.read_text()):
            assert added and isinstance(value, str)
            key = entity, attribute
            if key in seen:
                continue
            seen.add(key)
            structured = structured_occurrences(value)
            flat = list(FLATTENED.finditer(value))
            if not structured and not flat:
                continue
            row = {"entity": entity, "attribute_id": attribute,
                   "attribute": ATTRIBUTES.get(attribute), "value": value,
                   "structured_occurrences": len(structured),
                   "flattened_occurrences": len(flat)}
            rows.append(row)
            totals["structured_occurrences"] += len(structured)
            totals["flattened_occurrences"] += len(flat)
            for occurrence in structured:
                item = bases[occurrence["base"]]
                item["occurrences"] += 1
                field = [entity, attribute]
                if field not in item["fields"]:
                    item["fields"].append(field)
    rows.sort(key=lambda row: (row["entity"], row["attribute_id"]))
    (HERE / "candidates.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    (HERE / "structured-base-inventory.json").write_text(json.dumps(dict(bases), ensure_ascii=False, indent=2) + "\n")
    summary = {"candidate_fields": len(rows), "candidate_entities": len({row["entity"] for row in rows}),
               "attributes": dict(Counter(row["attribute"] or str(row["attribute_id"]) for row in rows)),
               "structured_fields": sum(bool(row["structured_occurrences"]) for row in rows),
               "flattened_fields": sum(bool(row["flattened_occurrences"]) for row in rows),
               "structured_distinct_bases": len(bases), **totals,
               "answer_values_require_history_preservation": sum(row["attribute_id"] == 1080 for row in rows),
               "changes_prepared": False}
    (HERE / "candidate-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return rows


def prepare(widths_path):
    rows = [row for row in inventory() if row["structured_occurrences"]]
    widths = json.loads(Path(widths_path).read_text())
    changes = []
    commands = Counter()
    for row in rows:
        key = row["entity"], row["attribute_id"]
        before = row["value"]
        after = before
        proofs = []
        assert not row["flattened_occurrences"], "Flattened recovery is a separate source-backed population"
        if row["structured_occurrences"]:
            def select_width(occurrence):
                field_key = str(row["entity"]) + "|" + str(row["attribute_id"]) + "|" + occurrence["base"]
                evidence = widths.get(field_key, widths.get(occurrence["base"]))
                assert evidence is not None, (key, "missing source-width evidence", occurrence["base"])
                assert isinstance(evidence, dict) and evidence.get("command") in ("hat", "widehat", r"\hat", r"\widehat")
                assert len(evidence) > 1, "A width choice must retain its source evidence"
                commands[evidence["command"].lstrip("\\")] += 1
                return evidence
            after, structured_proofs = transform_structured(after, select_width)
            proofs.extend(structured_proofs)
        assert before != after
        assert not FLATTENED.search(after) and not structured_occurrences(after)
        assert before.count("$") == after.count("$")
        assert re.findall(r"!\[[^\]]*\]\([^)]+\)", before) == re.findall(r"!\[[^\]]*\]\([^)]+\)", after)
        changes.append({"entity": row["entity"], "attribute_id": row["attribute_id"],
                        "attribute": row["attribute"], "before": before, "after": after,
                        "structured_occurrences": row["structured_occurrences"],
                        "flattened_occurrences": row["flattened_occurrences"],
                        "repaired_hat_occurrences": row["structured_occurrences"] + row["flattened_occurrences"],
                        "proofs": proofs,
                        "before_sha256": hashlib.sha256(before.encode()).hexdigest(),
                        "after_sha256": hashlib.sha256(after.encode()).hexdigest()})
    output = HERE / "structured"
    output.mkdir(exist_ok=True)
    (output / "changes.json").write_text(json.dumps(changes, ensure_ascii=False, indent=2) + "\n")
    summary = json.loads((HERE / "candidate-summary.json").read_text())
    summary.update({"changes_prepared": True, "changed_fields": len(changes),
                    "structured_commands": dict(commands),
                    "structured_width_evidence": str(Path(widths_path)),
                    "remaining_malformed_hat_occurrences_in_repaired_fields": 0,
                    "proper_existing_hats_left_unchanged": True,
                    "no_database_writes": True})
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--widths")
    args = parser.parse_args()
    if args.widths:
        prepare(args.widths)
    else:
        inventory()
