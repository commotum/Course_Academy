"""Verify each structured edit independently of the repair implementation."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
changes = json.loads((HERE / "changes.json").read_text())
counts = Counter()
for row in changes:
    replay = row["before"]
    for proof in sorted(row["proofs"], key=lambda value: -value["start"]):
        # The actual corpus has one exact import spelling and no nested hats.
        # Enforce this simple independent grammar instead of importing its parser.
        assert proof["before"] == r"\overset{^}{" + proof["base"] + "}"
        assert proof["base_after"] == proof["base"]
        command = proof["width_source"]["command"].lstrip("\\")
        assert command in ("hat", "widehat")
        assert proof["after"] == "\\" + command + "{" + proof["base"] + "}"
        assert replay[proof["start"]:proof["end"]] == proof["before"]
        replay = replay[:proof["start"]] + proof["after"] + replay[proof["end"]:]
        counts[command] += 1
    assert replay == row["after"]
    assert hashlib.sha256(row["before"].encode()).hexdigest() == row["before_sha256"]
    assert hashlib.sha256(row["after"].encode()).hexdigest() == row["after_sha256"]
    assert len(row["proofs"]) == row["structured_occurrences"]
    assert not re.search(r"\\(?:overset|stackrel)\s*\{\s*\^\s*\}", row["after"])
assert len(changes) == 282
assert sum(counts.values()) == 1174
result = {"passed": True, "fields": len(changes), "accent_occurrences": sum(counts.values()),
          "commands": dict(counts), "every_base_preserved_byte_for_byte": True,
          "every_field_replayed_exactly_from_recorded_spans": True,
          "all_other_content_preserved_byte_for_byte": True,
          "verified_without_importing_repair_implementation": True}
(HERE / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
