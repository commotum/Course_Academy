"""Repair the six current visible checkbox piecewise braces, without DB writes."""
import copy
import hashlib
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SOURCE = ROOT / "final-census/questions.json"
IDS = {17592186152823, 17592186152826, 17592186265782, 17592186265784, 17592186265785, 17592186407296}
SPAN = re.compile(r"(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\$(?!\$)[\s\S]*?(?<!\\)\$(?!\$)")
rows = json.loads(SOURCE.read_text())
cases = []
for before in rows:
    eid = before[":db/id"]
    if eid not in IDS:
        continue
    after = copy.deepcopy(before)
    replacements = {}
    objects = []
    for index, field in enumerate(after[":question/answer-fields"]):
        key = field[":answer-field/key"]
        assert key.startswith(r"${\begin{aligned}") and key.endswith(r"\end{aligned}$"), (eid, key)
        fixed = r"$\left\{" + key[2:-1] + r"\right.$"
        assert fixed.replace(r"\left\{", "{", 1).replace(r"\right.", "", 1) == key
        field[":answer-field/key"] = fixed
        replacements[key] = fixed
        objects.append({
            "source_label": ["I", "II", "III"][index],
            "field_id": field[":db/id"],
            "content": fixed,
            "source_fragment": key,
            "repair": "Restore the literal opening piecewise brace and pair it with an invisible right delimiter; preserve every expression and condition.",
        })
    assert len(objects) == len(replacements) == 3
    counts = {old: 0 for old in replacements}
    def replace_match(match):
        span = match.group()
        if span in replacements:
            counts[span] += 1
            return replacements[span]
        return span
    after[":question/worked-solution"] = SPAN.sub(replace_match, before[":question/worked-solution"])
    assert all(counts.values()), (eid, counts)
    assert after[":question/problem"] == before[":question/problem"]
    cases.append({
        "question": eid,
        "before": before,
        "after": after,
        "objects": objects,
        "method": "current_piecewise_checkbox_literal_brace_repair",
        "provenance": {
            "baseline_source": "final-census/questions.json",
            "baseline_source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "source_basis": 3771,
            "solution_reference_replacements": [{"before": old, "after": new, "count": counts[old]} for old, new in replacements.items()],
            "solution_guard": "Only complete isolated inline math spans matching a current checkbox key were replaced; display blocks were skipped.",
        },
    })
assert len(cases) == 6
path = OUT / "cases.json"
path.write_text(json.dumps({"cases": cases}, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"questions": len(cases), "fields": sum(len(c["objects"]) for c in cases), "solution_references": sum(r["count"] for c in cases for r in c["provenance"]["solution_reference_replacements"]), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}))
