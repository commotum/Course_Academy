"""Prepare the 18 authorized follow-up solution fixes from planned committed values."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
source = ROOT / "mapped-cases.json"
audit_source = OUT / "relation-brace-pattern-audit.json"
source_data = json.loads(source.read_text())
mapped = {case["question"]: case for case in source_data["cases"]}
audit = json.loads(audit_source.read_text())
held = {17592186188925, 17592186366455}
cases = []
for entry in audit["matches"]:
    eid = entry["question_eid"]
    if eid in held:
        continue
    prior = mapped[eid]
    before = copy.deepcopy(prior["after"])
    after = copy.deepcopy(before)
    attr = entry["attribute"]
    for span in entry["math_spans"]:
        assert before[attr].count(span["before"]) == 1, eid
        after[attr] = after[attr].replace(span["before"], span["after"], 1)
    assert after[attr] != before[attr]
    case = {
        "question": eid,
        "before": before,
        "after": after,
        "objects": copy.deepcopy(prior["objects"]),
        "method": "theorem_relation_literal_brace_repair",
        "provenance": {
            "baseline_kind": "planned_post_checkbox_values",
            "baseline_source": str(source.relative_to(ROOT)),
            "baseline_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "guard": "run_batch must refresh authoritative current basis and require exact old solution bytes before transacting",
            "attribute": attr,
            "source_fragment_replacements": entry["math_spans"],
            "reason": "The literal brace before the aligned equivalent conditions was imported as an unmatched raw TeX group. Escaping and sizing this brace restores recognition of the inline math without changing the conditions.",
        },
    }
    cases.append(case)
assert len(cases) == 18
out = OUT / "relation-brace-supplement-cases.json"
out.write_text(json.dumps({"cases": cases}, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"questions": len(cases), "output": str(out), "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}))
