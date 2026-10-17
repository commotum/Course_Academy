#!/usr/bin/env python3
"""Read-only verification of the scoped x-notation repair and native grading.

Usage: .venv/bin/python check_math.py PREVIEW_DIRECTORY [--native HARNESS]
Reads four preview-questions/items-before/after.edn pulls. Writes only local
grading evidence; never connects to EDB or imports the mutable generator.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import sympy as sp
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application, parse_expr, standard_transformations,
)

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "engine/rust/learning.rs").exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import loads

KP = 17592186073778
TARGET = 17592186542507
ORIGINAL_ENTERED = 17592186574812
EXPECTED_AFFECTED = {
    17592186542434, 17592186542435, 17592186542442, 17592186542448,
    17592186542452, 17592186542470, 17592186542477, 17592186542491,
    17592186542507, 17592186542509, 17592186542510,
}
X, Y, T, U = sp.symbols("x y t u")
SYMBOLS = {str(s): s for s in (X, Y, T, U)}
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def canonical(value):
    if isinstance(value, dict):
        return {str(k): canonical(v) for k, v in sorted(value.items(), key=lambda p: str(p[0]))}
    if isinstance(value, (list, tuple, set)):
        return sorted((canonical(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def same(left, right, message):
    require(canonical(left) == canonical(right), message)


def symbol_rename(math, alias):
    # Consume TeX commands whole: never replace the t in \\left or \\text.
    # Whole alphabetic tokens also protect the unit in \\[6pt] and prose inside
    # \\text{...}; coefficients such as 7t still expose the single-letter token.
    return re.sub(r"\\[A-Za-z]+|[A-Za-z]+", lambda m: "x" if m[0] == alias else m[0], math)


def prose_rename(text, alias):
    return re.sub(r"(\$\$|\$)(.*?)\1", lambda m: m[1] + symbol_rename(m[2], alias) + m[1], text, flags=re.S)


def expression(text):
    text = text.replace(" ", "").replace(r"\left", "").replace(r"\right", "").replace(r"\dfrac", r"\frac")
    while r"\frac" in text:
        changed = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", text)
        require(changed != text, f"Unsupported fraction: {text}")
        text = changed
    require("\\" not in text, f"Unsupported mathematical notation: {text}")
    return sp.expand(parse_expr(text, local_dict=SYMBOLS, transformations=TRANSFORMS))


def pair(text):
    text = text.replace(r"\left", "").replace(r"\right", "").strip()
    require(text.startswith("(") and text.endswith(")"), f"Not an ordered pair: {text}")
    parts = text[1:-1].split(",")
    require(len(parts) == 2, f"Wrong tuple shape: {text}")
    return tuple(expression(p) for p in parts)


def line(question):
    match = re.search(r"\\begin\{aligned\}\s*(.*?)\s*\\end\{aligned\}", question[":question/problem"], re.S)
    require(match is not None, "Question has no displayed system")
    equations = re.split(r"\\\\(?:\[6pt\])?", match[1])
    require(len(equations) == 2, "Expected exactly two lines")
    rows = []
    for equation in equations:
        left, right = equation.replace("&", "").split("=")
        delta = sp.expand(expression(left) - expression(right))
        require(delta.free_symbols <= {X, Y}, "Original equations changed variables")
        require(sp.Poly(delta, X, Y).total_degree() == 1, "Nonlinear displayed equation")
        rows.append((delta.coeff(X), delta.coeff(Y), -delta.subs({X: 0, Y: 0})))
    a, b, c = rows[0]
    d, e, f = rows[1]
    require(all((a, b, c, d, e, f)) and a * e == b * d and a * f == c * d, "Lines are not nonzero dependent equations")
    return rows, -a / b, c / b


def kind(field):
    return str(field[":answer-field/type"][":db/ident"])


def correct(field):
    eid = field[":answer-field/correct"][":db/id"]
    return next(a for a in field[":answer-field/choices"] if a[":db/id"] == eid)


def check_math(question, alias):
    rows, slope, intercept = line(question)
    fields = question[":question/answer-fields"]
    require(len(fields) == 1, "Changed field count")
    field = fields[0]
    variable = SYMBOLS[alias]
    target = slope * variable + intercept
    key = correct(field)
    if kind(field).endswith("/radio"):
        require(len(field[":answer-field/choices"]) == 5, "Changed radio bank size")
        valid = []
        objects = []
        for answer in field[":answer-field/choices"]:
            xx, yy = pair(answer[":answer/value"])
            require(xx == variable and (xx.free_symbols | yy.free_symbols) <= {variable}, "Wrong free coordinate in radio tuple")
            objects.append((xx, yy))
            if sp.simplify(yy - target) == 0:
                valid.append(answer[":db/id"])
        require(len(set(objects)) == 5 and valid == [key[":db/id"]], "Radio bank/key is not uniquely correct")
    else:
        require(kind(field).endswith("/blank"), "Unexpected field type")
        require(expression(key[":answer/value"]) == target, "Blank canonical expression is wrong")
        require(f"$({alias},$" in question[":question/problem"], "Blank first-coordinate convention mismatches key")
        require(f"terms of ${alias}$ only" in question[":question/problem"], "Blank instructions mismatch key")
    finals = re.findall(r"\$\$\s*(\\left\([^\n]+)\s*\$\$", question[":question/worked-solution"])
    require(len(finals) == 1, "Expected one final coordinate family")
    require(pair(finals[0]) == (variable, target), "Worked solution final tuple is wrong")
    require(f"where ${alias}$ is any number." in question[":question/worked-solution"], "Worked solution parameter differs")
    return rows, slope, intercept


def native_record(question):
    result = {":question/problem": question[":question/problem"], ":question/answer-fields": []}
    for field in question[":question/answer-fields"]:
        result[":question/answer-fields"].append({
            ":answer-field/key": field[":answer-field/key"],
            ":answer-field/type": kind(field),
            ":answer-field/correct": [":answer/id", str(correct(field)[":answer/id"])],
            ":answer-field/choices": [{
                ":answer/id": str(a[":answer/id"]),
                ":answer/type": str(a[":answer/type"][":db/ident"]),
                ":answer/value": a[":answer/value"],
            } for a in field[":answer-field/choices"]],
        })
    return {"question": result, "knowledge_point": {"title": "Finding the General Solution to a System With Infinitely Many Intersection Points"}, "generation": {"template": kind(question[":question/answer-fields"][0]).split("/")[-1]}}


def native_case(question, alias, label):
    _, slope, intercept = line(question)
    field = question[":question/answer-fields"][0]
    key = correct(field)
    if kind(field).endswith("/radio"):
        checks = [{"submitted_answer_id": str(a[":answer/id"]), "expected": "accepted" if a[":db/id"] == key[":db/id"] else "rejected", "purpose": "Preserved authored radio choice outcome"} for a in field[":answer-field/choices"]]
    else:
        checks = [
            {"submitted": key[":answer/value"], "expected": "accepted", "purpose": "Canonical scalar coordinate"},
            {"submitted": f"({slope})*({alias}-1)+({intercept + slope})", "expected": "accepted", "purpose": "Equivalent factored scalar coordinate"},
            {"submitted": f"({slope})*{alias}+({intercept + 1})", "expected": "rejected", "purpose": "Wrong intercept"},
        ]
    return {"label": label, "record": native_record(question), "checks": checks}


def load_questions(path):
    rows = loads(path.read_text())
    entities = [r[0] if isinstance(r, list) else r for r in rows]
    result = {q[":db/id"]: q for q in entities}
    require(len(result) == len(entities), "Duplicate question pull rows")
    return result


def load_items(path):
    rows = loads(path.read_text())
    entities = [r[-1] if isinstance(r, list) else r for r in rows]
    result = {i[":db/id"]: i for i in entities}
    require(len(result) == len(entities), "Duplicate item pull rows")
    return result


def verify(directory, harness):
    names = [f"preview-{entity}-{version}.edn" for entity in ("questions", "items") for version in ("before", "after")]
    before, after = [load_questions(directory / f"preview-questions-{v}.edn") for v in ("before", "after")]
    old_items, new_items = [load_items(directory / f"preview-items-{v}.edn") for v in ("before", "after")]
    require(set(before) == set(after) and len(before) == 18, "Question scope/membership changed")
    require(set(old_items) == set(new_items), "Presentation membership changed")
    fixtures, aliases, authored_updates = [], {}, 0
    new_answers = {}
    for eid, old in before.items():
        new = after[eid]
        match = re.search(r"\n\nLet \$([tu])=x\$ be the free coordinate\.", old.get(":question/worked-solution", ""))
        if not match:
            same(old, new, f"Unaffected question {eid} changed")
            continue
        alias = match[1]
        aliases[eid] = alias
        old_math = check_math(old, alias)
        new_math = check_math(new, "x")
        require(old_math == new_math, f"Displayed system changed for {eid}")
        expected = copy.deepcopy(old)
        expected[":question/problem"] = prose_rename(old[":question/problem"], alias)
        expected[":question/worked-solution"] = prose_rename(old[":question/worked-solution"].replace(match[0], ""), alias)
        ef, nf = expected[":question/answer-fields"][0], new[":question/answer-fields"][0]
        authored_ids = {a[":db/id"] for a in ef[":answer-field/choices"]} if kind(ef).endswith("/radio") else {correct(ef)[":db/id"]}
        for answer in ef[":answer-field/choices"]:
            if answer[":db/id"] in authored_ids:
                answer[":answer/value"] = symbol_rename(answer[":answer/value"], alias)
                authored_updates += 1
        ef[":answer-field/correct"][":answer/value"] = symbol_rename(ef[":answer-field/correct"][":answer/value"], alias)
        old_ids = {a[":db/id"] for a in ef[":answer-field/choices"]}
        extras = [a for a in nf[":answer-field/choices"] if a[":db/id"] not in old_ids]
        require(not extras or (eid == TARGET and len(extras) == 1), "Unexpected added answer")
        new_answers.update({a[":db/id"]: a for a in extras})
        ef[":answer-field/choices"].extend(extras)
        same(expected, new, f"Question {eid} changed beyond exact alias repair")
        fixtures.extend([native_case(old, alias, f"{eid} before"), native_case(new, "x", f"{eid} after")])
    require(set(aliases) == EXPECTED_AFFECTED, "Affected question scope drifted")
    require(authored_updates == 39 and len(new_answers) == 1, "Wrong answer repair count")
    original = next(a for a in before[TARGET][":question/answer-fields"][0][":answer-field/choices"] if a[":db/id"] == ORIGINAL_ENTERED)
    preserved = next(a for a in after[TARGET][":question/answer-fields"][0][":answer-field/choices"] if a[":db/id"] == ORIGINAL_ENTERED)
    same(original, preserved, "Original learner-entered answer was altered")
    replacement = next(iter(new_answers.values()))
    require(replacement[":answer/value"] == symbol_rename(original[":answer/value"], "t"), "Saved response replacement is not an exact alpha-renaming")
    require(str(replacement[":answer/id"]) != str(original[":answer/id"]), "Saved response identity was reused")
    same(replacement[":answer/type"], original[":answer/type"], "Saved response type changed")
    response_maps = 0
    saved_checks = 0
    for eid, old in old_items.items():
        new = new_items[eid]
        expected = copy.deepcopy(old)
        qid = old[":task-item/content"][":db/id"]
        for index, response in enumerate(expected.get(":task-item/responses", [])):
            if response[":db/id"] == ORIGINAL_ENTERED:
                expected[":task-item/responses"][index] = replacement
                response_maps += 1
        same(expected, new, f"Learner state or unrelated response changed for item {eid}")
        for question, item, label in [(before[qid], old, "before"), (after[qid], new, "after")]:
            responses = item.get(":task-item/responses", [])
            if not responses:
                continue
            require(len(responses) == 1, "Unexpected multi-field saved response")
            field = question[":question/answer-fields"][0]
            response = responses[0]
            require(response[":db/id"] in {a[":db/id"] for a in field[":answer-field/choices"]}, "Saved response lacks field ownership")
            status = str(item[":task-item/status"][":db/ident"])
            require(status in (":task-item.status/correct", ":task-item.status/incorrect"), "Unhandled saved response status")
            check = {"expected": "accepted" if status.endswith("/correct") else "rejected", "purpose": "Actual saved response preserves recorded outcome"}
            if kind(field).endswith("/blank"):
                check["submitted"] = response[":answer/value"]
            else:
                check["submitted_answer_id"] = str(response[":answer/id"])
            fixtures.append({"label": f"Saved response {eid} {label}", "record": native_record(question), "checks": [check]})
            saved_checks += 1
    require(response_maps == 1 and saved_checks == 4, "Saved-response scope changed")
    input_path, report_path = directory / "math-native-input.json", directory / "math-native-report.json"
    input_path.write_text(json.dumps(fixtures, indent=2) + "\n")
    subprocess.run([str(harness), str(input_path), str(report_path)], check=True, capture_output=True, text=True, timeout=55)
    native = json.loads(report_path.read_text())
    require(native["documented_unresolved_checks"] == 0, "Unresolved native grading")
    result = {
        "passed": True, "database_writes": 0, "questions_checked": len(before),
        "affected_questions": sorted(aliases), "unchanged_questions_including_originals": len(before) - len(aliases),
        "radio_questions": 7, "blank_questions": 4, "authored_answer_values_renamed": authored_updates,
        "displayed_systems_and_exact_solution_families_preserved": True,
        "question_field_answer_identities_and_keys_preserved": True,
        "original_entered_answer_byte_identical_and_still_owned": ORIGINAL_ENTERED,
        "saved_response_refs_mapped": response_maps, "actual_saved_response_grading_checks": saved_checks,
        "learner_status_timing_performance_and_task_links_unchanged": True,
        "native": {"accepted": native["accepted_checks"], "rejected": native["rejected_checks"], "unresolved": native["documented_unresolved_checks"]},
        "input_sha256": {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in names},
        "native_harness": str(harness), "native_harness_sha256": hashlib.sha256(harness.read_bytes()).hexdigest(),
    }
    (directory / "math-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--native", type=Path, default=ROOT / "generate/scratch/17592186073778/check-engine")
    args = parser.parse_args()
    print(json.dumps(verify(args.directory.resolve(), args.native.resolve()), indent=2))


if __name__ == "__main__":
    main()
