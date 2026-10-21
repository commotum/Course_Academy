"""Escape source percentages masking fifteen repaired hat derivations.

Only the fifteen aligned-error fields from the hat repair's browser findings
are considered. No other percentages, fields, or importer code are changed.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib
import json
import re
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
REPAIR = HERE.parent
ROOT = REPAIR.parents[3]
SOURCES = {
    17592186161703: "differential/14134349/observations/step-e10362-51ea94370a8229380c53.html",
    17592186162431: "differential/14134349/observations/history-solution-q-146295-1c2de91208cf6859f7a2.html",
    17592186162439: "differential/14234472/observations/history-solution-q-146454-c5d05fdee0e5bf9200dd.html",
    17592186441113: "differential/14134349/observations/history-solution-q-146450-4dbcff2eac10e88ded86.html",
    17592186441114: "differential/14134349/observations/history-solution-q-146441-00e8a7ec5e4144c1890c.html",
    17592186441115: "differential/14134349/observations/history-solution-q-146449-0ad8a5e575d069439c52.html",
    17592186441116: "differential/14134349/observations/history-solution-q-146447-111403580e4d864c15dd.html",
    17592186486446: "differential/14160102/observations/history-solution-q-146442-adc1b4ad878d4a5fe1fb.html",
    17592186486457: "differential/14160102/observations/history-solution-q-146444-a7366ded793e869aa362.html",
    17592186486463: "differential/14160102/observations/history-solution-q-146451-77b2deeb2198c859319a.html",
    17592186555845: "differential/14234472/observations/history-solution-q-146445-ef6d217784c80a29b3ba.html",
    17592186188685: "differential/14188482/observations/history-solution-q-146169-5034999a9220203df04e.html",
    17592186502078: "differential/14188482/observations/history-solution-q-146809-f1ce6b217bfe058540b0.html",
    17592186502114: "differential/14188482/observations/history-solution-q-146819-9ee13f5b1a3b45a9d7e6.html",
    17592186502151: "differential/14188482/observations/history-solution-q-146816-fa4857e4140d2d8093dd.html",
}
MATH = re.compile(r"\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", re.S)
changes = {(row["entity"], row["attribute"]): row for row in json.loads((REPAIR / "structured/changes.json").read_text())}
findings = json.loads((REPAIR / "render-findings.json").read_text())
blocked = {row["entity"] for row in findings["new_findings"] if row.get("new_errors")}
blocked.update(row["entity"] for row in findings["remaining_preexisting_errors"])
# Reproduction is also valid after the renderer confirms these fixes.  The
# explicit whitelist retains the original eleven plus the four final failures.
assert blocked <= set(SOURCES)
output = []
total = 0
for entity, relative in SOURCES.items():
    attribute = ":question/worked-solution"
    before = changes[entity, attribute]["after"]
    sourcepath = ROOT / "reference/mathacademy/capture" / relative
    raw = sourcepath.read_bytes()
    soup = BeautifulSoup(raw, "html.parser")
    percent_nodes = [node for node in soup.select("math mo, math mi, math mtext") if node.get_text() == "%"]
    assert percent_nodes, (entity, "source has no literal percent glyph")
    source_formulas = list(dict.fromkeys(str(node.find_parent("math")) for node in percent_nodes))
    math_ranges = [(match.start(), match.end()) for match in MATH.finditer(before)]
    spans = []
    for match in re.finditer(r"(?<!\\)%", before):
        assert any(start <= match.start() < end for start, end in math_ranges)
        # Check the integer percentage directly against visible source MathML.
        number = re.search(r"(\d+)$", before[:match.start()])
        assert number, (entity, "unexpected percent context")
        percentage = number.group(1)
        matching_source = []
        for node in percent_nodes:
            previous = node.find_previous_sibling()
            if previous is not None and previous.get_text().strip() == percentage:
                matching_source.append(str(node.find_parent("math")))
        assert matching_source, (entity, percentage, "source percent value differs")
        spans.append({"start": match.start(), "end": match.end(), "before": "%", "after": r"\%",
                      "percentage": percentage, "source_mathml": matching_source[0]})
    assert len(spans) == (1 if entity == 17592186161703 else 6 if entity in
                         {17592186188685, 17592186502078, 17592186502114, 17592186502151} else 2)
    after = before
    for span in reversed(spans):
        assert after[span["start"]:span["end"]] == span["before"]
        after = after[:span["start"]] + span["after"] + after[span["end"]:]
    # Each insertion is exactly one backslash before an existing percentage.
    assert after.replace(r"\%", "%") == before.replace(r"\%", "%")
    assert not re.search(r"(?<!\\)%", after)
    total += len(spans)
    output.append({"entity": entity, "attribute": attribute, "before": before, "after": after,
                   "repair_kind": "escape-source-percent-in-hat-rendering",
                   "sourcepath": str(sourcepath), "source_sha256": hashlib.sha256(raw).hexdigest(),
                   "source_literal_percent_nodes": len(percent_nodes), "proofs": spans,
                   "reason": "An unescaped percent in the same-line aligned derivation comments out its closing environment; the source MathML contains literal percent glyphs."})
(HERE / "changes.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
summary = {"fields": len(output), "escaped_percent_occurrences": total,
           "all_source_percent_values_verified": True, "only_backslash_insertions": True,
           "no_other_fields_or_importers_changed": True}
(HERE / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
