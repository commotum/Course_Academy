"""Independent verifier of exact base, annotation, and unaffected-text retention.

This reads the proposed evidence without importing or executing the repair
implementation.  Its accepted input grammar is the three exact forms that
occur in the audited corpus.  Nested changes must themselves be among those
verified exact forms; all other text is copied byte-for-byte.
"""
from collections import Counter
import json
from pathlib import Path


def replay(text, replacements):
    result = []
    i = 0
    by_first = {}
    for before, after in sorted(replacements.items(), key=lambda x: -len(x[0])):
        by_first.setdefault(before[0], []).append((before, after))
    while i < len(text):
        for before, after in by_first.get(text[i], []):
            if text.startswith(before, i):
                result.append(after)
                i += len(before)
                break
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def main():
    here = Path(__file__).resolve().parent
    changes = json.loads((here / "changes.json").read_text())
    totals = Counter()
    for row in changes:
        mapping = {}
        for item in row["evidence"]["occurrences"]:
            base, label, direction = item["base_before"], item["label_before"], item["direction"]
            if direction == "under":
                expected = "{" + base + "}_{⏟}"
                if label is not None:
                    expected = "{" + expected + "}_{" + label + "}"
            else:
                expected = r"\overset{⏞}{" + base + "}"
                if label is not None:
                    expected = r"\overset{" + label + "}{" + expected + "}"
            assert expected == item["before"], (row["entity"], "wrong base/label extraction", item)
            expected = "\\" + direction + "brace{" + item["base_after"] + "}"
            if label is not None:
                expected += ("_" if direction == "under" else "^") + "{" + item["label_after"] + "}"
            assert expected == item["after"], (row["entity"], "wrong repaired annotation", item)
            assert mapping.setdefault(item["before"], item["after"]) == item["after"]
            totals[direction + "brace"] += 1
            totals[direction + "brace_labeled" if label is not None else direction + "brace_unlabeled"] += 1
        for item in row["evidence"]["occurrences"]:
            assert replay(item["base_before"], mapping) == item["base_after"], (row["entity"], "base changed")
            if item["label_before"] is not None:
                assert replay(item["label_before"], mapping) == item["label_after"], (row["entity"], "label changed")
        assert replay(row["before"], mapping) == row["after"], (row["entity"], "unrelated text changed")
        for token in ("_(⏟)", "^(⏞)", "$", "[math]", "[/math]"):
            assert row["before"].count(token) == row["after"].count(token), (row["entity"], token)
        assert "_{⏟}" not in row["after"]
        assert r"\overset{⏞}" not in row["after"]
    result = {"passed": True, "verified_fields": len(changes), "counts": dict(totals),
              "exact_scope_and_labels_preserved": True,
              "all_unrelated_content_preserved_byte_for_byte": True,
              "verification_does_not_import_repair_implementation": True}
    (here / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
