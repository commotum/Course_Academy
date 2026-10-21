"""Record exact guarded relation-brace math-span repairs, without DB writes."""
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PATTERN = re.compile(r"\$\\,⟺\\,\{\\,\\begin\{aligned\}[^$]+?\\end\{aligned\}\$")


def spans(solution):
    result = []
    for match in PATTERN.finditer(solution):
        before = match.group()
        after = before.replace(r"⟺\,{\,\begin{aligned}", r"⟺\,\left\{\,\begin{aligned}", 1)
        after = after[:-1] + r"\right." + "$"
        result.append({"before": before, "after": after})
    return result


def dump(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


source = ROOT / "mapping/final-cases.json"
cases = json.loads(source.read_text())["cases"]
repairs = []
render_cases = []
for case in cases:
    found = spans(case["after"][":question/worked-solution"])
    if not found:
        continue
    assert case["question"] in {17592186188925, 17592186366455}
    assert len(found) == 1
    repaired = copy.deepcopy(case)
    for span in found:
        assert repaired["after"][":question/worked-solution"].count(span["before"]) == 1
        repaired["after"][":question/worked-solution"] = repaired["after"][":question/worked-solution"].replace(span["before"], span["after"], 1)
    repairs.append({
        "question_eid": case["question"],
        "attribute": ":question/worked-solution",
        "math_spans": found,
        "expected_count_per_span": 1,
        "reason": "Restore the literal opening brace for the aligned equivalent conditions, paired with an invisible right delimiter. The unmatched raw brace prevented recognition of the entire inline math span.",
    })
    render_cases.append(repaired)
assert len(repairs) == 2
dump("relation-brace-overrides.json", repairs)
dump("relation-brace-cases.json", {"cases": render_cases})
original = json.loads((ROOT / "questions.json").read_text())
audit = [{"question_eid": q[":db/id"], "attribute": ":question/worked-solution", "math_spans": spans(q.get(":question/worked-solution", ""))} for q in original if spans(q.get(":question/worked-solution", ""))]
dump("relation-brace-pattern-audit.json", {"source": str(ROOT / "questions.json"), "source_sha256": hashlib.sha256((ROOT / "questions.json").read_bytes()).hexdigest(), "count": len(audit), "matches": audit, "note": "Original snapshot audit; obtain current committed values for non-held questions before applying."})
print(json.dumps({"held_cases": len(repairs), "original_snapshot_matches": len(audit)}))
