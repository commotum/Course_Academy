#!/usr/bin/env python3
"""Verify the two classification repairs from local before/after preview pulls.

Never connects to EDB or imports a generator. Evidence is written only inside
the supplied preview directory. Usage: check_questions.py PREVIEW_DIRECTORY
"""
from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import sympy as sp
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application, parse_expr, standard_transformations,
)

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "engine/rust/learning.rs").exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import loads

REORDER = 17592186567796
SCALE = 17592186567832
RETAIN = 17592186567774
X, Y = sp.symbols("x y")
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)
BLOCK = re.compile(r"\\begin\{aligned\}\s*(.*?)\s*\\end\{aligned\}", re.S)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def canonical(value):
    """EDB cardinality-many pull order is immaterial; scalar bytes are exact."""
    if isinstance(value, dict):
        return {str(k): canonical(v) for k, v in sorted(value.items(), key=lambda p: str(p[0]))}
    if isinstance(value, (list, tuple, set)):
        return sorted((canonical(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def same(before, after, message):
    require(canonical(before) == canonical(after), message)


def load_entities(path, *, item=False):
    rows = loads(path.read_text())
    values = [row[-1 if item else 0] if isinstance(row, list) else row for row in rows]
    result = {value[":db/id"]: value for value in values}
    require(len(result) == len(values), f"Duplicate pull entities in {path.name}")
    return result


def expression(text):
    text = text.replace(" ", "").replace(r"\left", "").replace(r"\right", "").replace(r"\dfrac", r"\frac")
    while r"\frac" in text:
        updated = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", text)
        require(updated != text, f"Unsupported fraction: {text}")
        text = updated
    require(re.fullmatch(r"[0-9xy+*/().\-]+", text) is not None, f"Unsupported math: {text}")
    return sp.expand(parse_expr(text, local_dict={"x": X, "y": Y}, transformations=TRANSFORMS))


def rows(block):
    return [row.strip() for row in re.split(r"\\\\(?:\[[^\]]+\])?", block)]


def sides(row):
    parts = row.replace("&", "").split("=")
    require(len(parts) == 2, f"Expected one equality: {row}")
    return tuple(expression(part.strip()) for part in parts)


def coefficients(row):
    left, right = sides(row)
    delta = sp.expand(left - right)
    require(delta.free_symbols <= {X, Y} and sp.Poly(delta, X, Y).total_degree() == 1,
            f"Expected a linear equation: {row}")
    return tuple(Fraction(v) for v in (delta.coeff(X), delta.coeff(Y), -delta.subs({X: 0, Y: 0})))


def system(question):
    matches = list(BLOCK.finditer(question[":question/problem"]))
    require(len(matches) == 1, "Expected one displayed system")
    result = rows(matches[0][1])
    require(len(result) == 2, "Expected exactly two equations")
    return result, [coefficients(row) for row in result]


def normalized_line(row):
    pivot = next((v for v in row[:2] if v), None)
    require(pivot is not None, "Degenerate line")
    return tuple(v / pivot for v in row)


def check_substitution(question):
    _, equations = system(question)
    (a, b, c), (d, e, f) = equations
    require(normalized_line(equations[0]) == normalized_line(equations[1]), "System is not dependent")
    isolated = sp.Rational(c) / sp.Rational(a) - sp.Rational(b) / sp.Rational(a) * Y
    blocks = list(BLOCK.finditer(question[":question/worked-solution"]))
    require(len(blocks) == 3, "Expected isolation, substitution, and simplification displays")
    first, middle, last = [rows(match[1]) for match in blocks]
    require((len(first), len(middle), len(last)) == (3, 1, 4), "Substitution proof shape changed")
    for row in first:
        left, right = sides(row)
        require(sp.expand(left - right).coeff(X) != 0, "Isolation step lost its x term")
        require(sp.expand((left - right).subs(X, isolated)) == 0, "Invalid isolation step")
    require(sides(first[-1]) == (X, isolated) and sides(middle[0]) == (X, isolated),
            "Incorrect isolated x expression")
    require(coefficients(last[0]) == equations[1], "Solution uses the wrong second equation")
    expected_left = sp.expand(sp.Rational(d) * isolated + sp.Rational(e) * Y)
    for row in last[1:]:
        left, right = sides(row)
        require(left == expected_left and right == sp.Rational(f), "Invalid substitution/simplification step")
    require(expected_left == sp.Rational(f), "Dependent substitution did not reach a true identity")
    return len(first) + len(middle) + len(last)


def kind(field):
    return str(field[":answer-field/type"][":db/ident"])


def correct(field):
    eid = field[":answer-field/correct"][":db/id"]
    return next(answer for answer in field[":answer-field/choices"] if answer[":db/id"] == eid)


def native_record(question):
    fields = []
    for field in question[":question/answer-fields"]:
        require(kind(field) == ":answer-field.type/select", "Unexpected response format")
        fields.append({
            ":answer-field/key": field[":answer-field/key"],
            ":answer-field/type": kind(field),
            ":answer-field/correct": [":answer/id", str(correct(field)[":answer/id"])],
            ":answer-field/choices": [{
                ":answer/id": str(answer[":answer/id"]),
                ":answer/type": str(answer[":answer/type"][":db/ident"]),
                ":answer/value": answer[":answer/value"],
            } for answer in field[":answer-field/choices"]],
        })
    return {"question": {":question/problem": question[":question/problem"], ":question/answer-fields": fields},
            "knowledge_point": {"title": "Consistency and Dependency in Linear Systems"},
            "generation": {"template": "select-classification"}}


def fixture(question, checks, label):
    return {"label": label, "record": native_record(question), "checks": checks, "mapped_responses": []}


def verify(directory, harness):
    names = [f"preview-{entity}-{version}.edn" for entity in ("questions", "items") for version in ("before", "after")]
    before, after = [load_entities(directory / f"preview-questions-{version}.edn") for version in ("before", "after")]
    old_items, new_items = [load_entities(directory / f"preview-items-{version}.edn", item=True) for version in ("before", "after")]
    require(set(before) == set(after) and len(before) == 16, "Question scope changed")
    same(old_items, new_items, "Learner state, saved answers, or task-item membership changed")
    changed = {eid for eid in before if canonical(before[eid]) != canonical(after[eid])}
    require(changed == {REORDER, SCALE}, "Unexpected repaired question set")
    same(before[RETAIN], after[RETAIN], "The valid reordered question was changed")
    fixtures = []
    proof_rows = 0
    for eid in (REORDER, SCALE):
        old, new = before[eid], after[eid]
        expected = copy.deepcopy(old)
        if eid == REORDER:
            old_fragment, new_fragment = r"y &=4x + 9", r"y &=9 + 4x"
            require(old[":question/problem"].count(old_fragment) == 2, "Unexpected duplicate slope-intercept prompt")
            expected[":question/problem"] = old[":question/problem"].replace(old_fragment, new_fragment, 1)
            same(expected, new, "Slope-intercept repair changed more than the first RHS term order")
        else:
            old_fragment, new_fragment = r"\\ -2x - 3y &=-9", r"\\ -4x - 6y &=-18"
            require(old[":question/problem"].count(old_fragment) == 1, "Unexpected duplicate general-system prompt")
            expected[":question/problem"] = old[":question/problem"].replace(old_fragment, new_fragment)
            old_blocks = list(BLOCK.finditer(old[":question/worked-solution"]))
            new_blocks = list(BLOCK.finditer(new[":question/worked-solution"]))
            require(len(old_blocks) == len(new_blocks) == 3, "Worked solution shape changed")
            old_proof, new_proof = old_blocks[-1], new_blocks[-1]
            expected[":question/worked-solution"] = (old[":question/worked-solution"][:old_proof.start()]
                + new_proof[0] + old[":question/worked-solution"][old_proof.end():])
            same(expected, new, "General-system repair changed more than the second equation and substitution display")
            proof_rows += check_substitution(old) + check_substitution(new)
        old_rows, new_rows = system(old)[1], system(new)[1]
        require(old_rows[0] == new_rows[0], "First mathematical equation changed")
        require(normalized_line(old_rows[0]) == normalized_line(old_rows[1])
                == normalized_line(new_rows[0]) == normalized_line(new_rows[1]), "Solution line changed")
        if eid == SCALE:
            require(new_rows[1] == tuple(2 * v for v in old_rows[1]), "Second equation was not exactly doubled")
        for question, label in ((old, "before"), (new, "after")):
            expected_keys = ({"field-1": "coincide with each other", "field-2": "infinitely many solutions",
                              "field-3": "consistent dependent"} if eid == REORDER else {"field-1": "consistent dependent"})
            require({field[":answer-field/key"]: correct(field)[":answer/value"]
                     for field in question[":question/answer-fields"]} == expected_keys,
                    "Dependent-system answer keys do not match the independently established classification")
            checks = [{"field_index": i, "submitted_answer_id": str(answer[":answer/id"]),
                       "expected": "accepted" if answer[":db/id"] == correct(field)[":db/id"] else "rejected",
                       "purpose": "Unchanged authored choice grading"}
                      for i, field in enumerate(question[":question/answer-fields"])
                      for answer in field[":answer-field/choices"]]
            fixtures.append(fixture(question, checks, f"Question {eid} {label}"))
    practice = [q for q in after.values() if q.get(":knowledge-point/_questions")]
    require(len(practice) == 14, "Practice scope changed")
    for question in practice:
        printed = [re.sub(r"\s+|&", "", row) for row in system(question)[0]]
        require(printed[0] != printed[1], f"Literal duplicate equations remain in {question[':db/id']}")
    saved_checks = 0
    saved_items = 0
    for eid, item in old_items.items():
        responses = item.get(":task-item/responses", [])
        if not responses:
            continue
        saved_items += 1
        qid = item[":task-item/content"][":db/id"]
        for question, label in ((before[qid], "before"), (after[qid], "after")):
            fields = question[":question/answer-fields"]
            require(len(responses) == len(fields), "Incomplete or excessive saved responses")
            checks, seen_fields, outcomes = [], set(), []
            for response in responses:
                owners = [(i, field) for i, field in enumerate(fields)
                          if response[":db/id"] in {a[":db/id"] for a in field[":answer-field/choices"]}]
                require(len(owners) == 1, "Saved answer does not have one owning field")
                i, field = owners[0]
                require(i not in seen_fields, "Multiple saved answers for one select field")
                seen_fields.add(i)
                owned = next(a for a in field[":answer-field/choices"] if a[":db/id"] == response[":db/id"])
                same(response, owned, "Saved answer differs from its owned authored answer")
                accepted = response[":db/id"] == correct(field)[":db/id"]
                outcomes.append(accepted)
                checks.append({"field_index": i, "submitted_answer_id": str(response[":answer/id"]),
                               "expected": "accepted" if accepted else "rejected", "purpose": "Actual saved response"})
            status = str(item[":task-item/status"][":db/ident"])
            require(status in (":task-item.status/correct", ":task-item.status/incorrect"), "Unhandled saved status")
            require(all(outcomes) == status.endswith("/correct"), "Saved response disagrees with recorded outcome")
            fixtures.append(fixture(question, checks, f"Saved response {eid} {label}"))
            saved_checks += len(checks)
    input_path, report_path = directory / "question-native-input.json", directory / "question-native-report.json"
    input_path.write_text(json.dumps(fixtures, indent=2) + "\n")
    subprocess.run([str(harness), str(input_path), str(report_path)], check=True, capture_output=True, text=True, timeout=55)
    native = json.loads(report_path.read_text())
    require(native["documented_unresolved_checks"] == 0, "Unresolved native grading")
    result = {"passed": True, "database_writes": 0, "questions_checked": len(before),
              "repaired_questions": sorted(changed), "unchanged_questions": len(before) - len(changed),
              "explicitly_retained_question": RETAIN, "practice_questions_without_literal_duplicate_equations": len(practice),
              "question_field_answer_identities_keys_difficulty_and_memberships_preserved": True,
              "dependent_solution_lines_preserved": True, "independently_checked_solution_rows": proof_rows,
              "task_items_unchanged": len(old_items), "saved_response_items": saved_items,
              "saved_response_native_checks": saved_checks,
              "native": {"accepted": native["accepted_checks"], "rejected": native["rejected_checks"],
                         "unresolved": native["documented_unresolved_checks"]},
              "input_sha256": {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in names},
              "native_harness": str(harness), "native_harness_sha256": hashlib.sha256(harness.read_bytes()).hexdigest()}
    (directory / "question-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--native", type=Path, default=ROOT / "generate/scratch/17592186073778/check-engine")
    args = parser.parse_args()
    print(json.dumps(verify(args.directory.resolve(), args.native.resolve()), indent=2))


if __name__ == "__main__":
    main()
