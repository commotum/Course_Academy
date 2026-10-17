"""Independently check the conformability label repair and native grading.

This reads fixed-basis native preview pulls only. It never accesses the database.
Usage: python3 check_questions.py PREVIEW_DIRECTORY
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
from uuid import UUID

sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "Cargo.toml").exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import loads

NONE_IDS = {17592186562892, 17592186562914}
NONE_LABEL = "None of these products is well defined."
ROMANS = ("I", "II", "III")
MATRIX = re.compile(r"([A-Z])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}", re.S)
STATEMENT = re.compile(
    r"^\s*-\s*\*\*(I{1,3})\.\*\*\s+The product \$([A-Z])([A-Z])\$ is well defined\.?\s*$",
    re.M,
)
ROMAN_REF = re.compile(r"\bstatements?\s+[IVX]+\b|\*\*[IVX]+\.\*\*")
NATIVE = ROOT / "reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/check-checkbox-engine"


def insist(condition, message):
    if not condition:
        raise AssertionError(message)


def normalized(value):
    """Pull cardinality-many values are unordered; preserve all scalar values."""
    if isinstance(value, dict):
        return {str(k): normalized(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        return sorted((normalized(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return str(value) if isinstance(value, UUID) else value


def same(left, right, message):
    insist(normalized(left) == normalized(right), message)


def without(record, *keys):
    return {k: v for k, v in record.items() if k not in keys}


def rows(path):
    value = loads(path.read_text())
    # Native pulls are bare records; fixed-basis query evidence wraps find rows.
    return [v[0] if isinstance(v, list) and len(v) == 1 else v for v in value]


def dimensions(problem):
    found = MATRIX.findall(problem)
    insist(len(found) in (2, 3), "Expected exactly two or three displayed matrices")
    result = {}
    for name, body in found:
        matrix_rows = body.split(r"\\")
        widths = {len(row.split("&")) for row in matrix_rows}
        insist(len(widths) == 1, f"Ragged matrix {name}")
        insist(name not in result, f"Duplicate displayed matrix {name}")
        result[name] = (len(matrix_rows), widths.pop())
    return result


def fields_by_id(question):
    fields = question.get(":question/answer-fields", [])
    result = {f[":db/id"]: f for f in fields}
    insist(len(result) == len(fields), "Duplicate field entity in question")
    return result


def boolean_bank(field):
    insist(field[":answer-field/type"][":db/ident"] == ":answer-field.type/checkbox", "Expected checkbox field")
    bank = {a[":answer/value"]: a for a in field[":answer-field/choices"]}
    insist(set(bank) == {"false", "true"} and len(field[":answer-field/choices"]) == 2, "Expected exactly two owned Boolean answers")
    for answer in bank.values():
        insist(answer[":answer/type"][":db/ident"] == ":answer.type/text", "Boolean answer type changed")
    correct = field[":answer-field/correct"]
    same(correct, bank[correct[":answer/value"]], "Correct answer is not an owned answer")
    return bank


def to_native(question, label, expected_truth):
    native_fields = []
    fields = question[":question/answer-fields"]
    for f in fields:
        native_fields.append({
            ":answer-field/key": f[":answer-field/key"],
            ":answer-field/type": f[":answer-field/type"][":db/ident"],
            ":answer-field/correct": [":answer/id", str(f[":answer-field/correct"][":answer/id"])],
            ":answer-field/choices": [{
                ":answer/id": str(a[":answer/id"]),
                ":answer/type": a[":answer/type"][":db/ident"],
                ":answer/value": a[":answer/value"],
            } for a in f[":answer-field/choices"]],
        })
    checks = []
    for i, field in enumerate(fields):
        for value, answer in boolean_bank(field).items():
            checks.append({"field_index": i, "submitted_answer_id": str(answer[":answer/id"]),
                           "expected": "accepted" if (value == "true") == expected_truth[field[":db/id"]] else "rejected",
                           "purpose": "independent dimension-based truth"})
    return {
        "label": label,
        "record": {"question": {":question/problem": question[":question/problem"], ":question/answer-fields": native_fields},
                   "knowledge_point": {"title": "Determining Whether Two Matrices Are Conformable for Multiplication"},
                   "generation": {"template": str(question[":db/id"])}},
        "checks": checks,
        "mapped_responses": [],
    }


def add_response(fixture, question, selected, expected, purpose):
    fixture["mapped_responses"].append({
        "old_answer": purpose,
        "answer_ids": [str(boolean_bank(field)["true" if selected[field[":db/id"]] else "false"][":answer/id"])
                       for field in question[":question/answer-fields"]],
        "expected": expected,
    })


def check(directory):
    before = {q[":db/id"]: q for q in rows(directory / "preview-questions-before.edn")}
    after = {q[":db/id"]: q for q in rows(directory / "preview-questions-after.edn")}
    insist(len(before) == 18 and set(before) == set(after), "Expected all 18 KP questions at both snapshots")
    fixtures, reports, truths, added_fields = [], [], {}, {}
    before_fixture, after_fixture = {}, {}
    all_before_subsets = all_after_subsets = equivalent_subsets = 0
    for qid in sorted(before):
        old, new = before[qid], after[qid]
        old_fields, new_fields = fields_by_id(old), fields_by_id(new)
        if not old_fields:
            same(old, new, f"Canonical example {qid} changed")
            reports.append({"id": qid, "canonical_unchanged": True})
            continue
        insist(len(old_fields) == 3, f"Expected three original fields on {qid}")
        same(without(old, ":question/problem", ":question/worked-solution", ":question/answer-fields"),
             without(new, ":question/problem", ":question/worked-solution", ":question/answer-fields"),
             f"Question {qid} metadata, memberships, or difficulty changed")
        same(MATRIX.findall(old[":question/problem"]), MATRIX.findall(new[":question/problem"]), f"Question {qid} matrices changed")
        dims = dimensions(old[":question/problem"])
        same(dims, dimensions(new[":question/problem"]), f"Question {qid} dimensions changed")
        entries = STATEMENT.findall(old[":question/problem"])
        products = {roman: a + b for roman, a, b in entries}
        insist(len(entries) == 3 and set(products) == set(ROMANS), f"Cannot uniquely resolve {qid} original statements")
        insist(not ROMAN_REF.search(new[":question/problem"]), f"Question {qid} still has Roman list labels")
        insist("The product $" not in new[":question/problem"], f"Question {qid} still duplicates checkbox statements in prompt")
        insist("Select all that apply." in new[":question/problem"], f"Question {qid} lost checkbox instructions")
        old_body, old_conclusion = old[":question/worked-solution"].rsplit("\n\n", 1)
        new_body, new_conclusion = new[":question/worked-solution"].rsplit("\n\n", 1)
        same(old_body, new_body, f"Question {qid} solution reasoning changed")
        insist(not ROMAN_REF.search(new[":question/worked-solution"]), f"Question {qid} has orphaned Roman references")
        insist(set(old_fields) <= set(new_fields), f"Question {qid} lost original fields")
        field_truth = {}
        for fid, old_field in old_fields.items():
            new_field = new_fields[fid]
            roman = old_field[":answer-field/key"]
            insist(roman in products, f"Unknown old field label in {qid}")
            product = products[roman]
            truth = dims[product[0]][1] == dims[product[1]][0]
            field_truth[fid] = truth
            insist(new_field[":answer-field/key"] == f"The product ${product}$ is well defined.", f"Wrong statement label for {qid}/{roman}")
            same(without(old_field, ":answer-field/key"), without(new_field, ":answer-field/key"), f"Question {qid}/{roman} old IDs, banks, or key changed")
            boolean_bank(new_field)
            insist((new_field[":answer-field/correct"][":answer/value"] == "true") == truth, f"Question {qid}/{roman} key disagrees with matrix dimensions")
        extras = set(new_fields) - set(old_fields)
        if qid in NONE_IDS:
            insist(not any(field_truth.values()), f"Question {qid} unexpectedly has a true product")
            insist(len(extras) == 1, f"Question {qid} needs exactly one explicit None field")
            fid = extras.pop()
            field = new_fields[fid]
            insist(field[":answer-field/key"] == NONE_LABEL, f"Question {qid} None label mismatch")
            boolean_bank(field)
            insist(field[":answer-field/correct"][":answer/value"] == "true", f"Question {qid} None must be true")
            old_entity_ids = {e[":db/id"] for f in old_fields.values() for e in [f, *f[":answer-field/choices"]]}
            new_entity_ids = {e[":db/id"] for e in [field, *field[":answer-field/choices"]]}
            insist(len(new_entity_ids) == 3 and not old_entity_ids & new_entity_ids, "None field reuses an old entity")
            added_fields[qid] = fid
            field_truth[fid] = True
        else:
            insist(not extras and any(field_truth.values()), f"Question {qid} has unexpected new fields or an empty key")
        insist(any(field_truth.values()), f"Question {qid} offers no correct positive selection")
        conclusion_truth = {}
        for sentence in re.split(r"(?<=\.)\s+", new_conclusion):
            if sentence == f"Select “{NONE_LABEL}”":
                insist(qid in NONE_IDS, f"Question {qid} solution recommends an absent None field")
                continue
            match = re.fullmatch(r"The products? (.+?) (?:is|are) (well defined|undefined)\.", sentence)
            insist(match is not None, f"Question {qid} has an unrecognized final conclusion: {sentence}")
            names = re.findall(r"\$([A-Z]{2})\$", match[1])
            remainder = re.sub(r"\$[A-Z]{2}\$|\band\b|[,\s]", "", match[1])
            insist(names and not remainder, f"Question {qid} conclusion contains an unknown product expression")
            for name in names:
                insist(name not in conclusion_truth, f"Question {qid} repeats a product in its conclusion")
                conclusion_truth[name] = match[2] == "well defined"
        expected_product_truth = {product: dims[product[0]][1] == dims[product[1]][0] for product in products.values()}
        same(conclusion_truth, expected_product_truth, f"Question {qid} solution conclusion disagrees with matrix dimensions")
        truths[qid] = field_truth
        old_truth = {fid: field_truth[fid] for fid in old_fields}
        old_fixture = to_native(old, f"before-{qid}", old_truth)
        new_fixture = to_native(new, f"after-{qid}", field_truth)
        before_fixture[qid], after_fixture[qid] = old_fixture, new_fixture
        for bits in itertools.product((False, True), repeat=len(old_fields)):
            selected = dict(zip(old_fields, bits))
            expected = selected == old_truth
            add_response(old_fixture, old, selected, expected, f"all old subsets {bits}")
            all_before_subsets += 1
            mapped = dict(selected)
            if qid in added_fields:
                mapped[added_fields[qid]] = not any(bits)
            insist((mapped == field_truth) == expected, f"Question {qid} old subset correctness changed")
            add_response(new_fixture, new, mapped, expected, f"equivalent old subset {bits}")
            equivalent_subsets += 1
        for bits in itertools.product((False, True), repeat=len(new_fields)):
            selected = dict(zip(new_fields, bits))
            add_response(new_fixture, new, selected, selected == field_truth, f"all new subsets {bits}")
            all_after_subsets += 1
        fixtures.extend((old_fixture, new_fixture))
        reports.append({"id": qid, "dimensions": dims, "products": products,
                        "truth": {products[f[":answer-field/key"]]: field_truth[fid] for fid, f in old_fields.items()},
                        "old_ids_and_banks_preserved": True, "new_none_field": added_fields.get(qid),
                        "solution_reasoning_preserved": True, "new_conclusion": new_conclusion})

    old_items = {i[":db/id"]: i for i in rows(directory / "preview-items-before.edn")}
    new_items = {i[":db/id"]: i for i in rows(directory / "preview-items-after.edn")}
    insist(len(old_items) == 3 and set(old_items) == set(new_items), "Expected all three learner items before and after")
    response_reports = []
    for iid, old in old_items.items():
        new = new_items[iid]
        qid = old[":task-item/content"][":db/id"]
        same(without(old, ":task-item/responses"), without(new, ":task-item/responses"), f"Learner item {iid} state changed")
        if qid not in truths:
            same(old, new, f"Canonical completed item {iid} changed")
            response_reports.append({"item": iid, "question": qid, "unchanged": True})
            continue
        old_selected, new_selected = {}, {}
        for question, item, selected in ((before[qid], old, old_selected), (after[qid], new, new_selected)):
            responses = {a[":db/id"]: a for a in item.get(":task-item/responses", [])}
            owned = set()
            for fid, field in fields_by_id(question).items():
                matches = [a for a in field[":answer-field/choices"] if a[":db/id"] in responses]
                insist(len(matches) == 1, f"Saved item {iid} has missing or duplicate response for {fid}")
                answer = matches[0]
                same(answer, responses[answer[":db/id"]], f"Saved item {iid} response content changed")
                selected[fid] = answer[":answer/value"] == "true"
                owned.add(answer[":db/id"])
            insist(owned == set(responses), f"Saved item {iid} has an unowned response")
        expected_new = dict(old_selected)
        if qid in added_fields:
            fid = added_fields[qid]
            expected_new[fid] = not any(old_selected.values())
            none_answer = boolean_bank(fields_by_id(after[qid])[fid])["true" if expected_new[fid] else "false"]
            same(new[":task-item/responses"], old[":task-item/responses"] + [none_answer], f"Saved item {iid} changed original responses")
        else:
            same(old, new, f"Saved item {iid} should be unchanged")
        same(expected_new, new_selected, f"Saved item {iid} semantics changed")
        old_correct = old_selected == {fid: truths[qid][fid] for fid in old_selected}
        new_correct = new_selected == truths[qid]
        insist(old_correct == new_correct, f"Saved item {iid} correctness changed")
        status = old[":task-item/status"][":db/ident"]
        if status in (":task-item.status/correct", ":task-item.status/incorrect"):
            insist(old_correct == (status == ":task-item.status/correct"), f"Saved item {iid} original grade disagrees with stored status")
        add_response(before_fixture[qid], before[qid], old_selected, old_correct, f"saved item {iid}")
        add_response(after_fixture[qid], after[qid], new_selected, new_correct, f"saved item {iid}")
        response_reports.append({"item": iid, "question": qid, "correctness_preserved": True,
                                 "state_preserved": True, "new_none_response": qid in added_fields})

    fixture_path = directory / "independent-native-grading-input.json"
    native_report_path = directory / "independent-native-grading-report.json"
    fixture_path.write_text(json.dumps(fixtures, indent=2) + "\n")
    subprocess.run([str(NATIVE), str(fixture_path), str(native_report_path)], check=True)
    native = json.loads(native_report_path.read_text())
    report = {
        "database_writes": 0, "questions": len(before), "practice_questions": len(truths),
        "canonical_examples_unchanged": len(before) - len(truths),
        "original_subsets_checked": all_before_subsets, "new_subsets_checked": all_after_subsets,
        "equivalent_old_subsets_checked": equivalent_subsets, "learner_items_checked": len(old_items),
        "native_whole_responses_checked": native["whole_original_choices_preserved"],
        "all_checks_passed": True, "question_checks": reports, "learner_item_checks": response_reports,
    }
    (directory / "independent-question-verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("question_checks", "learner_item_checks")}))


if __name__ == "__main__":
    insist(len(sys.argv) == 2, "Usage: check_questions.py PREVIEW_DIRECTORY")
    check(Path(sys.argv[1]).resolve())
